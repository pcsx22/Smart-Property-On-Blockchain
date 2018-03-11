<h2>#ABOUT</h2>
This is a rough hackish and poor implementation(lots of security issues) of smart property on blockchain. Multichain is used as a platform for providing underlying blockchain infrastrucutre for implementing smart property.This was solely built with the purpose to learn build blockchain based apps.<br/><br/>

Here smart property means not only storing the ownership data of the device in blockchain but also issuing cryptographic tokens for authentication of the real user. Smart devices store their ownership data in a blockchain based key-value store(which multichain calls as stream). Whoever can provide a valid signature for proving as a valid owner can access the device. Ownership can be changed if when a valid new transaction can be provided to the device with valid signature for proving the user own the address.
 
<h2>#SETUP</h2>
1. Dockerfile will create the necessary linux environment with multichain installed. Both hot and cold node can be started

2. A Flask server running in hot nodes. Hot nodes serve as the data hub. It's semi-decantralized environment. Client.py works like a cyrpto wallet while hot nodes work as full blockchain data server serving data to wallet client via REST API for wallet client verification purpose.

3. Daemon.py file is a simulation to a smart electronic device(eg: RASPBERy PI) that supports linux. (Future reference: Daemon.py can be configured with login shell to control user verfication via our sets of API)

4. Savoir API is used for communication with hot nodes. Savoir is basically a wrapper over JSON-RPC API provided by multichain. 

5. keyhandler.py contains RSA public keys and multichain addresses for testing purpose.

<h2>#BlockChain settings</h2>

1. A blockchain with a name is to be started via all the hot nodes. Mine is test1

2. Create a stream for ownership of the device. Basically, stream in multichain is a key-value store which contains data like the ownership data of the smart devices. Also create another stream to hold public key of all the smart devices for encrypting the TCP connection between the device and the client. (key:address of devices, value:public key or ownership data - acutally both can be implemented in one stream}

3. Form a network of hot nodes and start executing transactions.

<h2>#Commands</h2>
1. login [ownership-transactiond-id] [vout] [signature] [message] - for preventing replay attacks nonce can be sent to client from the smart device as a part of handshaking process. 

2. create-ownership [new-transaction-id] [vout] [signature] [message] - [new-transactiond-id] should spend the old ownership transaction of the device. After verifying if [new-transaction-id] is produced 
by spending old-transaction-id, the device changes it's ownership by updating ownership stream.

<b>#NOTE:</b> Only I maybe able to set this project properly. It's a complete mess and poorly written python code
