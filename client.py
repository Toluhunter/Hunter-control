import socket,time,re
import subprocess,os,ssl
import concurrent.futures as exec
class client:
    def __init__(self,ip):
        self.ip=ip
        self.animating=False
        self.thread=exec.ThreadPoolExecutor()

    def connect(self,id='0000'):
        socket_obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_obj.connect((self.ip,8890))

        time.sleep(0.5)

        user_type='client:'+id
        socket_obj.send(user_type.encode())
        response=socket_obj.recv(30).decode('utf-8')

        if response=='wrong id':
            print(response)
            return False

        self.socket_api=socket_obj
        return True


    def run_cmd(self,cmd):
        responses=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for response in responses.communicate():

            if response:
                return response

        #returns if command doesnt have output or error
        return 'command executed with return code 0\n'.encode('utf-8')

   
    def awaiting_animation(self):
        time.sleep(2)
        while (self.animating):
            print('awaiting command'+' '*30,end="\r")
            if(not self.animating):
                break
            time.sleep(0.8)

            print('awaiting command.'+' '*30,end="\r")
            if(not self.animating):
                break
            time.sleep(0.8)

            print('awaiting command..'+' '*30,end="\r")
            if(not self.animating):
                break
            time.sleep(0.8)

            print('awaiting command...'+' '*30,end="\r")
            if(not self.animating):
                break
            time.sleep(0.8)
        

    def display(self):
        choice=''
        print('==================== client mode ==================')

        while True:
            self.thread.submit(self.awaiting_animation)
            cmd=self.socket_api.recv(1024).decode('utf-8')
            self.animating=False
            time.sleep(1)

            if cmd=='':
                print('Disconnected')
                break

            #sends current working directory to host
            elif cmd=='pwd?ps1':
                response=os.getcwd().encode('utf-8')
                self.socket_api.send(response)

            elif cmd=='exit':
                print('Disconnected')
                response=f'command executed with return code 0 {cmd}\n'.encode('utf-8')
                self.socket_api.send(response)
                time.sleep(0.2)
                self.socket_api.close()
                break
            
            else:
                if choice!='a':
                    print('\ncommand: '+cmd)
                    choice=input('Do you wish to allow this command to run on your system\n(Y/y=yes N/n=no A/a=allow no confirmation ): ')

                    while(not choice):
                        print('Please Enter an option')
                        choice=input('Do you wish to allow this command to run on your system\n(Y/y=yes N/n=no A/a=allow no confirmation ): ')

                    choice=choice[0].lower()

                if choice=='a' or choice=='y':

                    #checks for the "cd /path" command
                    if re.search(r'^cd (.+)',cmd) or cmd=='cd':
                        print(cmd)
                        #gets the path from the command
                        for match in re.finditer(r'^cd (.+)',cmd):
                            cmd=match.group(1)
                        
                        try:
                            os.chdir(cmd)
                            response='command executed with return code 0\n'.encode('utf-8')

                        except FileNotFoundError:
                            response=f'command executed with return code 127\nno directory with the name {cmd}\n'.encode('utf-8')

                        finally:
                            self.socket_api.send(response)

                    else:
                        print('\ncommand: '+cmd)
                        response=self.run_cmd(cmd)
                        try:
                            response_str=response.decode('utf-8')
                            print(f'\n{response_str}')
                        except UnicodeDecodeError:
                            response="Command could not be decoded"
                            print(response)
                            response=response.encode('utf-8')

                        print('='*30)
                        self.socket_api.send(response)

                else:
                    print(cmd+' (DENIED)')
                    self.socket_api.send('command Denied by client'.encode('utf-8'))
            self.animating=True


def main():
    #checks for active internet connection
    try:
        test_internet=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        test_internet=ssl.wrap_socket(test_internet)
        test_internet.connect(("google.com",443))
        test_internet.close()
    except socket.gaierror:
        print("This program requires an active internet connection\nCheck your connection and try again")
        return

    id=input('Input id:')

    while(not re.match(r'^[1-9]{1}\d{3}$',id)):
        print('Invalid input please try agin')
        id=input('Input id:')

    #Replace with your Server Ip
    ip=os.getenv('SERVERIP')
    client_obj=client(ip)
    status=client_obj.connect(id)

    if status:
        client_obj.display()
    else:
        print('Disconnected')


if __name__=='__main__':
    main()
