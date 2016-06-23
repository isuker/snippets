# -*- coding: utf-8 -*-
import os,os.path

#import pdb
#pdb.set_trace()

import paramiko
from celery import Celery, Task, exceptions
from celery.result import AsyncResult
#http://docs.celeryproject.org/en/latest/reference/celery.contrib.methods.html
from celery.contrib.methods import task_method

from app.models import TestBed, TestSet, TestJob
# don't mix app any more, here we use another namespace
from app import app as flask_app
from app import testbed, testset

import setting

celery = Celery(__name__)
celery.config_from_object(setting)

class TestClient(object):

    def __init__(self, hostname='10.244.178.54',username='root',password='c4dev!'):
        '''Now only default is my dev vm'''

        self.hostname = hostname
        self.username = username
        self.password = password
        self.connected = False
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = paramiko.SSHClient()
            #self._transport = paramiko.Transport(self.hostname)
            self._session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self._session.connect("10.244.178.54", username="root", password="c4dev!")
                #self._transport.connect(username="root", password="c4dev")
                self.connected = True
            except:
                print "connect to %s failed" %self.hostname

        return self._session

    def __del__(self):
        self.session.close()
        self.connected = False

    def getFile(self, filename):
        pass

    def putFile(self, local_file, remote_filename=""):
        """upload local file to remote host"""

        #sftp=paramiko.SFTPClient.from_transport(self._transport)
        sftp = self.session.open_sftp()

        # if remote filename is missing, we just upload to "/" on remote 
        #with same filename 
        if remote_filename == "":
            remote_filename = os.path.join("/", os.path.basename(local_file))
        sftp.put(local_file, remote_filename)
        sftp.close()

    def run(self, cmd):

        print cmd
        (stdin, stdout, stderr) = self.session.exec_command(cmd)
        response = {'stdout': stdout.readlines(), 'stderr': stderr.readlines()}
        print response['stdout']
        print response['stderr']

        self.response = response
        return self.response


class AutomatosManager(object):
    """Automatos Execute Client"""

    _client = None

    # Default config on my dev vm
    LOG_BASE_DIR = "/srv/www/vhosts/ring-check/automatos"
    WORKSPACE = "/opt/automatos/Automatos/Tests/Dev"
    #TEMPLATE = "/opt/automatos/Automatos/Tests/Dev/mainConfig.xml.template"
    MAIN_CONFIG = """
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<opt doc_type="MAIN_CFG" version="1">
   <local_base_log_path>/tmp/logs</local_base_log_path>
   <test_set_file>FunctionalTest/HostEnablement/HighAvailability/testSetInfo.xml</test_set_file>
   <testbed_file>FunctionalTest/HostEnablement/HighAvailability/HA_MPIO_BC-D1059-RHEL.xml</testbed_file>
   <execution_parameters>
       <parameter name="STOP_ON_ERROR" value="0"></parameter>
       <parameter name="LOGGING_LEVEL" value="INFO"></parameter>
   </execution_parameters>
</opt>
"""

    CMD = "cd %s; perl -I /opt/automatos/Automatos/Framework/Dev/lib/ /opt/automatos/Automatos/Framework/Dev/bin/automatos.pl --configFile "%WORKSPACE

    def __init__(self, testbed, testset, logdir, client=None):

        self.testbed = testbed
        self.testset = testset
        self.logpath = os.path.join(self.LOG_BASE_DIR, logdir)
        self._client = client or TestClient()

    @property
    def client(self):
        if self._client is None:
            self._client = TestClient()
        return self._client

    def composeMainConfig(self):
        '''generate mainConfig file for Automatos'''

        tbFilename = os.path.join(self.logpath, self.testbed.filename)
        # raise RuntimeError('working outside of application context')
        tbUrl = tsUrl = ""
        tsPath = tbPath = ""
        with flask_app.test_request_context():
            tbUrl = self.testbed.url
            tsUrl = self.testset.url
            tsPath = testset.path(self.testset.filename)
            tbPath = testbed.path(self.testbed.filename)

        #tbCmd = "cd %s;wget -c %s -o %s" %(self.logpath, tbUrl, tbFilename)
        #self.client.run(tbCmd)
        tsFilename = os.path.join(self.logpath, self.testset.filename)
        #tsCmd = "cd %s; wget -c %s -o %s" %(self.logpath, tsUrl, tsFilename)
        #self.client.run(tsCmd)

        self.client.putFile(tsPath, tsFilename)
        self.client.putFile(tbPath, tbFilename)

        # generate mainConfig.xml
        from xml.etree import ElementTree
        root = ElementTree.ElementTree(ElementTree.fromstring(self.MAIN_CONFIG.strip()))
        log_node= root.find("local_base_log_path")
        log_node.text = self.logpath
        set_node = root.find('test_set_file')
        set_node.text = tsFilename
        bed_node= root.find('testbed_file')
        bed_node.text = tbFilename

        # saved local file
        saved_file = "/tmp/MainConfigfile-%s-%s.%s.xml" %(self.testset.filename, \
                        self.testbed.filename, os.getpid())
        root.write(saved_file)

        # upload to Test Client
        remote_mcFile = os.path.join(self.logpath, "mainConfig.xml")
        self.client.putFile(saved_file, remote_mcFile)

        return remote_mcFile

    def start(self):

        # create logdir
        self.client.run("mkdir -p %s"%self.logpath)
        mcFile = self.composeMainConfig()

        cmd = self.CMD + mcFile
        return self.client.run(cmd)


#@celery.task(filter=task_method)
#@celery.task(base=Manager)

@celery.task
def execute(testbed_id, testset_id, logdir):

    bed = TestBed.query.filter(testbed_id == TestBed.id).first_or_404()
    set = TestSet.query.filter(testset_id == TestSet.id).first_or_404()

    # now the only test client is Ray's dev vm
    client = AutomatosManager(bed, set, logdir)
    return client.start()

#@celery.task
# Not a celery task
def query(job_id):
    '''Query the automatos execute status'''
    job = TestJob.query.filter(job_id == TestJob.id).first_or_404()
    
    result = AsyncResult(job.task_id, backend=celery.backend)
    response = {'stdout':[""], 'stderr':[""]}
    try:
        response = result.get(timeout=1)
    except exceptions.TimeoutError, e:
        print "Task:%s didn't finish yet" %job.task_id
        response['stdout'] = ["Job:%d is still running, please wait..." %job.id]
    except exceptions.TaskRevokedError, e:
        print "Task:%s have been terminated" %job.task_id
    except:
        print "Unknown failture for query"

    return (result.state,response)

def stop(job_id):
    '''Stop the automatos execute status'''
    job = TestJob.query.filter(job_id == TestJob.id).first_or_404()
    result = AsyncResult(job.task_id, backend=celery.backend)
    result.revoke()

    celery.control.revoke(job.task_id, terminate=True, signal='SIGKILL')

    return "cancel success"
    

if __name__ == "__main__":

    #bed = TestBed.query.filter(1 == TestBed.id).first_or_404()
    #set = TestSet.query.filter(1 == TestSet.id).first_or_404()
    #m = AutomatosManager(bed, set, "ray/job10000")
    #m.start()

    print query(1)


