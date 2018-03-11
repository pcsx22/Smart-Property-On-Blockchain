import socket
import fcntl
import struct,sys,select
from base64 import b64encode,b64decode
from Crypto.PublicKey import RSA
import KeyHandler
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]

IP = sys.argv[1]
PORT = 6060
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((IP,PORT))
client_key = RSA.importKey(KeyHandler.client_priv_key)
print "Connected... "
command = raw_input("Enter Command: ")
sock.send(command)
if "login" in command:
  print "Receiving AES key.."
  secret = client_key.decrypt(b64decode(sock.recv(1024)))
  cipher = AES.new(secret)

  sys.stdout.write("\n$")
  while 1:
    readable,writable,exceptional = select.select([sys.stdin,sock.fileno()],[],[],0)
    if sys.stdin in readable:
      command = raw_input()
      sock.send(b64encode(cipher.encrypt(pad(command))))
      sys.stdout.write("\n$")
    elif sock.fileno() in readable:
      print sock.recv(1024)
      sys.stdout.write("$")


# sock.close()
