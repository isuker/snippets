#!/usr/bin/python
#
# yum-build -- a tool to install latest Fedora package from sources. 
# Author: Ray Chen <chenrano2002@gmail.com>
#

import os
import sys
import subprocess
import commands
import shlex
import rpm

FEDORA_GITS_URL="http://pkgs.fedoraproject.org/gitweb"
REPO_DIR="/tmp/fedora/portage"
# set by rpmdevtools by default
RPMBUILD_DIR=os.path.expanduser("~/rpmbuild")

def usage():
    usage = """
yum-build -- a tool to install latest Fedora package from sources. 
usage:
        yum-build.py packagename
    """
    print usage
    sys.exit(1)

def list_all_packages():
    '''Get a list of all fedora package name
    From:
        http://pkgs.fedoraproject.org/gitweb/

    '''
    pkgs = []

    return pkgs

def exec_cmd(cmd_str):
    '''execute local cmd on host'''
    args = shlex.split(cmd_str)
    print "="*60
    retcode = 1 # 0 mean Success, 1 mean Failure
    try:
        retcode = subprocess.call(args)
    except:
        # 1 mean Failure
        reccode = 1

    if retcode:
		sys.stdout.write("*** Run Cmd '%s': FAIL ***\n"%cmd_str)
    else:
		sys.stdout.write("*** Run Cmd '%s': PASS ***\n"%cmd_str)

    print "="*60,"\n"
    return retcode == 0

def fetch_package_spec(pkg):
    '''Fetch package spec file and source files
    Two steps:
        1. git clone git://pkgs.fedoraproject.org/pkg
        2. spectool -g -C DIR pkg.spec

    '''
    # enter repo dir
    os.chdir(REPO_DIR)

    # if package git repo already exists, just pull
    # else, use git clone to download
    if os.path.exists(pkg):
        os.chdir(pkg)
        if not exec_cmd("git pull"):
            return False
    else:

        CLONE_CMD="git clone git://pkgs.fedoraproject.org/%s" %pkg
        if not exec_cmd(CLONE_CMD):
            return False

    # enter git repo dir
    os.chdir(os.path.join(REPO_DIR,pkg))

    # OK, package spec file is fetched.
    # Now start to download source tar file
    dest_dir = os.path.join(RPMBUILD_DIR, "SOURCES", pkg)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    SPECTOOL_CMD="spectool -g -C %s %s.spec" %(dest_dir,pkg)
    if not exec_cmd(SPECTOOL_CMD):
        return False

    # it's time to move all patch files
    PATCH_CMD="spectool -l %s.spec"%pkg
    (exitstatus, outtext) = commands.getstatusoutput(PATCH_CMD)
    if exitstatus:
        return False

    # get the path filename from CLI output
    all_files = map(lambda line: line.split(":")[1].strip(),outtext.strip().split("\n"))
    copied_files = filter(lambda name: not (name.startswith("http") or name.startswith("ftp")), all_files)

    files = " ".join(copied_files)
    if len(files) > 0:
        if not exec_cmd("cp %s %s"%(files, dest_dir)):
            return False

    return True

def analy_pkg_spec(filename):
    '''return the version and release info from spec file'''

    (ver, rel) = ("", "")
    with open(filename, 'r') as f:
        for line in f.readlines():
            line.strip()

            if line.startswith("Version"):
                ver = line.split(":")[1].strip()
                continue
            if line.startswith("Release"):
                rel = line.split(":")[1].split("%")[0].strip()
                continue
        # end for
                
    return (ver, rel)

def is_update_needed(pkg,specfile):
    '''check whether the version of newly built package is higher
       than local package. If it is, just skip all build process. 
    '''

    (local_ver, local_rel) = ("", "")
    ts = rpm.TransactionSet()
    mi = ts.dbMatch('name', pkg)
    if len(mi) == 0:
        # package is not installed on system
        return True

    if len(mi) == 1:
        for head in mi:
            local_ver = head['version']
            local_rel = head['release'].split(".")[0]
    
    # version info from spec file
    (ver, rel) = analy_pkg_spec(specfile)

    # compare
    if str(ver) > str(local_ver):
        return True
    else:
        if str(ver) == str(local_ver):
            return str(rel) > str(local_rel)

    # end if
    return False

def build_package(pkg):
    '''rpmbuild to build RPM, return the rpm file name
        if build failed for skipped, return None
    '''

    # enter git repo dir
    os.chdir(os.path.join(REPO_DIR,pkg))
    spec_file = os.path.join(REPO_DIR, pkg, "%s.spec"%pkg)
    (version, release) = analy_pkg_spec(spec_file)
    filename = "%s-%s-%s" %(pkg, version, release)

    if not is_update_needed(pkg, spec_file):
        sys.stdout.write("The package '%s' already installed and latest version. Skip build...\n"%filename)
        return None

    # install dependce for this package
    if not exec_cmd("sudo yum-builddep -y %s.spec"%pkg):
        return None

    sourcedir = os.path.join(RPMBUILD_DIR, "SOURCES", pkg)
    RPMBUILD_CMD="rpmbuild --define '_sourcedir %s' -ba %s.spec" %(sourcedir,pkg)
    if not exec_cmd(RPMBUILD_CMD):
        return None

    # get the rpm file name
    # search the rpm file in '~/rpmbuild/RPMS'
    # The generated RPM must be located in "~/rpmbuild/RPMS"
    rpm_dir = os.path.join(RPMBUILD_DIR, "RPMS")
    FIND="find %s -name %s*" %(rpm_dir, filename)
    (exitstatus, outtext) = commands.getstatusoutput(FIND)
    if exitstatus:
        return None
        
    return outtext
    
def install_package(rpm_file):
    '''local install RPM file using YUM'''

    INSTALL_CMD="sudo yum localinstall %s" %rpm_file
    if not exec_cmd(INSTALL_CMD):
        return False

    return True

def init_env():
    exec_cmd("rpmdev-setuptree")
    exec_cmd("mkdir -p %s"%REPO_DIR)

    return True

def main(args):

    init_env()

    # golbal vars
    fedora_pkgs = list_all_packages()

    pkg = args[1]
    if not pkg in fedora_pkgs:
        print "%s is NOT invalid package name" %pkg
        #sys.exit(1)

    print "yum-build '%s' package starts..." %pkg

    # step 1:
    #   a) fetch package spec
    #   b) download source tar files
    if not fetch_package_spec(pkg):
        print "Step 1: dowload source tar files failed."
        sys.exit(1)

    # step 2:
    #   build rpm from source files
    rpm_file = build_package(pkg)
    if rpm_file is None:
        print "Step 2: build rpm file failed or skipped."
        sys.exit(1)

    # step 3:
    #   install rpm file using Yum
    install_package(rpm_file)

    print "yum-build '%s' package ends!" %pkg


if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    main(sys.argv)
