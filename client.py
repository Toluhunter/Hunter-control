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
    def check_cmd(self):
        pass
    def run_cmd(self):
        print('==================== client mode ==================')
        while True:
            cmd=self.socket_api.recv(1024).decode('utf-8')
            if cmd=='':
                print('Disconnected')
                break
            print('\ncommand: '+cmd)
def main():
    id=input('Input id:')
    while(not re.match(r'^[1-9]{1}\d{3}$',id)):
        print('Invalid input please try agin')
        id=input('Input id:')
    ip=os.getenv('SERVER_IP')
    client_obj=client('localhost')
    if client_obj.connect(id):
        client_obj.run_cmd()
    else:
        print('Disconnected')
if __name__=='__main__':
    main()
