import concurrent.futures as exec
import time,select
class Handler:
    def __init__(self,server):
        self.server=server
        self.thread=exec.ThreadPoolExecutor()

    def add(self,socket_set,id):
        for i in socket_set:
            i.send('0'.encode('utf-8'))
            
        self.thread.submit(self.forward_msg,socket_set,id)

    def forward_msg(self,socket_set,id):
        timeout_secs=100
        while self.server.accepting:
            
            ready,_,_=select.select(socket_set,[],[],timeout_secs)
            try:
                    
                if ready[0] is socket_set[0]:
                    cmd=socket_set[0].recv(2048)
                    if cmd.decode('utf-8')!='':
                        socket_set[1].send(cmd)
                    else:
                        raise Exception

                else:
                    response=socket_set[1].recv(2048)
                    if response.decode('utf-8')!='':
                        socket_set[0].send(response)
                    else:
                        raise Exception
                            
            except:
                break
        if(not self.server.accepting):
            print(f'\nsession {id} was closed')
        time.sleep(3)
        socket_set[0].close()
        socket_set[1].close()
        time.sleep(0.1)
        self.server.users.pop(id)