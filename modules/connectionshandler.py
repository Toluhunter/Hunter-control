import select
from threading import Thread

class Handler:
    def __init__(self, server):
        self.SERVER = server
    
    #recieves socket pair(host and client) and threads the connection
    def add(self, socket_set, ID, timeout=5*60):
        socket_set[0].sendall('Connected'.encode('utf-8'))
        self.thread = Thread(target=self.forward_msg, args=(socket_set, ID, timeout))
        self.thread.start()

    def session_timeout(self, ID, timeout=300, count=0):
        while self.SERVER.accepting: 
            socket_set = self.SERVER.users(ID)

            ready, _, _ = select.select(socket_set, [], [], 1)
            #if host doesnt have a client after time out close connection remove id
            if ((ready) or (not self.SERVER.accepting) or (count == timeout)):
                return ready

            count += 1

    def forward_msg(self, socket_set, ID, timeout):
        while self.SERVER.accepting:
            
            ready = self.session_timeout(ID)
            #when select times out return empty list which raises IndexError
            #if cmd or response is empty close connection
            if ready:
                if ready[0] is socket_set[0]:
                    cmd = socket_set[0].recv(2048)

                    if cmd.decode('utf-8'):
                        socket_set[1].send(cmd)
                    else:
                        break
                    
                else:
                    response = socket_set[1].recv(2048)

                    if response.decode('utf-8'):
                        socket_set[0].send(response)
                    else:
                        break
                            
        socket_set[0].close()
        socket_set[1].close()
        self.SERVER.close_session(ID)