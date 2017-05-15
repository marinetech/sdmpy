import socket
import subprocess

def reset(modemIP):
  sock = socket.create_connection((modemIP, 9200), 2)
  sock.send(b'AT?S\n')
  if (b'PHY' not in sock.recv(1024)):
    sock.send(b'ATP\n')
    sock.recv(1024)
    print ("# modem " + modemIP + " reset")

def runCMD(cmd,modemID):
	print ("# exec cmd : " + cmd)
	shell = subprocess.Popen(["sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	with open('f.tmp','w') as w:
		w.write(cmd)
	cmdSh = "./sdmsh " + modemID + " -f f.tmp\n"	
	shell.stdin.write(cmdSh.encode('ascii'))
	shell.stdin.close()
	for l in shell.stdout:
		print(l)
