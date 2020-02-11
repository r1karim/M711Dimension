import pygame,sys
import socket
import pickle

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
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
	print('Sent bytes...')
	_bytes_,addr = s.recvfrom(1024)
	print('Received bytes...')
	print(_bytes_)
	servers = pickle.loads(_bytes_)
	print('Loaded bytes...')
	print(servers)
def gameloop():
	while True:
		events = pygame.event.get()
		for event in events:
			if(event.type == pygame.QUIT):
				pygame.quit()
		surface.fill((255,255,255))
		pygame.draw.rect(surface, (255,255,255),(100,100,100,100))
		pygame.display.update()
		pygame.time.Clock().tick(FPS)


if __name__ == '__main__':
	RefreshList()
	gameloop()