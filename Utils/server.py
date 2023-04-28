import os
import socket,random,time
import colorama
from platform import system
from threading import Thread
from Connection.ConnectionsHandler import Handler

class Server:
    def __init__(self):
        
        if system() == 'Windows':
            colorama.init(convert=True)
            self.CLEAR = 'cls'
        else:
            self.CLEAR = 'clear'

        self.RESET = colorama.Fore.RESET
        self.GREEN = colorama.Fore.GREEN
        self.YELLOW = colorama.Fore.YELLOW
        self.BLUE = colorama.Fore.CYAN
        
        self.__users = dict()
        self.__accepting = True

    @property
    def accepting(self) :
        return  self.__accepting
    
    def users(self, id='0000'):
        if id != '0000':
            return self.__users[id]

        return self.__users 

    def close_session(self, id):
        self.__users.pop(id)

    def close(self):
        ''' allows admin to shutdown server and close all conection '''
        while (self.accepting):
            print("1: clear")
            print("2: list users")
            print("3: shutdown")
            option = input("Select your option: ").strip()

            if option == '1':        
                os.system(self.CLEAR)
                
            #prints all sessions currently on the server
            elif option == '2':
                if not self.users():
                    print(f"{self.BLUE}No Users currently connected{self.RESET}\n")
                    continue

                for i in self.users():
                    if len(self.users(i)) != 2:
                        print(f"Host {i} has formed a conection and is {self.YELLOW}awaiting{self.RESET} a client")

                    else:
                        print(f"Host {i} has formed a {self.GREEN}successful{self.RESET} connection with a client")
                print()

            #closes server accept_conn(stops accepting more connections)
            elif option == '3':
                self.__accepting = False
                print('\nshutting down server this can take up to 5 minutes please wait')
                time.sleep(0.5)
                
    def id_timeout(self, id, timeout=60):
        socket_set = self.users(id)
        count=0

        #if host doesnt have a client after time out close connection remove id
        while True:
            peer = len(self.users(id))
            if peer > 1:
                break
            elif (peer < 2 and  count == timeout) or not self.accepting:
                msg = 'SERVER SHUTDOWN$' if not self.accepting else 'Timeout$'
                socket_set[0].sendall(msg.encode('utf-8'))
                #wait for client to close connection to prevent TIME_WAIT state
                time.sleep(3)
                socket_set[0].close()
                self.__users.pop(id)
                break
            else:
                time.sleep(1)
                count += 1
   
    def accept_conn(self):
        timeout = Thread()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(False)
        s.bind(('', 8890))
        s.listen(4)


        handle = Handler(self)
        thread = Thread(target=self.close)
        
        thread.start()
        while (self.accepting):
            #catches BlockingIOError from non-blocking socket
            try:
                socket_api, addr = s.accept()
                user_type = socket_api.recv(30).decode('utf-8')
                user_type = user_type.split(':')
            
                if user_type[0] == 'host':
                    ttl_server = 60
                    # Client will close connection if no response from server in 70 seconds
                    ttl_client=70
                    id = self.generate_id()
                    host_tag = id+':'+str(ttl_client)
                    self.__users[id] = []
                    socket_api.send(host_tag.encode('utf-8'))
                    self.__users[id].append(socket_api)
                    timeout = Thread(target=self.id_timeout, args=(id, ttl_server))
                    timeout.start()

                elif user_type[0] == 'client':
                    id = user_type[1]
                    #If Id doesn't exist or host already has client raise key error
                    try:
                        pair = self.users(id)
                        if(len(pair) == 2):
                            raise KeyError
                        
                        socket_api.sendall('Id accepted'.encode('utf-8'))
                        self.__users[id].append(socket_api)
                        handle.add(self.users(id), id)

                    except KeyError:
                        socket_api.send('wrong id'.encode())
                        socket_api.close()

            except BlockingIOError:
                pass
            
        thread.join()

        if timeout.is_alive():
            timeout.join()
        print('Connections will no longer be accepted')


    def generate_id(self):
        id = random.randint(1111, 9999)
        id = str(id)

        #Ensures ID is not already in use
        while id in self.users():
            id = random.randint(1111, 9999)
            id = str(id)

        return id

def main():
    obj = Server()
    obj.accept_conn()
    
if __name__ == "__main__":
    main()
