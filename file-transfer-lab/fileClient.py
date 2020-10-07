#! /usr/bin/env python3
import socket, sys, re
sys.path.append("../lib")
import params
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)

sendingFile = input("Enter the file name")
if exists(sendingFile):
    cp_file = open(sendingFile, 'r')
    data_file = cp_file.read()
    if len(data_file)==0:
        print("Empty file")
        sys.exit(0)
    else:
        framedSend(s, sendingFile.encode(), debug)
        try:
            fileExistance = framedReceive(s, debug)
            fileExistance = fileExistance.decode()
        except:
            print("Connection has being disconnected")
        if fileExistance == True:
            print("File already exist in the server")
            sys.exit(0)
        else:
            try:
                framedSend(s, data_file, True)
            except:
                print("Error: check your conection status")
            try:
                framedReceive(s, True)
            except:
                print('Error: check your connection status')
else:
    print("file not found.")
    sys.exit(0)

s.close()
