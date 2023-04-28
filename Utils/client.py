import socket, time, re
import subprocess, os, ssl
from platform import system
from threading import Thread

import colorama

class client:

    def __init__(self, ip):
        if system() == 'Windows':
            colorama.init(convert=True)

        self.GREEN = colorama.Fore.GREEN
        self.RED = colorama.Fore.RED
        self.RESET = colorama.Fore.RESET
        self.BLUE = colorama.Fore.LIGHTBLUE_EX

        self.ip = ip
        self.animating = True


    def check_network(self):
        ''' checks for active internet connection '''
        try:
            test_internet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            test_internet = ssl.wrap_socket(test_internet)
            test_internet.connect(("google.com", 443))
            test_internet.close()

        except socket.gaierror:
            print('{self.RED}This program requires an active internet connection')
            print('Check your connection and try again {self.RESET}')
            return False
        else:
            return True


    def connect(self, id='0000'):
        ''' Forms a connection to the server with user type '''
        socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        try:
            socket_obj.connect((self.ip, 8890))
        except Exception:
            print(f"{self.RED}EITHER SERVER IS NOT UP OR CHECK IP{self.RESET}")
            return False

        time.sleep(0.2)

        user_type = 'client:' + id
        socket_obj.sendall(user_type.encode())
        response = socket_obj.recv(30).decode('utf-8')
        
        print(response+'\n')
        # if user id is invalid 
        if response == 'wrong id':
            return False

        self.socket_api = socket_obj
        return True


    def run_cmd(self, cmd):
        choice = ''
        response = ''

        while(not choice):
            print('Please Enter an option')
            choice = input('''Do you wish to allow this command
                              \rto run on your system\n
                              \r(Y/y=yes N/n=no A/a=allow no confirmation ):'''
                              ).strip()
            print('')

            choice = choice[0].lower()

        if choice == 'a' or choice=='y':
            #checks for the "cd /path" command
            if re.search(r'^cd (.+)',cmd) or cmd == 'cd':
                print(cmd)
                #gets the path from the command
                for match in re.finditer(r'^cd (.+)', cmd):
                    cmd = match.group(1)
                        
                try:
                    os.chdir(cmd)
                    response = 'command executed with return code 0\n'
                except FileNotFoundError:
                    response = f'''command executed with return code 127
                                   \rno directory with the name {cmd}
                                   '''

            else:
                responses = subprocess.Popen(
                        cmd,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                        )

                # loops through the output and error messages returns non empty response
                for msg in responses.communicate():
                    if msg:
                        response = msg
                    
                if response == '':
                    response = 'command executed with return code 0\n'.encode('utf-8')

                # test if message can be represented in UTF-8 format
                try:
                    response = response.decode('utf-8')
                except UnicodeDecodeError:
                    response = "Command could not be decoded"

        else:
            response = cmd+f'{self.RED} (DENIED BY CLIENT) {self.RESET}'
        
        return response


    def awaiting_animation(self):
        ''' animation for awaiting connection '''
        dots = 0
        msg = f'{self.BLUE}Awaiting command'
        print(msg, end='', flush=True)
        while (self.animating):

            if dots > 3:
                dots = 0

            print('.'*dots, end='', flush=True)

            time.sleep(0.5)
            print('\b \b'*dots, end='', flush=True)
            dots += 1

        clear = len(msg) + dots
        #clears Animation text once animating is done
        print('\b \b'*clear, end='', flush=True)
        print(f'{self.RESET}', end='', flush=True)


    def display(self):
        ''' Display output of commands sent by host computer '''
        print('==================== client mode ==================')

        while True:
            thread = Thread(target=self.awaiting_animation)
            # starts awaiting animation on seperate thread
            thread.start()

            cmd=self.socket_api.recv(1024).decode('utf-8')
            #stops awaiting animation
            self.animating=False
         
            thread.join()

            if cmd=='':
                print(f'{self.RED}Disconnected {self.RESET}')
                break

            #sends current working directory to host
            elif cmd=='pwd?ps1':
                response=os.getcwd().encode('utf-8')
                self.socket_api.send(response)

            elif cmd=='exit':
                print(f'{self.RED}Disconnected {self.RESET}')
                response=f'command executed with return code 0 {cmd}\n'.encode('utf-8')
                self.socket_api.send(response)
                time.sleep(0.2)
                self.socket_api.close()
                break
            
            else:
                print(f'\n{self.BLUE}Command: {self.GREEN}{cmd}{self.RESET}')

                response = self.run_cmd(cmd)

                print(response)
                response = response.encode('utf-8')
                print('='*30)
                self.socket_api.send(response)

            self.animating=True


def main():

    ip = os.getenv('SERVER')
    if not ip:
        ip = input("Enter your IP address: ")

    client_obj = client(ip)
    
    # Ends program if theres no internet connection
    if not client_obj.check_network():
        exit(2)

    id = input('Input id: ')

    while(not re.match(r'^[1-9]{1}\d{3}$', id)):
        print(f'{client_obj.RED}Invalid input please try agin {client_obj.RESET}')
        id=input('Input id: ')

    #Replace with your Server Ip
    status = client_obj.connect(id)

    if status:
        client_obj.display()
    else:
        print(f'{client_obj.RED}Disconnected {client_obj.RESET}')


if __name__=='__main__':
    main()
