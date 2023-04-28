import os
import re
import time
import argparse
from sys import argv

from dotenv import load_dotenv

from utils.server import Server
from utils.host import Host
from utils.client import client

BASE_DIR = os.sep.join(__file__.split(os.sep)[:-1])
load_dotenv(os.path.join(BASE_DIR, ".env"))

parser = argparse.ArgumentParser(
    description='''
                    A Terminal based program to allow multiple users and clients connect seamlessly, 
                    and have multiple independent sessions which allow the trade of commands and responses 
                    across a remote network
                    ''',
    epilog='By Toluhunter')

parser.add_argument("--server", required=False, const=True,
                    action='store_const', help="Perform server connection handling")
parser.add_argument("--host", required=False, const=True,
                    action='store_const', help="Client mode")
parser.add_argument("--client", required=False, const=True,
                    action='store_const', help="Host mode")

if len(argv) != 2:
    parser.print_help()
    exit(-1)

args = parser.parse_args()

if args.server:
    server = Server()
    server.accept_conn()

if args.host:
    host = Host()
    if not host.check_network():
        exit(2)

    # Replace with your own ip
    ip = os.getenv('SERVER')
    if not ip:
        ip = input("Enter your ip address of the server: ")
    # returns empty string if server is shutdown or id timesout
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

if args.client:

    ip = os.getenv('SERVER')
    if not ip:
        ip = input("Enter your IP address: ")

    client_obj = client(ip)

    # Ends program if theres no internet connection
    if not client_obj.check_network():
        exit(2)

    id = input('Input id: ')

    while (not re.match(r'^[1-9]{1}\d{3}$', id)):
        print(f'{client_obj.RED}Invalid input please try agin {client_obj.RESET}')
        id = input('Input id: ')

    # Replace with your Server Ip
    status = client_obj.connect(id)

    if status:
        client_obj.display()
    else:
        print(f'{client_obj.RED}Disconnected {client_obj.RESET}')
