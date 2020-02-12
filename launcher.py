import pygame,sys
import socket
import pickle
from Libraries import ptext


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
MASTER_LIST_PORT = 56871


s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 60310))
bytes_ = '$__J711__$_4EVA'.encode('UTF-8')
servers = []

def RefreshList():
	global servers
	s.sendto(bytes_, (MASTER_LIST_IP, MASTER_LIST_PORT))
	_bytes_,addr = s.recvfrom(1024)
	servers = pickle.loads(_bytes_)
	print(servers)
def gameloop():
	while True:
		surface.fill(GREY)

		events = pygame.event.get()
		for event in events:
			if(event.type == pygame.QUIT):
				pygame.quit()
		pygame.draw.rect(surface, LIGHTBLUE, (10,10, SCREEN_WIDTH-200, 25))
		ptext.draw('hostname\tplayers', (12,12), fontsize=25)
		for srv in servers:
			serverid = servers.index(srv) + 1
			pygame.draw.rect(surface, LIGHTBLUE, (10,10 + (serverid*30),SCREEN_WIDTH-200,25))
			ptext.draw(srv['hostname']+'\t0/'+str(srv['maxplayers']), (14, 14 + (serverid*30)), fontsize=20)
		pygame.draw.rect(surface, GREEN, (30 + SCREEN_WIDTH-200,10, 100,25))
		ptext.draw('Play', (SCREEN_WIDTH-140, 14), fontsize=22)
		pygame.draw.rect(surface, GREEN, (30 + SCREEN_WIDTH-200,40, 100,25))
		ptext.draw('Refresh list', (SCREEN_WIDTH-165, 45))
		pygame.display.update()
		pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
	RefreshList()
	gameloop()