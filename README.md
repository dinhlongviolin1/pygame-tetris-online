# pygame-tetris-online
Tetris multiplayer online mode using Python socket and threading

## Requirement to use this app
* Have python 3.x installed (socket, threading is built into Python)
* Have pygame installed

## How to run this app? 
1. On your computer
* Get your private IP address (local machine IP address)
* Go to server.py and client.py and change `SERVER` to your private IP address
* Run server.py
* Run instances of client.py

2. On server
* Get your server private and public IP address
* Go to server.py and change `SERVER` to your private IP address
* Go to client.py and change `SERVER` to your public IP address
* Run server.py on server
* Run instances of client.py on your computer
