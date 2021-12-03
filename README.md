# Hunter control
**Version Beta 1.1**

A Terminal program to allow users connect to remote clients 

---
A Terminal based program to allow multiple users and clients connect seamlessly, and have multiple independent sessions which allow the trade of commands and responses across a remote network, the server IP is to be provided by the the user, team, organization e.t.c.

# How It Works
Hunter Control is split into four main parts the server side, connectionhandler, client side and user/host side,  each side is designed to take part in a full session connection

Server Side: The server.py file is meant to be run on the users server which should have a public Ip address to allow for both the host and the client to form a connection with, this part of the program provides the host with a randomly generated user id, the program will then proceed to wait for 1 minute for the client to join, should the time elapse the the connection to the host will be closed and the user id voided , should a client connect providing the host user id the client will be paired together with the host(owner of the provided valid id) and then moved to the connection handler to manage their session

ConnectionHAndler: The fucntion of this file is to create a thread for each successful connection between host and client to allow exchange of data while the main program continues to accept new connections

Host: This is the file that is to be run by the user this will provide them a user id which should be told to the client to allow the client to be paired with the host once done the host will be provided with a shell like interface to input commands which will be sent to the client, they can either be rejected or allowed by the client outputs will be forwarded back to the host 

Client: This is the file that will be run the client, they will be prompted for a host user id which upon input will pair the client to the repective host, the client has the right to accept or reject any command sent to them

# Author

Toluhunter https://www.linkedin.com/in/tolulope-fakoya-775550224/

# License & Copyright
This program is licensed under the <a href="https://github.com/Toluhunter/Hunter-control/blob/main/LICENSE">BSD-2-Clause License</a>. Please note other third party frameworks may be licensed under different licenses

Copyright Ⓒ 2021 Toluhunter
