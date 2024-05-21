from xander_plugin import *
import socket
import threading

recvSocket = None
recvThread = None

def onload():
    global recvSocket
    global recvThread
    recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    recvSocket.bind(("127.0.0.1", 5036))
    recvThread = threading.Thread(target=recvloop, daemon=True)
    recvThread.start()
    log("Wrapper plugin loaded.")

def recvloop():
    while True:
        try:
            message, address = recvSocket.recvfrom(1024)
        except:
            continue
        if message.decode() == "ping":
            log("Got ping from wrapper.")

def onexit():
    global recvSocket
    recvSocket.close()
    log("Wrapper plugin exit run.")