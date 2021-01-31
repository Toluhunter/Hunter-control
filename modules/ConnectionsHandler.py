import concurrent.futures as exec
import time
class Handler:
    def __init__(self,server):
        self.server=server
        self.thread=exec.ThreadPoolExecutor()

    def add(self,socket_set,id):
        for i in socket_set:
            i.send('0'.encode('utf-8'))
        self.thread.submit(self.forward_msg,socket_set,id)

    def forward_msg(self,socket_set,id):
        while self.server.accepting:
            cmd=socket_set[0].recv(2048)
            socket_set[1].send(cmd)
            response=socket_set[1].recv(2048)
            socket_set[0].send(response)