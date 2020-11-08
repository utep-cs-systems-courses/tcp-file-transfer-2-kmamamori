#! /usr/bin/env python3
import socket, sys, re
sys.path.append("../lib")
import params
sys.path.append("../framed-echo")
from framedSock import framedSend, framedReceive
from os.path import exists

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

file_to_send = input("Enter the file name: ")
if exists(file_to_send):
    cp_file = open(file_to_send, 'rb')
    data_file = cp_file.read()
    cp_file.close()
    if len(data_file)==0:
        print("Empty file")
        sys.exit(0)
    else:
        print("File found.\n")
        file_name = input("give us file name: ")
        framedSend(s,file_name.encode(), debug)
        fileExistance = framedReceive(s, debug)
        fileExistance = fileExistance.decode()

        """
        try:
            framedSend(s, file_name.encode(), debug)
            fileExistance = framedReceive(s, debug)
            fileExistance = fileExistance.decode()
        except:
            print("Connection has being disconnected")
            """
        if fileExistance == 'True':
            print("File already exist in the server")
            sys.exit(0)
        else:
            try:
                print("try sending")
                framedSend(s, data_file, debug)
            except:
                print("Sending Error: check your conection status")
                sys.exit(0)
            try:
                print("try receive")
                framedReceive(s, debug)
            except:
                print('Receiving Error: check your connection status')
                sys.exit(0)
else:
    print("file not found.")
    sys.exit(0)

s.close()
