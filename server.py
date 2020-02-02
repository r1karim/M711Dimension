import socket
from threading import Thread
import pickle
import time

print("Launching the server...")

class Player:
    def __init__(self, ID,NAME, IP, HEALTH, X,Y):
        self.id = ID
        self.name = NAME
        self.ip = IP
        self.Health = HEALTH
        self.x = X
        self.y = Y
    def GetPlayerPosition(self):
        return self.x,self.y
    def GetPlayerName(self):
        return self.name
    def GetPlayerHealth(self):
        return self.Health
    def GetPlayerIp(self):
        return self.ip
    def printInformation(self):
        print("Name: " + self.name + " IP: " + str(self.ip) + " Health: " + str(self.Health) + " X: " +str(self.x) +" Y: "+str(self.y))
clients = []

IP = '127.0.0.1'
PORT = 8545
s = socket.socket()
s.bind((IP,PORT))
s.listen(50)
s.settimeout(0.0001)
def UpdatePlayers():
    players = []
    for client in clients:
        playerDict = {'name': client.name, 'X': client.x, 'Y':client.y}
        players.append(playerDict)
    for e in clients:
        obj = pickle.dumps(players)
        print('pickled')
        #message = 'E'.encode('UTF-8')
        #message = message + obj
        e.id.send(obj)
        print('sent.')
        e.printInformation()

def HandleConnections():
    while True:
        try:
            client, address = s.accept()
            client.setblocking(0)
            name = client.recv(500)
            player = Player(client, name.decode('UTF-8'), address, 100.0, 0, 0)
            player.printInformation()
            clients.append(player)
            message = 'F'+player.name + " has joined the game."
            print(player.name + " has connected. IP: " + str(player.ip))
            for c in clients:
                c.id.send(message.encode('UTF-8'))
            time.sleep(2)
            UpdatePlayers()
        except:
            pass
def CommunicateWithPlayers():
    while True:
        try:
            for c in clients:
                m = c.id.recv(1)
                m = m.decode("UTF-8")
                if(m[0] == 'A'):
                    c.x+=5 #right
                    UpdatePlayers()
                elif(m[0] == 'B'):
                    c.x-=5 #left
                    UpdatePlayers()
                elif(m[0] == 'C'):
                    c.y+=5 #down
                    UpdatePlayers()
                elif(m[0] == 'D'):
                    c.y-=5 #up
                    UpdatePlayers()
        except:
            pass
ConnectionHandler = Thread(target=HandleConnections)
PlayerMovementHandler = Thread(target=CommunicateWithPlayers)
ConnectionHandler.start()
PlayerMovementHandler.start()
print("Server has started.")