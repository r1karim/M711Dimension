import socket
from threading import Thread
import pickle
import time
import math
from configparser import ConfigParser
import lupa

print("Launching the server...")

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
    sp=config.get("main", "port")
    smp=config.get("main", "maxplayers")
    srp=config.get("main", "rconpassword")
    sps=config.get("main","password")
    sgm=config.get("main","gamemode")
except:
    print("Config file doesn't exist or lacks keys.")
    quit()

#
SOUTH = 0
WEST = 1
NORTH = 2
EAST = 3

def GetTheDistanceBetweenTwoPoints(x,y,x1,y1):
    a = (x - x1)**2
    b = (y - y1)**2
    R = math.sqrt(a + b)
    return R


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
    def IsInRangeOfPoint(self, range, x,y):
        R=GetTheDistanceBetweenTwoPoints(self.x, self.y, x,y)
        if(R <= range):
            return True
        else:
            return False
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
        playerDict = {'type': 'player','name': client.name, 'X': client.x, 'Y':client.y, 'H':client.Health, 'S':client.score, 'D': client.direction}
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
            lua.eval("OnPlayerConnect()")
            time.sleep(1.2)
            UpdatePlayers()
        except:
            pass

if(__name__=='__main__'):
    ConnectionHandler = Thread(target=HandleConnections)
    ConnectionHandler.start()
server = Server(shs,sgm,sl,sp,smp,srp,sps)

lua.execute(open(server.gamemode,'r').read())