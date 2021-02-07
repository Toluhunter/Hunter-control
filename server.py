import socket,random,time
import concurrent.futures as exec
import modules.ConnectionsHandler as handle

class server:
    def __init__(self):
        self.users=dict()
        self.accepting=True
        self.handle=handle.Handler(self)

        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setblocking(False)
        self.s.bind((socket.gethostbyname(''),8890))
        self.s.listen(4)
        
        self.thread=exec.ThreadPoolExecutor(max_workers=1)
        self.thread.submit(self.close)
        self.accept_conn()
        

    def close(self):
        #allows admin to shutdown server and close all conection
        while (self.accepting):
            input('Enter any key to shutdown server...')
            #prints all sessions currently on the server
            for i in self.users:
                print(i,end=" ")

            print("")
            confirm=input('are you sure you wish to shutdown sever y/n:')

            if confirm=='y':
                #closes server accept_conn(stops accepting more connections)
                self.accepting=False
                print('\nshutting down server this can take up to 5 minutes please wait')
                time.sleep(0.5)
                
   
    def accept_conn(self):
        while (self.accepting):
            #catches BlockingIOError from non-blocking socket
            try:
                self.socket_api,self.addr=self.s.accept()
                user_type=self.socket_api.recv(30).decode('utf-8')
                user_type=user_type.split(':')
            
                if user_type[0]=='host':
                    id_timeout=60
                    id=self.generate_id()
                    host_tag=id+':'+str(id_timeout)
                    self.users[id]=[]
                    self.socket_api.send(host_tag.encode('utf-8'))
                    self.users[id].append(self.socket_api)
                    self.handle.timeout(id,id_timeout)

                elif user_type[0]=='client':
                    id=user_type[1]
                    #If Id doesn't exist or host already has client raise key error
                    try:
                        pair=self.users[id]
                        if(len(pair)==2):
                            raise KeyError

                        self.users[id].append(self.socket_api)
                        self.handle.add(self.users[id],id)

                    except KeyError:
                        self.socket_api.send('wrong id'.encode())
                        self.socket_api.close()

            except BlockingIOError:
                pass
        print('Connections will no longer be accepted')
            

    def generate_id(self):
        id=random.randint(1111,9999)
        id=str(id)

        #Ensures ID is not already in use
        while id in self.users:
            id=random.randint(1111,9999)
            id=str(id)

        return id

    def __del__(self):
        self.thread.shutdown()

def main():
    server_obj=server()
    
if __name__=="__main__":
    main()
