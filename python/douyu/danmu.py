#!/usr/bin/env python
# encoding: utf-8

import time
import socket
import logging
import threading
import signal

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DANMU_SERVER = 'openbarrage.douyutv.com'
DANMU_PORT = 8601

log = logging.getLogger(__name__)

def rid_to_url(room_id):
	return 'http://www.douyu.com/' + str(room_id)

class InvalidParam(Exception):
    pass


class ResponseError(Exception):
    pass


class DanMuResponse(object):
    MSG_ERROR_MAP = {
        '0': 'Success',
        '51': 'Data transport error',
        '52': 'The Server is closed',
        '204': 'Wrong Room ID',
    }

    def __init__(self, response):
        self.content = str(response)
        self.data = self._to_dict(self.content)

    @staticmethod
    def _convert_msg(msg):
        while msg.find('@A') != -1:
            msg = msg.replace('@A', '@')
        while msg.find('@S') != -1:
            msg = msg.replace('@S', '/')
        return msg

    def _to_dict(self, raw):
        _data = {}
        log.debug("response raw data: %s" % raw)
        parts = raw.split('/')
        for p in parts:
            try:
                (key, value) = p.split('@=', 1)
                value = self._convert_msg(value)

                # The list@={body} will contain nested data
                if 'ranklist' in raw and value.startswith('list'):
                    raw_list = value.split('//')
                    value = map(lambda x: self._to_dict(x), raw_list)
                # end if
                _data[key] = value
            except ValueError as e:
                log.debug("split string '%s' failed" % p)
        log.debug("response data dict %s" % _data)
        return _data

    def __getattr__(self, item):
        if item == "_covert_msg":
            return self._convert_msg
        try:
            return self.data[item]
        except KeyError:
            log.error("Key '%s' is not found in response" % item)
            return ""

    def __repr__(self):
        return repr(self.data)

    def has_error(self):
        return 'error' in self.content

    def raise_if_error(self):
        if not self.has_error():
            return True
        # if error found, generate related exception
        code = self.code
        if code not in self.MSG_ERROR_MAP:
            msg = 'Unknown Error'
        else:
            msg = self.MSG_ERROR_MAP[code]
        raise ResponseError(msg)

    def _show_chat_msg(self):
        #message = "\t".join([self.type, self.nn]) + '<' + \
        #          ",".join([self.uid, self.level]) + '>\t' + self.txt
        #log.info(message)
        log.info("{0:>6}  {1:>16}<{2}, {3}>  {4:<32}".
                 format(self.type, self.nn, self.uid, self.level, self.txt))

    def _show_user_enter(self):
        message = "\t".join([self.type, self.nn]) + '<' + \
                  ", ".join([self.uid, self.level]) +  '>\t' + "Enter this room"
        log.info(message)

    def _show_gift(self):
        message = self.type + self.gn + "<" + self.gc + ">\t" + \
                  " => ".join([self.sn, self.dn]) + ' In Room ' + rid_to_url(self.drid)
        log.info(message)

    def _show_rank_list(self):
        log.info("ranklist TODO")

    def _show_online_gift(self):
        log.info("onlinegift TODO")

    def _show_send_gift(self):
        log.info("dgb TODO")

    def display(self):
        if self.type == 'chatmsg':
            #log.info("Type NickName<uid, level> Message")
            self._show_chat_msg()
        elif self.type == 'uenter':
            self._show_user_enter()
        elif self.type == 'spbc':
            #log.info("Type Gift<Number> Sender Receiver Room")
            self._show_gift()
        elif self.type == 'ranklist':
            #log.info("Type Room Sender Receiver Room")
            self._show_rank_list()
        elif self.type == 'onlinegift':
            self._show_online_gift()
        elif self.type == 'dgb':
            self._show_send_gift()
        else:
            log.debug("Ignore this unknown message type: %s" % self.type)


class DanMuMsg(object):
    """dou yu protocol message with little byteorder"""
    def __init__(self, content, is_server=False):
        self.length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
        self.code = self.length
        self.magic = bytearray([0xb1, 0x02, 0x00, 0x00])
        # client code is 689, server code is 690
        if is_server:
            self.magic = bytearray([0xb2, 0x02, 0x00, 0x00])
        self.content = bytes(content.encode("utf-8"))
        self.end = bytearray([0x00])

    @property
    def bytes(self):
        return bytes(self.length + self.code + self.magic + self.content + self.end)


class DanMuClient(object):

    def __init__(self, server=DANMU_SERVER, port=DANMU_PORT):
        self.server = server
        self.port = port

        self._is_live = True
        self._build_conn()

    def __del__(self):
        if self._session is not None:
            self._session.close()
    
    def _build_conn(self):
        try:
            self._session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._session.connect((self.server, self.port))
        except socket.error as msg:
            self._session = None
            log.error("Connect with DanMu Server failed: %s" % msg)
            raise

    @staticmethod
    def _convert(msg):
        msg = str(msg)
        # if contain '@', then convert to '@A'
        msg = msg.replace('@', '@A')
        # if contain '/', then convert to '@S'
        msg = msg.replace('/', '@S')
        return msg

    def _build_msg(self, **kwargs):
        msg_type = kwargs.pop('type')
        if not msg_type:
            raise InvalidParam('missing type parameter')

        # type is the first key
        msg = 'type@=' + msg_type + '/'
        for (key, value) in kwargs.iteritems():
            key = self._convert(key)
            value = self._convert(value)
            msg += '@='.join([key, value]) + '/'
            
        log.debug('built message is %s' % msg)
        return msg

    def _parse_response(self):
        msg = self._session.recv(4096)
        content = msg[12:-1].decode('utf-8', 'ignore')
        response = DanMuResponse(content)
        response.raise_if_error()
        return response

    def login(self, room_id, username="", password=""):
        #msg = self._build_msg(type='loginreq', username=username,
        #                      password=password, roomid=str(room_id))
        msg = 'type@=loginreq/roomid@=/%s/' % room_id
        self.send(msg)
        # check the response from server
        self._parse_response()

    def logout(self):
        msg = self._build_msg(type='logout')
        self.send(msg)

    def send(self, text):
        msg = DanMuMsg(text)
        log.debug('start send message: %s' % text)
        try:
            self._session.sendall(msg.bytes)
        except socket.error as e:
            log.debug("Send message failed with %s" % e)


    def heartbeat(self, interval=40):
        while self._is_live:
            msg = self._build_msg(type='keeplive', tick=int(time.time()))
            self.send(msg)
            try:
                self._parse_response()
                self._is_live = True
                log.debug("heart beat is ok, retry in %d second later" % interval)
                time.sleep(interval)
            except ResponseError as error:
                log.error("Found heart beat error: %s" % error)
                self._is_live = False
        # End while

    def join_group(self, rid, gid=-9999):
        msg = self._build_msg(type='joingroup', rid=rid, gid=gid)
        self.send(msg)
        self._parse_response()

    def run(self, room_id):
        def signal_handler(signal, frame):
            log.info(" ...You Pressed CTL+C ,exit... ")
            self._is_live= False
            self._thread.join()
            self.logout()
            sys.exit(1)
        # end def
        signal.signal(signal.SIGINT, signal_handler)

        log.info("Show Danmu in Room: '%s'" % rid_to_url(room_id))
        self.login(room_id)

        # start new thread to keep monitor heartbeat
        self._thread = threading.Thread(target=self.heartbeat)
        self._thread.setDaemon(True)
        self._thread.start()
        self.join_group(room_id)

        # Now keeping get the danmu message
        while self._is_live:
            message = self._parse_response()
            message.display()

        log.info("Finish run")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(name)-8s:%(lineno)d %(levelname)-6s %(message)s',
            filename='test.log',
            datefmt = '%m-%d %H:%M:%S')

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-6s %(message)s')
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

    danmu = DanMuClient()
    danmu.run(room_id=sys.argv[1])

