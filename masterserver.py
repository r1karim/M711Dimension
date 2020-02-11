import socket
from time import time
import pickle
from threading import Thread
IP = '127.0.0.1'
PORT = 56871
sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind((IP,PORT))

server = {
	'hostname': '',
	'IP': '',
	'PORT': -1,
	'Gamemode': '',
	'maxplayers': 0,
	'language': '',
}
servers = []

def server_com():
	while True:
		x= time() + 10
		srvs = []
		while(time() < x):
			try:
				r,addr=sock.recvfrom(1024)
				r = r.decode('UTF-8')
				separators = []
				server_ip = addr[0]
				server_port = addr[1]
				for i in range(len(r)):
					if(r[i] == '$'):
						separators.append(i)
				server_name = r[separators[0]+1:separators[1]]
				server_gamemode = r[separators[1]+1:separators[2]]
				server_language = r[separators[2]+1:separators[3]]
				server_maxplayers = int(r[separators[3]+1:])
				server['hostname'] = server_name
				server['IP'] = addr[0]
				server['PORT'] = addr[1]
				server['Gamemode'] = server_gamemode
				server['maxplayers'] = server_maxplayers
				server['language'] = server_language
				for srv in srvs:
					if(srv['IP'] == server_ip and srv['PORT'] == server_port):
						break
				else:
					srvs.append(server)
			except:
				pass
		servers = srvs
		print(servers)
def client_com():
	while True:
		_bytes_,addr = sock.recvfrom(1024)
		if _bytes_.decode('UTF-8') == '$__J711__$_4EVA':
			obj = pickle.dumps(servers)
			sock.sendto(obj, (addr))
if __name__ == '__main__':
	thread = Thread(target=server_com)
	thread_ = Thread(target=client_com)
	thread.start()
	thread_.start()