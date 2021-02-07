import socket,time
import os,argparse
import select

class Host:
    def __init__(self,ip):
        self.ip=ip


    def connect(self):
        socket_obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_obj.connect((self.ip,8890))
        socket_obj.send('host'.encode('utf-8'))
        self.socket_api=socket_obj

        user_tag=self.socket_api.recv(30).decode('utf-8')
        id,timeout=user_tag.split(':')

        print('Your id is',id)
        print(f'Id will expire in {timeout} if connection is not formed with client')
        return self.socket_api.recv(30).decode('utf-8')
        

    def send_cmd(self,command):
        output=''

        #sets a long value for timeout to wait for client authentication
        #except for exit which requires no authentication
        if command!='exit':
            timeout=99*100
        else:
            timeout=2

        command=command.encode('utf-8')
        self.socket_api.sendall(command)

        while True:
            response,_,_=select.select([self.socket_api],[],[],timeout)
            if response:
                out=self.socket_api.recv(2048).decode('utf-8')

                if out=='':
                    break

                output+=out
                #resets timeout once client authentication has been made
                timeout=1
            else:
                break

        return output


    #request for current location
    @property
    def current_loc(self):
        return self.send_cmd('pwd?ps1')


    def display_term(self):
        print('=================== Host Mode ===================')

        while True:
            #gives a short period to allow client get ready for command
            time.sleep(0.4)
            cwd=self.current_loc

            if not cwd=='':
                cmd=input(cwd+'> ')

                while(not cmd):
                    print('you need to enter a command')
                    cmd=input(cwd+'> ')

                response=self.send_cmd(cmd)
                if response=='':
                    print('Disconnected')
                    break

                print(response)

                if cmd=='exit':
                    self.socket_api.close()
                    print('Disconnected')
                    break
            else:
                print('Disconnected')
                break
            

#Replace with your own ip
ip=str(os.getenv('SERVER_IP'))
host=Host(ip)
#returns empty string if server is shutdown or id timesout
status=host.connect()

if status:
    host.display_term()
else:
    print('Disconnected')



