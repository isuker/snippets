#!/usr/bin/env python

import re
import socket
import logging


DANMU_SERVER = 'openbarrange.douyutv.com'
DANMU_PORT = 8601

log = logging.getLogger(__name__) 


class InvalidParam(Exception):
    pass


class ResponseError(Exception):
    pass


class DanMuResponse(object):
    MSG_MAP = {
        '0': 'Success',
        '51': 'Data transport error',
        '52': 'The Server is closed',
        '204': 'Wrong Room ID',
    }

    def __init__(self, response):
        self.content = response

    @property
    def data(self):
        _data = []
        parts = self.content.split("/")
        for p in parts:
            if p:
                (key, value) = p.split('@=')
                _data.append({key: value})
        log.debug("response data: %s" % _data)
        return _data

    def __repr__(self):
        return repr(self.data)

    def has_error(self):
        return 'error' in self.content

    def check(self):
        if not self.has_error():
            return True
        # if error found, generate related exception
        code = self.data[1]['code']
        if code not in self.MSG_MAP:
            msg = 'Unknown Error'
        else:
            msg = self.MSG_MAP[code]
        raise ResponseError(msg)


class DanMuMsg(object):
    def __init__(self, content, is_server=False):
        self.length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
        self.code = self.length
        self.magic = bytearray([0xb1, 0x02, 0x00, 0x00])
        self.content = bytes(content.encode("utf-8"))
        self.end = bytearray([0x00])

    @property
    def bytes(self):
        return bytes(self.length + self.code + self.magic + self.content + self.end)


class DanMuClient(object):

    def __init__(self, server=DANMU_SERVER, port=DANMU_PORT):
        self.server = server
        self.port = port

        self._is_live = False
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
        # if contain '@', then convert to '@A'
        msg = msg.replace('@', '@A')
        # if contain '/', then convert to '@S'
        msg = msg.replace('/', '@S')
        log.debug('converted msg: %s' % msg)
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

    def _parse_response(self, msg):
        content = msg[12:-1].decode('utf-8', 'ignore')
        res = DanMuResponse(content)
        res.check()

    def login(self, room_id):
        msg = self._build_msg(type='logreq', roomid=str(room_id))
        self.send(msg)
        # check the response from server
        res = self._session.recv(2048)
        self._parse_response(res)

    def logout(self):
        msg = self._build_msg(type='logout')
        self.send(msg)

    def send(self, text, is_server=False):
        msg = DanMuMsg(text, is_server)
        log.debug('start send message: %s' % text)
        try:
            self._session.sendall(msg.bytes)
        except socket.error as e:
            log.debug("Send message failed with %s" % e)


    def heartbeat(self, interval=30):
        msg = self._build_msg(type='keeplive', tick=time())
        self.send(msg)
        self._is_live = True

    def join_group(self, rid, gid=-9999):
        msg = self._build_msg(type='joingroup', rid=rid, gid=gid)
        self.send(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    danmu = DanMuClient(server='122.188.107.179')
    danmu.login(48699)
