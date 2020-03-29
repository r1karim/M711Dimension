'''
	M711Dimension - Launcher
	Author: adri1
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
	def destroy(self):
		widget.widgets.remove(self)
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
GREEN2 = (118,191,115)
GREEN3 = (104,129,104)
RED = (150,10,10)
BLUE = (10,10,150)
LIGHTBLUE = (3, 127, 252)
LIGHTBLUE2 = (15, 160,255)
GREY = (54, 54, 59)
GREY2 = (32,32,32)

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 450
FPS = 500

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


def RefreshList():
	global servers
	try:
		s.sendto(bytes_, (MASTER_LIST_IP, MASTER_LIST_PORT))
		_bytes_,addr = s.recvfrom(3064)
		servers = pickle.loads(_bytes_)
		count = 0
		for btn in widget.widgets:
			if '$__J711__$_4EVA_SRV' in btn.id:
				try:
					btn.destroy()
				except:
					print('ERROR: Could not destroy UI elements.')
		print(widget.widgets)
		for srv in servers:
			serverid = servers.index(srv) + 1
			if count % 2 == 0:
				srvbtn = Button('$__J711__$_4EVA_SRV' + str(serverid),10,40 + (serverid*30),SCREEN_WIDTH-200,25, srv['hostname']+'\t0/'+str(srv['maxplayers']),LIGHTBLUE2,GREY)
			else:
				srvbtn = Button('$__J711__$_4EVA_SRV' + str(serverid),10,40 + (serverid*30),SCREEN_WIDTH-200,25, srv['hostname']+'\t0/'+str(srv['maxplayers']),LIGHTBLUE,GREY)
			count+=1
	except:
		print('ERROR: Could not contact the master server.')

def gameloop():
	global servercount
	playButton = Button('play_button', 30 + SCREEN_WIDTH-200,10, 100,25, 'Play',GREEN2,GREY)
	refreshButton = Button('refresh_button', 30 + SCREEN_WIDTH-200,40, 100,25, 'Refresh',GREEN2,GREY)
	txt = Textarea('username_input',100,10,150,25,'username',24,BLACK, GREEN2,GREY)

	while True:
		surface.fill(GREY2)
		x,y = pygame.mouse.get_pos()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONUP:
				for wdgt in widget.widgets:
					if wdgt.type == 'button':
						if x >= wdgt.x and x <= wdgt.x + wdgt.width and y >= wdgt.y and y <= wdgt.y+wdgt.height:
							if wdgt.id == 'play_button':
								pass
							elif wdgt.id == 'refresh_button':
								print('Refreshing list..')
								time.sleep(0.5)
								RefreshList()
							elif '$__J711__$_4EVA_SRV' in wdgt.id:
								print('Clicked on as server button')
					elif wdgt.type == 'textarea':
						if x >= wdgt.x and x <= wdgt.x+wdgt.width and y >= wdgt.y and y <= wdgt.y + wdgt.height:
							wdgt.isSelected = True
						else:
							wdgt.isSelected = False
		pygame.draw.rect(surface, LIGHTBLUE, (10,40, SCREEN_WIDTH-200, 25))
		ptext.draw('hostname\tplayers', (12,42), fontsize=25)
		for wdgt in widget.widgets:
			if wdgt.hovercolor is None:
				pygame.draw.rect(surface, wdgt.color, (wdgt.x,wdgt.y, wdgt.width, wdgt.height))
			else:
				if x >= wdgt.x and x <= wdgt.x+wdgt.width and y >= wdgt.y and y <= wdgt.y + wdgt.height:
					pygame.draw.rect(surface, wdgt.hovercolor, (wdgt.x,wdgt.y, wdgt.width, wdgt.height))
				else:
					pygame.draw.rect(surface, wdgt.color, (wdgt.x,wdgt.y, wdgt.width, wdgt.height))

			if wdgt.type == 'button':
				ptext.draw(wdgt.text, (wdgt.x+int(wdgt.width/4), wdgt.y+ int(wdgt.height / 4)))
			elif wdgt.type == 'textarea':
				ptext.draw(wdgt.text, (wdgt.x + int(wdgt.width/4), wdgt.y + int(wdgt.height/4)))
				if not wdgt.isSelected and wdgt.text == '':
					ptext.draw(wdgt.placeholder, (wdgt.x + int(wdgt.width/5), wdgt.y + int(wdgt.height/4)), color=WHITE, fontsize=20)
				else:
					pass
		pygame.display.update()
		pygame.time.Clock().tick(FPS)
if __name__ == '__main__':
	RefreshList()
	gameloop()