import socket,time
import os,argparse

class Host:
    def __init__(self,ip):
        self.ip=ip
    def connect(self):
        socket_obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_obj.connect((self.ip,8890))
        time.sleep(0.5)
        socket_obj.send('host'.encode())
        self.socket_api=socket_obj
        id=self.socket_api.recv(12).decode('utf-8')
        print('Your id is',id)
        self.socket_api.recv(30)
        

    def send_cmd(self,command):
        command=command.encode('utf-8')
        time.sleep(0.5)
        self.socket_api.send(command)
        output=self.socket_api.recv(2048).decode('utf-8')
        return output
        
    @property
    def current_loc(self):
        return self.send_cmd('pwd?ps1')

    def display_term(self):
        print('=================== Host Mode ===================')
        while True:
            time.sleep(0.4)
            cwd=self.current_loc
            if not cwd=='':
                cmd=input(cwd+'> ')
                response=self.send_cmd(cmd)
                if response=='':
                    print('Disconnected')
                    break
                print(response)
            else:
                print('Disconnected')
                break
            
ap=argparse.ArgumentParser(prog='Hunter-control',description='A command line rdp for terminal')
ap.parse_args()

#Replace with your own ip
ip=str(os.getenv('SERVER_IP'))

host=Host('localhost')
host.connect()
host.display_term()



