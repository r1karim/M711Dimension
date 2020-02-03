import socket
from threading import Thread
import pickle
import time

print("Launching the server...")

#
SOUTH = 0
WEST = 1
NORTH = 2
EAST = 3

class Player:
    def __init__(self, ID,NAME, IP, HEALTH, X,Y):
        self.id = ID
        self.name = NAME
        self.ip = IP
        self.Health = HEALTH
        self.x = X
        self.y = Y
        self.score = 0
        self.direction = SOUTH
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
clients = []

IP = '127.0.0.1'
PORT = 8545
s = socket.socket()
s.bind((IP,PORT))
s.listen(50)
s.settimeout(0.0001)

def SendAllPlayersMessage(message):
    for client in clients:
        client.id.send(message.encode('UTF-8'))

def CommunicateWithPlayer(__client__):
    while True:
        try:
            m = __client__.id.recv(1024)
            m = m.decode("UTF-8")
            if(m[0] == 'A'):
                __client__.x+=5 #right
                __client__.direction = EAST
                UpdatePlayers()

            elif(m[0] == 'B'):
                __client__.x-=5 #left
                __client__.direction = WEST
                UpdatePlayers()

            elif(m[0] == 'C'):
                __client__.y+=5 #down
                __client__.direction = SOUTH
                UpdatePlayers()

            elif(m[0] == 'D'):
                __client__.y-=5 #up
                __client__.direction = NORTH
                UpdatePlayers()

            elif(m[0] == 'E'):
                if('/damage' in m[1:8]):
                    __client__.Health-=25
                    UpdatePlayers()

                    pMessage = "F\n"+__client__.name+" has been hurt."
                    time.sleep(0.1)
                    SendAllPlayersMessage(pMessage)
                    print('meeeeeeow')
                else:
                    pMessage = "F\n"+__client__.name+": "+m[1:]
                    SendAllPlayersMessage(pMessage)
                    print(pMessage)

        except:
            pass
def UpdatePlayers():
    players = []
    for client in clients:
        playerDict = {'name': client.name, 'X': client.x, 'Y':client.y, 'H':client.Health, 'S':client.score, 'D': client.direction}
        players.append(playerDict)
    for e in clients:
        obj = pickle.dumps(players)
        e.id.send(obj)
def HandleConnections():
    while True:
        try:
            client, address = s.accept()
            client.setblocking(0)
            name = client.recv(500)
            player = Player(client, name.decode('UTF-8'), address, 100.0, 0, 0)
            player.printInformation()
            clients.append(player)
            thread = Thread(target=CommunicateWithPlayer, args=[player])
            thread.start()
            message = 'F\n'+player.name + " has joined the game."
            print(player.name + " has connected. IP: " + str(player.ip))
            SendAllPlayersMessage(message)
            time.sleep(2)
            UpdatePlayers()
        except:
            pass

if(__name__=='__main__'):
    ConnectionHandler = Thread(target=HandleConnections)
    ConnectionHandler.start()
    print("Server has started.")