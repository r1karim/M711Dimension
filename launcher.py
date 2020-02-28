'''
	M711Dimension - Launcher
	Author: adri711
	Language: Python
'''

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
		self.type = ''
		self.isSelected = False
		widget.widgets.append(self)

class Button(widget):
	def __init__(self,ID,x,y,width, height, text,color,hovercolor=None):
		super().__init__(ID,x,y,width,height)
		self.text = text
		self.color = color
		self.type = 'button'
		self.hovercolor = hovercolor

class Textarea(widget):
	def __init__(self,ID,x,y,width, height, pholder,maxlen,txtcolor, bgcolor,hovercolor=None):
		super().__init__(ID,x,y,width,height)
		self.placeholder = pholder
		self.maxlength = maxlen
		self.textcolor = txtcolor
		self.color = bgcolor
		self.text = ''
		self.type = 'textarea'
		self.hovercolor = hovercolor

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
txt = Textarea('username_input',100,10,100,25,'username',24,BLACK, BLUE)

def RefreshList():
	global servers
	try:
		s.sendto(bytes_, (MASTER_LIST_IP, MASTER_LIST_PORT))
		_bytes_,addr = s.recvfrom(3064)
		servers = pickle.loads(_bytes_)
	except:
		print('ERROR: Could not contact the master server.')

def gameloop():
	playButton = Button('play_button', 30 + SCREEN_WIDTH-200,10, 100,25, 'Play',GREEN,BLACK)
	refreshButton = Button('refresh_button', 30 + SCREEN_WIDTH-200,40, 100,25, 'Refresh',GREEN,BLACK)

	while True:
		surface.fill(GREY)
		x,y = pygame.mouse.get_pos()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONUP:
				for wdgt in widget.widgets:
					if wdgt.type == 'button':
						if x >= wdgt.x and x <= wdgt.x + wdgt.width and y >= wdgt.y and y <= wdgt.y+wdgt.height:
							if wdgt.id == 'play_button':
								pass
							elif wdgt.text == 'refresh_button':
								time.sleep(1)
								RefreshList()
					elif wdgt.type == 'textarea':
						if x >= wdgt.x and x <= wdgt.x+wdgt.width and y >= wdgt.y and y <= wdgt.y + wdgt.height:
							wdgt.isSelected = True
						else:
							wdgt.isSelected = False
		pygame.draw.rect(surface, LIGHTBLUE, (10,40, SCREEN_WIDTH-200, 25))
		ptext.draw('hostname\tplayers', (12,42), fontsize=25)
		for wdgt in widget.widgets:
			if wdgt.type == 'button':
				if wdgt.hovercolor is None:
					pygame.draw.rect(surface, wdgt.color, (wdgt.x,wdgt.y, wdgt.width, wdgt.height))
				else:
					if x >= wdgt.x and x <= wdgt.x+wdgt.width and y >= wdgt.y and y <= wdgt.y + wdgt.height:
						pygame.draw.rect(surface, wdgt.hovercolor, (wdgt.x,wdgt.y, wdgt.width, wdgt.height))
					else:
						pygame.draw.rect(surface, wdgt.color, (wdgt.x,wdgt.y, wdgt.width, wdgt.height))
				ptext.draw(wdgt.text, (wdgt.x+int(wdgt.width/4), wdgt.y+ int(wdgt.height / 4)))
			elif wdgt.type == 'textarea':
				pygame.draw.rect(surface, wdgt.color, (wdgt.x, wdgt.y, wdgt.width, wdgt.height))
				ptext.draw(wdgt.text, (wdgt.x + int(wdgt.width/4), wdgt.y + int(wdgt.height/4)))
				if not wdgt.isSelected:
					ptext.draw(wdgt.placeholder, (wdgt.x + int(wdgt.width/5), wdgt.y + int(wdgt.height/4)), color=GREEN, fontsize=20)
				else:
					pass
		for srv in servers:
			serverid = servers.index(srv) + 1
			pygame.draw.rect(surface, LIGHTBLUE, (10,40 + (serverid*30),SCREEN_WIDTH-200,25))
			ptext.draw(srv['hostname']+'\t0/'+str(srv['maxplayers']), (14, 44 + (serverid*30)), fontsize=20)

		pygame.display.update()
		pygame.time.Clock().tick(FPS)
if __name__ == '__main__':
	RefreshList()
	gameloop()