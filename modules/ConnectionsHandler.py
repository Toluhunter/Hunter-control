import concurrent.futures as exec
import time,select
class Handler:
    def __init__(self,server):
        self.server=server
        self.thread=exec.ThreadPoolExecutor()

    
    #recieves socket pair(host and client) and threads the connection
    def add(self,socket_set,id,timeout=5*60):
        for i in socket_set:
            i.send('0'.encode('utf-8'))
            
        self.thread.submit(self.forward_msg,socket_set,id,timeout)


    #threads the timeout of the id if clients doesnt connect
    def timeout(self,id,timeout):
        self.thread.submit(self.id_timeout,id,timeout)
        
    
    #timeout threaded to prevent blocking of main thread
    def id_timeout(self,id,timeout):
        socket_set=self.server.users[id]

        time.sleep(timeout)

        #if host doesnt have a client after time out close connection remove id
        if len(self.server.users[id])!=2:
            socket_set[0].close()
            self.server.users.pop(id)


    def forward_msg(self,socket_set,id,timeout):
        while self.server.accepting:
            
            ready,_,_=select.select(socket_set,[],[],timeout)
            #when select times out return empty list which raises IndexError
            #if cmd or response is empty close connection
            try:    
                if ready[0] is socket_set[0]:
                    cmd=socket_set[0].recv(2048)

                    if cmd.decode('utf-8')!='':
                        socket_set[1].send(cmd)
                    else:
                        raise IndexError

                else:
                    response=socket_set[1].recv(2048)

                    if response.decode('utf-8')!='':
                        socket_set[0].send(response)
                    else:
                        raise IndexError
                            
            except IndexError:
                break

        if(not self.server.accepting):
            print(f'\nsession {id} was closed')

        socket_set[0].close()
        socket_set[1].close()
        self.server.users.pop(id)
    

    def __del__(self):
        self.thread.shutdown()