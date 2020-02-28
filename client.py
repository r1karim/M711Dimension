'''
    M711Dimension - Client
    Author: adri711
    Language: Python
'''

import pygame,sys
import socket
from random import*
from threading import Thread
import pickle
from Libraries import GUI_TextEntry as Ti
from Libraries import ptext
import time

class spritesheet:
    def __init__(self, filename, cols, rows):
        self.sheet = pygame.image.load(filename).convert_alpha()
        
        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows
        
        self.rect = self.sheet.get_rect()
        w = self.cellWidth = int(self.rect.width / cols)
        h = self.cellHeight = int(self.rect.height / rows)
        hw, hh = self.cellCenter = (int(w / 2), int(h / 2))
        
        self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])
        self.handle = list([
            (0, 0), (-hw, 0), (-w, 0),
            (0, -hh), (-hw, -hh), (-w, -hh),
            (0, -h), (-hw, -h), (-w, -h),])
        
    def draw(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.cells[cellIndex])

#
SOUTH = 0
WEST = 1
NORTH = 2
EAST = 3

NORMAL = 0
TEXTCHAT = 1
PLAYERSLIST = 2
gameState = NORMAL

#COLORS:
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (10,150,10)
RED = (150,10,10)
BLUE = (10,10,150)
TEST = (0,0,0,100)
#Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
#
name = "player" + str(randint(0, 10000) + randint(0, 100))
X, Y = 0.0, 0.0
Health = 100.0

players = []
checkpoints = []

chatLog = "Welcome to M711Dimension!\n"

dialog = {
    'Title': '', 
    'Content': '', 
    'Width':0, 
    'Height':0,
    'Button1': {
        'value': '',
        'Width': 0,
        'Height': 0,
        'PosX': -1,
        'PosY': -1,
    },
    'Button2': {
        'value': '',
        'Width': 0,
        'Height': 0,
        'posX': -1,
        'posY': -1,
    },
    'switch':False
}

#Connection to the server.
IP = '127.0.0.1'
PORT = 5241
s = socket.socket()
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
s.settimeout(1)
s.connect((IP, PORT))
print("Connected to the server.")
s.send(name.encode('UTF-8'))

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 8)
textChatFont = pygame.font.SysFont('Arial',15)
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Transparent_Surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
surface.blit(Transparent_Surface, (0,0))
pygame.display.set_caption("M711Dimension")

playerSheet = spritesheet("george.png", 4,4)
terrain = spritesheet("PathAndObjects.png", 6,6)
textinput = Ti.TextInput("", "none",20,True,WHITE,WHITE)

def gameLoop():
    global gameState
    while True:
        surface.fill(GREEN)
        events = pygame.event.get()
        for event in events:
            if(event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if(dialog['switch']):
                    if(dialog['Button2']['value'] == ''):
                        if(dialog['Button1']['PosX'] <= x and dialog['Button1']['PosX']+dialog['Button1']['Width'] >= x):
                            if(dialog['Button1']['PosY'] <= y and dialog['Button1']['PosY']+dialog['Button1']['Height'] >= y):
                                pass
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RIGHT):
                    s.send('A'.encode('UTF-8'))
                elif(event.key == pygame.K_LEFT):
                    s.send('B'.encode('UTF-8'))
                elif(event.key == pygame.K_UP):
                    s.send('D'.encode('UTF-8'))
                elif(event.key == pygame.K_DOWN):
                    s.send('C'.encode('UTF-8'))
                elif(event.key == pygame.K_t):
                    if(gameState == NORMAL):
                        gameState = TEXTCHAT
                        time.sleep(0.3)
                        textinput.input_string  = ""
                elif(event.key==pygame.K_TAB):
                    if(gameState == NORMAL or gameState == TEXTCHAT):
                        gameState = PLAYERSLIST

                elif(event.key == pygame.K_RETURN):
                    if(gameState == TEXTCHAT):
                        gameState = NORMAL
                        msg = textinput.get_text()
                        print(msg)
                        msg = 'E'+msg
                        msg = msg.encode('UTF-8')
                        textinput.input_string  = ''
                        s.send(msg)
            elif(event.type == pygame.KEYUP):
                if(event.key == pygame.K_TAB):
                    gameState = NORMAL
        Transparent_Surface.fill((200, 200, 200, 10))

        for checkpoint in checkpoints:
            pygame.draw.circle(Transparent_Surface, (150,10,10,150), (100,200),20)
        
        if(dialog['switch']):
            pygame.draw.rect(surface, BLACK, (int((SCREEN_WIDTH/2)-(dialog['Width']/2)),int((SCREEN_HEIGHT/2)-(dialog['Height']/2)), dialog['Width'], dialog['Height']))
            pygame.draw.rect(surface, BLUE, (int((SCREEN_WIDTH/2)-(dialog['Width']/2)),int((SCREEN_HEIGHT/2)-(dialog['Height']/2)), dialog['Width'], 20))
            ptext.draw(dialog['Title'], (int((SCREEN_WIDTH/2)-(dialog['Width']/2)),int((SCREEN_HEIGHT/2)-(dialog['Height']/2)+3)), color=BLACK)
            ptext.draw(dialog['Content'], (int((SCREEN_WIDTH/2)-(dialog['Width']/2)),int((SCREEN_HEIGHT/2)-(dialog['Height']/2)+23)), color=WHITE, fontsize=20)
            if(dialog['Button2']['value'] == ''):
                pygame.draw.rect(surface, BLUE, (dialog['Button1']['PosX'],dialog['Button1']['PosY'], dialog['Button1']['Width'],dialog['Button1']['Height']))
                ptext.draw(dialog['Button1']['value'],(int((SCREEN_WIDTH/2) - int(dialog['Button1']['Width']/2)),int((SCREEN_HEIGHT/2)+(dialog['Height']/2)-27)), color=WHITE)

        for player in players:
            if(player['D'] == SOUTH):
                playerSheet.draw(surface,0,player['X'], player['Y'])
            elif(player['D'] == WEST):
                playerSheet.draw(surface,1,player['X'], player['Y'])
            elif(player['D'] == EAST):
                playerSheet.draw(surface,3,player['X'], player['Y'])
            elif(player['D'] == NORTH):
                playerSheet.draw(surface,2,player['X'], player['Y'])
            pygame.draw.rect(surface, BLACK, (player['X'], player['Y']-10, 50,9))
            pygame.draw.rect(surface, RED, (player['X'], player['Y']-10, int(player['H']/2),9))
            textsurface = myfont.render(player['name'], False, WHITE)
            surface.blit(textsurface,(player['X'], player['Y']-10))
        if(gameState == TEXTCHAT):
            pygame.draw.rect(surface, BLACK, (10,10, SCREEN_WIDTH-20, 25))
            textinput.update(events)
            surface.blit(textinput.get_surface(), (10, 10))
        elif(gameState == PLAYERSLIST):
            BOX_WIDTH = 200
            BOX_HEIGHT = 300
            pygame.draw.rect(surface, TEST,(int((SCREEN_WIDTH/2)-(BOX_WIDTH/2)), int((SCREEN_HEIGHT/2)-(BOX_HEIGHT/2)), BOX_WIDTH,BOX_HEIGHT))
            playerlisttext = "id\tname\tScore\n"
            for player in players:
                playerlisttext+=str(player['id'])+'\t'+player['name']+'\t'+str(player['S'])+'\n'
            ptext.draw(playerlisttext,((SCREEN_WIDTH/2)-(BOX_WIDTH/2), (SCREEN_HEIGHT/2)-(BOX_HEIGHT/2)), color=WHITE)
        ptext.draw(chatLog,(10,SCREEN_HEIGHT-150), color=BLUE)
        surface.blit(Transparent_Surface, (0,0))
        pygame.display.update()
        pygame.time.Clock().tick(FPS)

def recvMessages():
    global chatLog
    global players
    while True:
        try:
            message = s.recv(1024)
            try:
                message = message.decode('UTF-8')
                print(message)
                objectstart = []
                objectend = []
                for i in range(len(message)):
                    if(message[i] == '$'):
                        objectstart.append(i)
                    elif(message[i] == '£'):
                        objectend.append(i)
                for i in range(len(objectstart)):
                    message_type = message[objectstart[i]+1]
                    fullmessage = message[objectstart[i]+2:objectend[i]]
                    if(message_type == 'F'):
                        chatLog += fullmessage + '\n'
                    elif(message_type == 'W'):
                        print("Received a dialog")
                        dialog_type = fullmessage[0]
                        dialog_id = fullmessage[1]
                        x = []
                        for i in range(len(fullmessage)):
                            if(fullmessage[i] == '語'):
                                x.append(i)
                                continue
                        dialog_title = fullmessage[2:x[0]]
                        dialog_content = fullmessage[x[0]+1:x[1]]
                        dialog_button1 = fullmessage[x[1]+1:x[2]]
                        dialog_button2 = fullmessage[x[2]+1:]
                        print(f"Dialog type: {dialog_type}")
                        print(f"Dialog title: {dialog_title}")
                        print(f"Dialog ID: {dialog_id}")
                        print(f"Dialog content: {dialog_content}")
                        print(f"dialog button1: {dialog_button1}")
                        print(f"dialog button2: {dialog_button2}")
                        lines = []
                        characters = 0
                        print("test")
                        dialog['Title'] = dialog_title
                        dialog['Content'] = dialog_content
                        dialog['switch'] = True
                        dialog['Button1']['value'] = dialog_button1
                        dialog['Button1']['Width'] = len(dialog['Button1']['value']) * 10 + 2
                        dialog['Button1']['PosX'] = int((SCREEN_WIDTH/2) - int(dialog['Button1']['Width']/2))
                        dialog['Button1']['PosY'] = int((SCREEN_HEIGHT/2)+(dialog['Height']/2) +20)
                        dialog['Button1']['Height'] = 20
                        dialog['Button2']['value'] = dialog_button2
                        for i in range(len(dialog_content)):
                            if(i < len(dialog_content)-1):
                                ch = dialog_content[i]+dialog_content[i+1]
                            else:
                                ch='__'
                            if (ch == 't\n'):
                                lines.append(characters)
                                characters = 0
                            else:
                                characters += 1
                        lines.append(characters)
                        dialog['Height'] = (len(lines) * 10) + 90
                        lines.sort(reverse = True)
                        dialog['Width'] = lines[0]*10
            except:
                temp = pickle.loads(message)
                plist = [] #playerlist
                cplist = []
                for t in temp:
                    if(t['type']=='player'):
                        plist.append(t)
                    elif(t['type']=='checkpoint'):
                        cplist.append(t)
                players = plist

        except:
            pass
if(__name__=='__main__'): 
    ServerCommunicator = Thread(target=recvMessages)
    ServerCommunicator.start()
    gameLoop()