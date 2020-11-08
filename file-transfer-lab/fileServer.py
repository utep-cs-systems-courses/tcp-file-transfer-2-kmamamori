#! /usr/bin/env python3

import sys, os, re, socket
sys.path.append("../lib")
import params
from framedSock import framedSend, framedReceive
from os.path import exists

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "echosever"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


while True:
    sock, addr = lsock.accept()
    print("connection rec'd from", addr)
    if not os.fork():
        while True:
            payload = framedReceive(sock, debug)
            if not payload:
                break
            payload = payload.decode()

            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug)
                try:
                    payload2 = framedReceive(sock, debug)
                except:
                    print("Connection has being disconnected.")
                    sys.exit(1)
                if not payload2:
                    break
                payload2 += b"!"
                try:
                    framedSend(sock, payload2, debug)
                except:
                    print("Connection has being disconnected")
                    sys.exit(1)
                output = open(payload, 'wb')
                output.write(payload2)
                output.close()
        sock.close()
