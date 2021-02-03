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
        
        
    def recv(self,buffer):
        msg=self.socket_api.recv(buffer)
        msg=str(msg,'utf-8')
        return msg
    def close(self):
        while (self.accepting):
            input('Enter any key to shutdown server...')
            # print(self.users)
            confirm=input('are you sure you wish to shutdown sever y/n:')
            if confirm=='y':
                self.accepting=False
                print('\nshutting down server this can take up to 2 minutes please wait')
                time.sleep(0.5)
                

        
    def accept_conn(self):
        
        while (self.accepting):
            
            try:
                self.socket_api,self.addr=self.s.accept()
                
                user_type=self.recv(11).split(':')
            
                if user_type[0]=='host':
                    id=self.generate_id()
                    self.users[id]=[]
                    self.socket_api.send(id.encode())
                    self.users[id].append(self.socket_api)

                elif user_type[0]=='client':
                    id=user_type[1]
                    try:
                        if(len(self.users[id])==2):
                            raise Exception
                        self.users[id].append(self.socket_api)
                        self.handle.add(self.users[id],id)
                    except:

                    
                        self.socket_api.send('wrong id'.encode())
                        self.socket_api.close()
            except:
                pass
        print('Connections will no longer be accepted')
            

    def generate_id(self):
        id=random.randint(1111,9999)
        id=str(id)
        while id in self.users:
            id=random.randint(1111,9999)
            id=str(id)
        return str(id)

    def __del__(self):
        self.thread.shutdown()
def main():
    server_obj=server()
    
if __name__=="__main__":
    main()
