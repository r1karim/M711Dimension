import pygame,sys
import socket
import pickle
from Libraries import ptext
import time

class widget:
	widgets = []
	def __init__(self, ID,x,y,width, height):
		self.id = ID
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		widget.widgets.append(self)

class Button(widget):
	def __init__(self, text, x,y,width,height, color):
		self.text = text
		self.color = color

class Textarea(widget):
	def __init__(self,x,y,width,height,maxlen,txtcolor, bgcolor, pholder):
		self.maxlength = maxlen
		self.textcolor = txtcolor
		self.color = bgcolor
		self.text = ''
		self.placeholder = pholder
		
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (52, 235, 101)
RED = (150,10,10)
BLUE = (10,10,150)
LIGHTBLUE = (3, 127, 252)
GREY = (54, 54, 59)

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 450
FPS = 30

pygame.init()
pygame.font.init()
pygame.display.set_caption("M711Dimension - Launcher")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

MASTER_LIST_IP = '127.0.0.1'
MASTER_LIST_PORT = 65034

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 60310))
bytes_ = '$__J711__$_4EVA'.encode('UTF-8')
servers = []
txt = Textarea(100,10,100,25,24,BLACK, BLUE, 'Username')

def RefreshList():
	global servers
	try:
		s.sendto(bytes_, (MASTER_LIST_IP, MASTER_LIST_PORT))
		_bytes_,addr = s.recvfrom(3064)
		servers = pickle.loads(_bytes_)
	except:
		print('ERROR: Could not contact the master server.')

def gameloop():
	playButton = Button('Play', 30 + SCREEN_WIDTH-200,10, 100,25, GREEN)
	refreshButton = Button('Refresh',30 + SCREEN_WIDTH-200,40, 100,25, GREEN)

	while True:
		surface.fill(GREY)
		events = pygame.event.get()
		for event in events:
			if(event.type == pygame.QUIT):
				pygame.quit()
			elif(event.type == pygame.MOUSEBUTTONUP):
				x,y = pygame.mouse.get_pos()
				for btn in Button.widgets:
					if x >= btn.x and x <= btn.x + btn.width and y >= btn.y and y <= btn.y+btn.height:
						if btn.text == 'Play':
							pass
						elif btn.text == 'Refresh':
							time.sleep(1)
							RefreshList()
				for txtar in Textarea.widgets:
					if x >= txtar.x and x <= txtar.x+txtar.width and y >= txtar.y and y <= txtar.y + txtar.height:
						txtar.isSelected = True
		pygame.draw.rect(surface, LIGHTBLUE, (10,40, SCREEN_WIDTH-200, 25))
		ptext.draw('hostname\tplayers', (12,42), fontsize=25)
		for btn in Button.widgets:
			pygame.draw.rect(surface, btn.color, (btn.x,btn.y, btn.width, btn.height))
			ptext.draw(btn.text, (btn.x+int(btn.width/4), btn.y+ int(btn.height / 4)))
		for txtar in Textarea.widgets:
			pygame.draw.rect(surface, txtar.color, (txtar.x, txtar.y, txtar.width, txtar.height))
			ptext.draw(txtar.text, (txtar.x + int(txtar.width/4), txtar.y + int(txtar.height/4)))
			if(txtar.isSelected == False):
				ptext.draw(txtar.placeholder, (txtar.x + int(txtar.width/5), txtar.y + int(txtar.height/4)), color=GREEN, fontsize=20)
		for srv in servers:
			serverid = servers.index(srv) + 1
			pygame.draw.rect(surface, LIGHTBLUE, (10,40 + (serverid*30),SCREEN_WIDTH-200,25))
			ptext.draw(srv['hostname']+'\t0/'+str(srv['maxplayers']), (14, 44 + (serverid*30)), fontsize=20)
		pygame.display.update()
		pygame.time.Clock().tick(FPS)
if __name__ == '__main__':
	RefreshList()
	gameloop()