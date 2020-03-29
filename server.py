'''
    M711Dimension - Server
    Author: adri711
    Language: Python
'''

import socket
from threading import Thread
import pickle
import time
import math
from configparser import ConfigParser
import lupa
from datetime import datetime
import os



def printt(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('['+current_time+']', message)

printt("Launching the server...")

class Server:
    def __init__(self, hostname,gamemode, language, port, maxplayers, rconpassword, password):
        self.hostname = hostname
        self.gamemode = gamemode
        self.language = language
        self.port = port
        self.maxplayers = maxplayers
        self.rconpassword = rconpassword
        self.password = password
        print(f"{self.hostname} has been successfuly launched on {port} with {maxplayers} max player count.")

lua = lupa.LuaRuntime(unpack_returned_tuples=True)
config = ConfigParser()

try:
    config.read('server_config.ini')
    shs=config.get("main", "hostname")
    sl=config.get("main", "language")
    sp=int(config.get("main", "port"))
    smp=int(config.get("main", "maxplayers"))
    srp=config.get("main", "rconpassword")
    sps=config.get("main","password")
    sgm=config.get("main","gamemode")
except:
    print("Config file doesn't exist or lacks keys.")
    os._exit(0)

#
SOUTH = 0
WEST = 1
NORTH = 2
EAST = 3

def GetTheDistanceBetweenTwoPoints(x,y,x1,y1):
    return math.sqrt(((x-x1)**2)+((y-y1)**2))

class Player:
    def __init__(self, ID,IDINT,NAME, IP, HEALTH, X,Y,team,skin):
        self.id = ID
        self.idint = IDINT
        self.name = NAME
        self.ip = IP
        self.Health = HEALTH
        self.x = X
        self.y = Y
        self.score = 0
        self.direction = SOUTH
        self.team = team
        self.skin = skin
        self.admin = False
    def GetPlayerPosition(self):
        return self.x,self.y
    def GetPlayerName(self):
        return self.name
    def GetPlayerHealth(self):
        return self.Health
    def GetPlayerIp(self):
        return self.ip
    def GetPlayerScore(self):
        return self.score
    def printInformation(self):
        print("Name: " + self.name + " IP: " + str(self.ip) + " Health: " + str(self.Health) + " X: " +str(self.x) +" Y: "+str(self.y))
    def IsInRangeOfPoint(self, range, x,y):
        R=GetTheDistanceBetweenTwoPoints(self.x, self.y, x,y)
        if(R <= range):
            return True
        else:
            return False

MASTER_LIST_IP = '127.0.0.1'
MASTER_LIST_PORT = 65034

clients = []

IP = '127.0.0.1'
PORT = sp
s = socket.socket()
s.bind(('',PORT))
s.listen(50)
s.settimeout(1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

server = Server(shs,sgm,sl,sp,smp,srp,sps)

UDP_SERVER = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_SERVER.bind((IP,PORT))


def CommunicateWithPlayer(user):
    while True:
        try:
            message = user.id.recv(1024).decode("UTF-8")
            Type = message[0]
            FullMessage = message[1:]
            if Type == 'A':
                user.x+=5 #right
                user.direction = EAST
            elif Type == 'B':
                user.x-=5
                user.direction = WEST
            elif Type == 'C':
                user.y+=5
                user.direction = SOUTH
            elif Type == 'D':
                user.y-=5
                user.direction = NORTH
            elif Type == 'E':
                result=lua.eval(f'OnPlayerText({user.idint}, {FullMessage})')
                if(result != -1):
                    pMessage = f'{user.name}: {FullMessage}'
                    SendAllPlayersMessage(pMessage)
                    print(pMessage)
            elif Type == 'G':
                temp = []
                for i in range(len(FullMessage)):
                    if FullMessage[i] == '£':
                        temp.append(i)
                dialog_id = FullMessage[temp[0]+1]
                dialog_response = FullMessage[temp[1]+1]
                lua.eval(f'OnDialogResponse({user.idint}, {dialog_id}, {dialog_response})')
            UpdatePlayers()
        except:
            pass

def UpdatePlayers():
    players = []
    for client in clients:
        playerDict = {'type': 'player', 'id':client.idint,'name': client.name, 'X': client.x, 'Y':client.y, 'H':client.Health, 'S':client.score, 'D': client.direction}
        players.append(playerDict)
    obj = pickle.dumps(players)
    for c in clients:
        c.id.send(obj)

def HandleConnections():
    while True:
        try:
            client, address = s.accept()
            client.setblocking(1)
            name = client.recv(620)
            for p in clients:
                if(p.name == name):
                    client.close()
                    break
            else:
                player = Player(client, len(clients),name.decode('UTF-8'), address, 100.0, 15, 15, 0,0)
                player.printInformation()
                clients.append(player)
                thread = Thread(target=CommunicateWithPlayer, args=[player])
                thread.start()
                print(player.name + " has connected. IP: " + str(player.ip))
                lua.eval(f"OnPlayerConnect({player.idint})")
                time.sleep(1.20)
                UpdatePlayers()
        except:
            pass
def masterlist():
    while True:
        _bytes_ = ('$'+server.hostname+'$'+server.gamemode+'$'+server.language+'$'+str(server.maxplayers))
        try:
            UDP_SERVER.sendto(_bytes_.encode('UTF-8'),(MASTER_LIST_IP,MASTER_LIST_PORT))
            time.sleep(1)
        except:
            pass

#SERVER FUNCTIONS
def SendAllPlayersMessage(message):
    message = f'$F{message}£'
    for client in clients:
        client.id.sendall(message.encode('UTF-8'))

def GetPlayerName(playerid):
    name = ''
    for client in clients:
        if(client.idint == playerid):
            name = client.name
            break
    return name

def SendPlayerMessage(playerid,message):
    message = f'$F{message}£'
    for client in clients:
        if(client.idint == playerid):
            client.id.sendall(message.encode('UTF-8'))
            break

def SetPlayerTeam(playerid, teamid):
    for client in clients:
        if(client.idint == playerid):
            client.team = teamid
            break

def SetPlayerSkin(playerid, skinid):
    for client in clients:
        if(client.idint == playerid):
            client.skin == skinid
            break

def SetPlayerAdmin(playerid, a):
    for client in clients:
        if(client.idint == playerid):
            client.admin = a #1 = is admin
            print(f'{client.name} is now a server administrator.')
            break

def KickPlayer(playerid):
    for client in clients:
        if(client.idint == playerid):
            client.id.close()
            clients.remove(client)
            break

def GetPlayerIp(playerid):
    ip = ''
    for client in clients:
        if(client.idint == playerid):
            ip = client.GetPlayerIp()
            break
    return ip

def ShowPlayerDialog(playerid, dialogid,type, title, content,button1,button2):
    time.sleep(0.1)
    for client in clients:
        if(client.idint == playerid):
            dialogcode = f"$W{type}{dialogid}{title}語{content}語{button1}語{button2}£"
            client.id.sendall(dialogcode.encode('UTF-8'))
            break

if(__name__=='__main__'):
    ConnectionHandler = Thread(target=HandleConnections)
    masterlistHandler = Thread(target=masterlist)
    ConnectionHandler.start()
    masterlistHandler.start()

lua.execute(open(server.gamemode,'r').read())