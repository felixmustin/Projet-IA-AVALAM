import socket
import sys
import json
import cherrypy


class EchoClient:
    def __init__(self, msg):
        self.__s = socket.socket()
        self.__msg = msg

    def run(self, host, port):
	    self.__s.connect((host, port))
	    self._send()
	    self.__s.close()

    def _send(self):
        msg = json.dumps(self.__msg).encode('utf8')
        totalsent = 0
        while totalsent < len (msg):
            sent = self.__s.send(msg[totalsent:])
            totalsent += sent



port = int(sys.argv[1])
name = sys.argv[2]
matricule = str(sys.argv[3])

msg = {"matricules": [matricule, "22222"], "port": 8081, "name": name}

EchoClient(msg).run('localhost', port)