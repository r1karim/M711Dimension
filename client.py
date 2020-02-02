import pygame,sys
import socket
from random import*
from threading import Thread
import pickle

#COLORS:
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (10,150,10)
RED = (150,10,10)
BLUE = (10,10,150)

#Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
#
name = "user" + str(randint(0, 10000) + randint(0, 100))
X, Y = 0.0, 0.0
Health = 100.0

players = []

#Connection to the server.
IP = '127.0.0.1'
PORT = 8545
s = socket.socket()
s.settimeout(1)
s.connect((IP, PORT))
print("Connected to the server.")
s.send(name.encode('UTF-8'))

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("M711Platform")

def gameLoop():
    while True:
        surface.fill(GREEN)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RIGHT):
                    #print("meow")
                    s.send('A'.encode('UTF-8'))
                elif(event.key == pygame.K_LEFT):
                    s.send('B'.encode('UTF-8'))
                elif(event.key == pygame.K_UP):
                    s.send('D'.encode('UTF-8'))
                elif(event.key == pygame.K_DOWN):
                    s.send('C'.encode('UTF-8'))
        for player in players:
            pygame.draw.rect(surface, WHITE, (player['X'], player['Y'], 50,50))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
def recvMessages():
    global players
    while True:
        try:
            message = s.recv(1000)
            temp = ''
            try:
                temp = message.decode('UTF-8')
            except:
                temp = pickle.loads(message)
                players=temp
            if(temp[0] == 'F'):
                temp = message.decode('UTF-8')
                print(temp[1:])
        except:
            pass
ServerCommunicator = Thread(target=recvMessages)
ServerCommunicator.start()
gameLoop()
