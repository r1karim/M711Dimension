import socket
from time import time
import pickle
from threading import Thread
from datetime import datetime
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
	'language': ''
}
servers = []

def com():
	while True:
		x= time() + 10
		srvs = []
		while(time() < x):
			try:
				_bytes_,addr = sock.recvfrom(1024)
				_bytes_ = _bytes_.decode('UTF-8')
				if _bytes_ == '$__J711__$_4EVA':
					_object_ = pickle.dumps(servers)
					sock.sendto(_object_, (addr))
				else:
					separators = []
					server_ip = addr[0]
					server_port = addr[1]
					for i in range(len(_bytes_)):
						if(_bytes_[i] == '$'):
							separators.append(i)
					server_name = _bytes_[separators[0]+1:separators[1]]
					server_gamemode = _bytes_[separators[1]+1:separators[2]]
					server_language = _bytes_[separators[2]+1:separators[3]]
					server_maxplayers = int(_bytes_[separators[3]+1:])
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

if __name__ == '__main__':
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print('['+current_time+'] M711Dimension master server has been launched.')
	thread = Thread(target=com)
	thread.start()