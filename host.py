import socket, time
import sys
import os
import select, ssl
from platform import system

import colorama

class Host:
    def __init__(self):
        if system() == 'Windows':
            colorama.init(convert=True)

        self.green = colorama.Fore.GREEN
        self.red = colorama.Fore.RED
        self.reset = colorama.Fore.RESET
        self.blue = colorama.Fore.LIGHTBLUE_EX

        self.animating = True


    def connect(self, ip):
        '''Forms a connection with the server while recievind id and timeout'''
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #attempt to connect to server
        try:
            socket_obj.connect((ip, 8890))
        except ConnectionRefusedError:
            print(f'''{self.red}Server is currently not active
                   \rPlease startup server code on your designated server {self.reset}''')
            socket_obj.close()
            return False

        socket_obj.send('host'.encode('utf-8'))
        self.socket_api = socket_obj

        user_tag = self.socket_api.recv(30).decode('utf-8')
        id, timeout = user_tag.split(':')
        timeout = int(timeout)

        print('Your id is', id)
        print(f'''Id will expire in {self.blue}{timeout}{self.reset}
                  \rIf connection is not formed with client\n''')
        
        #returns connected message when host is associated with a client
        status, [], [] = select.select([self.socket_api], [], [], timeout)

        return status 


    def send_cmd(self, command):
        '''sets a long value for timeout to wait for client authentication
           except for exit which requires no authentication'''
        
        output=''
        minute = 60 

        if command != 'exit':
            timeout = minute * 4
        else:
            timeout = 2

        command=command.encode('utf-8')
        self.socket_api.sendall(command)

        # waits for response for client uses loop to read in large responses 
        while True:
            response,_,_=select.select([self.socket_api],[],[],timeout)
            if response:
                out=self.socket_api.recv(2048).decode('utf-8')

                if out=='':
                    break

                output+=out
                #resets timeout once message has been sent
                timeout=1
            else:
                break

        return output


    #request for current location
    @property
    def current_loc(self):
        return self.send_cmd('pwd?ps1')

    def user_input(self, cwd):
        ''' Gets input from standard input '''
        minute = 60
        cmd = ''

        while(not cmd):
            if system() == 'Windows':
                print(f'{self.green}{cwd}{self.blue}> {self.reset}', end='')
                cmd = input().strip()

            else:
                # Times out user input if no command has been entered in 4 minutes
                print(f'{self.green}{cwd}{self.blue}> {self.reset}', end='', flush=True)
                stdin_cmd = select.select([sys.stdin], [], [], minute * 4)

                if stdin_cmd[0]:
                    cmd = stdin_cmd[0][0].readline().strip()

                else:
                    cmd = 'exit'

        return cmd


    def check_network(self):
        '''checks for active internet connection'''
        try:
            test_internet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            test_internet = ssl.wrap_socket(test_internet)
            test_internet.connect(("google.com", 443))
            test_internet.close()
        
        except socket.gaierror:
            print(f'''{self.red}This program requires an active internet connection
                      \rCheck your connection and try again {self.reset}''')
            return False
        
        return True


    def display_term(self):
        '''Displays a shell for users to input commands for the client system '''
        print('=================== Host Mode ===================')

        while True:
            #gives a short period to allow client get ready for command
            time.sleep(0.4)
            cwd=self.current_loc

            if cwd:
                cmd = self.user_input(cwd)
                response = self.send_cmd(cmd)
                if response == '':
                    print(f'{self.red}Disconnected {self.reset}')
                    break

                print(response)

                if cmd == 'exit':
                    self.socket_api.close()
                    print(f'{self.red}Disconnected {self.reset}')
                    break
            else:
                print(f'{self.red}Disconnected {self.reset}')
                break
            

def main():
    host = Host()
    if not host.check_network():
        exit(2)

    #Replace with your own ip
    ip = os.getenv('SERVER')
    if not ip:
        ip = input("Enter your ip address of the server: ")
    #returns empty string if server is shutdown or id timesout
    status = host.connect(ip)

    if status:
        msg = status[0].recv(1024).decode('utf-8')
        if msg[-1] == '$':
            msg = msg.rstrip('$')
            print(f'{host.red}{msg}{host.reset}')
            host.socket_api.close()
        else:
            print(msg)
            start = time.time()
            host.display_term()
            stop = time.time()

            print(f'Session Lasted for {stop-start} second(s)')
    else:
        print(f'{host.red}An Unexpected issue occured{host.reset}')

if __name__ == "__main__":
    main()

