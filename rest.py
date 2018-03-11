from flask import Flask, request, session
from Savoir import Savoir
import json,time,socket,sys
from thread import start_new_thread

rpcuser = 'multichainrpc'
rpcpasswd = 'DjYSEurAYtCQmbxXve1KVNZDZikeSTx2StHFtccdQBNo'
rpchost = 'localhost'
rpcport = '9538'
chainname = 'test1'
api = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
app = Flask(__name__)
app.secret_key = "lolololol"


def create_ownership(ip,port):
	time.sleep(0.2)
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((ip,port))
	data = sock.recv(1024)
	data = data.split(",")
	device_address = data[0]
	print "Device Address: ",device_address
	client_address = data[1]
	transaction_id =data[2]
	hex_data = api.createrawsendfrom(device_address,{},[{"for":"ownership-stream","key":device_address,"data":transaction_id}])
	sock.send(hex_data)
	raw_tx = api.decoderawtransaction(hex_data)
	tx_id = raw_tx['vin'][0]['txid']
	tx_out = api.gettxout(tx_id,0)
	related_tx_str = '[{"txid":\"'+ tx_id +'\","vout":0,"scriptPubKey":\"' + tx_out['scriptPubKey']['hex'] + '\"}]'
	sock.send(related_tx_str)
	data = sock.recv(1024)
	data = json.loads(data)
	print "########## Sending Raw Transaction ################"
	print api.sendrawtransaction(data['hex'])
	sock.close()
	#create transaction 

@app.route('/')
def test():
	print api.getinfo()
	return 'Hello World\n'


@app.route('/getTransaction/', methods=['POST'])
def getTransaction():
	data = request.get_json(force=True)
	txid = data['transaction_id']
	print "request for transaction_id: ",txid
	txData = api.getrawtransaction(txid,1)
	return json.dumps(txData)

@app.route('/getPubKey/', methods=['POST'])
def getPubKey():
	address = request.get_json(force=True)['address']
	print address
	keyData = api.liststreamkeyitems("test-stream",address) 
	return json.dumps(keyData)

@app.route('/getOwnership/', methods=['POST'])
def getOwnership():
	address = request.get_json(force=True)['address']
	keyData = api.liststreamkeyitems("ownership-stream",address)
	return json.dumps(keyData)

@app.route('/createOwnership/', methods=['POST'])
def createOwnership():
	port = request.get_json(force=True)['port']
	ip = request.get_json(force=True)['ip']
	start_new_thread(create_ownership,(ip,port,))
	return "a"


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug = True)