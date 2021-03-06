
import socket
import ssl

TYPE_UDP = 0
TYPE_TCP = 1
TYPE_SSL = 2

class Socket:
	def __init__(self, type):
		if type == TYPE_UDP:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		elif type == TYPE_TCP:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
		else:
			tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
			self.s = ssl.wrap_socket(tcp)
			
		self.server_addr = None
		
	def connect(self, host, port, timeout=3):
		self.s.settimeout(timeout)
		try:
			self.s.connect((host, port))
		except socket.timeout:
			return False
		self.s.setblocking(False)
		self.server_addr = host, port
		return True

	def close(self): self.s.close()
	def send(self, data): self.s.sendall(data)
	def recv(self, num=4096):
		try:
			return self.s.recv(num)
		except (BlockingIOError, ssl.SSLWantReadError):
			pass
		except OSError:
			return b""
			
	def client_address(self): return self.s.getsockname()
	def server_address(self): return self.server_addr
