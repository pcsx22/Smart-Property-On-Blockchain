import socket
import fcntl
import struct,os,sys,subprocess,select
import binascii,requests,time,random,json
import KeyHandler
from Crypto.PublicKey import RSA
from base64 import b64encode,b64decode
from Crypto.Cipher import AES
import KeyHandler

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]

class MySocket(socket.socket):
    def __init__(self, family=socket.AF_UNIX, type=socket.SOCK_STREAM, proto=0, _sock=None):
        socket.socket.__init__(self, family, type, proto, _sock)
        
    def write(self, text):
        return self.send(text)
    
    def readlines(self):
        return self.recv(2048)
    
    def read(self):
        return self.recv(1024)
    
    def accept(self):
        conn, addr = socket.socket.accept(self)
        return MySocket(_sock=conn), addr 

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

IP = get_ip_address('eth0')
PORT = 6060
BUFFER_SIZE = 1024

sock = MySocket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((IP,PORT))
sock.listen(5)

local_server_address = '/tmp/my_sock1'
my_address = KeyHandler.device_block_chain_address[0]['address']
my_public_key = KeyHandler.device_block_chain_address[0]['pubkey']
my_priv_key = KeyHandler.device_block_chain_address[0]['privkey']

try:
    os.unlink(local_server_address)
except OSError:
    if os.path.exists(local_server_address):
        raise

local_sock = MySocket(socket.AF_UNIX,socket.SOCK_STREAM)
local_sock.bind(local_server_address)
local_sock.listen(1)


print 'Listening on ', IP , PORT

while 1:
	print "Waiting for connection..."
	conn,addr = sock.accept()
	print 'Received a connection from: ', addr
	command = conn.recv(BUFFER_SIZE)
	command = command.split(" ");
	method = command[0]
	if method == "login":
		transaction_id = command[1]
		vout = int(command[2])
		signature = command[3]
		message = command[4]
		print "Transaction Id: ",transaction_id,"\nSignature: ", signature, "\nMessage: ", message
		r = requests.post("http://172.17.0.1:5000/getTransaction/",json={'transaction_id' : transaction_id}).json()
		old_record = requests.post("http://172.17.0.1:5000/getOwnership/",json={'address':my_address}).json()
		t_check = (old_record[-1]['data'] == transaction_id)
		#Need a transaction check by getting data from streams and comparing with the provided data
		addressList = r['vout'][vout]['scriptPubKey']['addresses']
		exit_status = os.system("multichain-cli -cold test1 verifymessage " + addressList[0] + " " + signature + " " + message)
		if exit_status == 0 and t_check:
			print "\nVerified!"
			s = requests.post("http://172.17.0.1:5000/getPubKey/",json={'address' : addressList[0]}).json()
			print "Public key of the user: ",s
			pubKey = binascii.a2b_hex(s[0]['data'])
			client_public_key = RSA.importKey(pubKey)
			secret = os.urandom(16)
			cipher = AES.new(secret)
			conn.send(b64encode(client_public_key.encrypt(secret,32)[0]))
			
			new_pid = os.fork()
			if new_pid == 0:
				fork_sock = MySocket(socket.AF_UNIX,socket.SOCK_STREAM)
				time.sleep(0.5)
				try:
					fork_sock.connect(local_server_address)
					print "LOCAL SOCKET CONNECTED...."
				except socket.error,msg:
					print sys.stderr,msg
					sys.exit(1)
				proc = subprocess.Popen("/bin/bash",stdin=fork_sock,stdout=fork_sock,stderr=fork_sock,shell=True)
				while 1:
					time.sleep(3)
			else:
				local_conn,local_addr = local_sock.accept()
				while True:
					readable,writable,exceptional = select.select([conn.fileno(),local_conn.fileno()],[],[],0.2)
					if conn.fileno() in readable:
						data = conn.read()
						data = unpad(cipher.decrypt(b64decode(data)))
						data = data + "\n"
						local_conn.write(data)
					elif local_conn.fileno() in readable:
						data = local_conn.read()
						conn.write(data)
			#spawn a process for shell and let the user communicate  
		else:
			print "Verification Failed!"
		conn.close()
	elif method == "create-ownership":
		transaction_id = command[1]
		vout = command[2]
		signature = command[3]
		message = command[4]
		r_port = 2000 + random.randint(1,1000)
		sock_change = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock_change.bind((IP,r_port))
		sock_change.listen(1)
		old_record = requests.post("http://172.17.0.1:5000/getOwnership/",json={'address':my_address}).json()
		print "Existing stream data: ",old_record[-1]
		#assume last entry is the latest valid entry
		old_transaction = old_record[-1]['data']
		if old_transaction == transaction_id:
			print "Ownership belongs to u"
			sys.exit(0)
		trans = requests.post("http://172.17.0.1:5000/getTransaction/",json={'transaction_id' : transaction_id}).json()
		spent_transaction = trans['vin'][0]["txid"]
		print spent_transaction,"----",old_transaction
		if spent_transaction == old_transaction:
			print "Ownership needs to be changed"
			address_record = trans['vout'][int(vout)]['scriptPubKey']['addresses'][0]
			exit_status = os.system("multichain-cli -cold test1 verifymessage " + address_record + " " + signature + " " + message)
			if exit_status == 0:
				r = requests.post("http://172.17.0.1:5000/createOwnership/",json={'port':r_port,'ip':IP})
				print "Waiting for connection:"
				r_conn,r_addr = sock_change.accept()
				print "connection Received: ",r_addr
				r_conn.send(my_address + "," + address_record + "," + transaction_id)
				data = r_conn.recv(1024)
				print "Raw Transaction: ", data
				related_tx_str = r_conn.recv(1024)
				print "Transaction vin : " + related_tx_str
				a = subprocess.Popen("multichain-cli -cold test1 signrawtransaction " + data + " '" + related_tx_str + "' " + "'[\"" + my_priv_key + "\"]'",stdout=subprocess.PIPE,shell=True).communicate()[0]
				print a
				r_conn.send(a)
				sock_change.close()



#store the public key of the device in BC(multichain stream), retrieve it, use it to encrypt the command and send it to the device(DNS entry might to required to do this wihtout
#the need of ip address.) 
#ask the server to get the public address of the user and use it to encrypt AES key for further cumminication