import socket,time,re
import subprocess,os
class client:
    def __init__(self,ip):
        self.ip=ip
    def connect(self,id):
        socket_obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_obj.connect((self.ip,8890))
        time.sleep(0.5)
        user_type='client:'+str(id)
        socket_obj.send(user_type.encode())
        cmd=socket_obj.recv(30).decode('utf-8')
        if cmd=='wrong id':
            print(cmd)
            return False
        self.socket_api=socket_obj
        return True
    def check_cmd(self,cmd):
        responses=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        responses.wait()
        for response in responses.communicate():
            if response:
                return response
        return 'command executed with return code 0\n'.encode('utf-8')
        
    def run_cmd(self):
        choice=''
        print('==================== client mode ==================')
        while True:
            cmd=self.socket_api.recv(1024).decode('utf-8')
            if cmd=='':
                print('Disconnected')
                break
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
                if not choice=='a':
                    print('\ncommand: '+cmd)
                    choice=input('Do you wish to allow this command to run on your system\n(Y/y=yes N/n=no A/a=allow no confirmation ): ')
                    choice=choice[0].lower()
                if choice=='a' or choice=='y':
                    if re.search(r'^cd (.+)',cmd) or cmd=='cd':
                        print(cmd)
                        for match in re.finditer(r'^cd (.+)',cmd):
                            cmd=match.group(1)
                        
                        try:
                            os.chdir(cmd)
                            response='command executed with return code 0\n'.encode('utf-8')
                        except:
                            response=f'command executed with return code 127\nno directory with the name {cmd}\n'.encode('utf-8')
                        finally:
                            self.socket_api.send(response)
                    else:
                        print('\ncommand: '+cmd)
                        response=self.check_cmd(cmd)
                        response_str=response.decode('utf-8')
                        print(f'\n{response_str}')
                        print('='*30)
                        self.socket_api.send(response)
                else:
                    print(cmd+' (DENIED)')
                    self.socket_api.send('command Denied by client'.encode('utf-8'))
def main():
    id=input('Input id:')
    while(not re.match(r'^[1-9]{1}\d{3}$',id)):
        print('Invalid input please try agin')
        id=input('Input id:')
    ip=os.getenv('SERVER_IP')
    client_obj=client(ip)
    if client_obj.connect(id):
        client_obj.run_cmd()
    else:
        print('Disconnected')
if __name__=='__main__':
    main()
