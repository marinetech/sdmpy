from time import sleep
from helper import reset
from helper import runCMD
from os import path
from os import listdir
from os import makedirs
import signal
import fcntl
import os
# ======  Variables ==============
Fs = 67500
rxFilename = 'rx_OFDM_'
refFileName = 'ShortLFM'
FNAME = "./tx"
c = {}

modems = ['147']
c['136'] = ['1','0','0'] # threshold 1-4095 , gain , level
c['137'] = ['200','0','0']
c['138'] = ['1','0','0']
c['146'] = ['1','0','0']
c['147'] = ['1','0','0']
c['148'] = ['1','0','0']

# ============== loop code ============

def handler(signum, frame):
    print ('./tx was changed')
    runCMD('stop',m)
    for n in os.listdir(FNAME):
        runCMD('tx ' + FNAME + '/' + n)
        os.remove(FNAME + '/' + n)

def notify(directory, handler):
    fd = os.open(FNAME, os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_NOTIFY,fcntl.DN_CREATE)
    signal.signal(signal.SIGIO, handler)

if not path.exists(FNAME):
    makedirs(FNAME)

if not path.exists('./tmp'):
    makedirs('./tmp')

# signal.signal(signal.SIGIO, handler)
# fd = len(listdir(FNAME))
# fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
# fcntl.fcntl(fd, fcntl.F_NOTIFY,fcntl.DN_MODIFY)
notify(FNAME, handler)

m = modems[0]
try:
    reset('192.168.0.' + m)
except:
    print("# Cannot connect to modem : " + m )
    exit()

runCMD('stop',m)
while 1:
	nextFileId =  len([name for name in listdir('./tmp') if (path.isfile('./tmp/' + name) and rxFilename in './tmp/' + name)])
	runCMD('config 1 0 0\n',m)
	runCMD('ref tmp/' + refFileName,m)
	runCMD('rx ' + str(Fs*5) + ' ./tmp/' + rxFilename + str(nextFileId),m)
