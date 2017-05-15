from time import sleep
from helper import reset
from helper import runCMD

Fs = 250000
c = {}
FileIDVec = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']

############################
####   Variables    ########
############################

modems = ['136']
c['136'] = ['1','0','0'] # threshold 1-4095 , gain , level
c['137'] = ['1','0','0'] 
c['138'] = ['1','0','0'] 
c['146'] = ['1','0','0'] 
c['147'] = ['1','0','0'] 
c['148'] = ['1','0','0'] 

############################
#### Run the script ########
############################

# commands : 
# stop 
# config Threshold, gain, level
# tx [filename]
# tx ShortLFM
# tx LFM
# ref [filename]
# rx [samples] tmp/[filename]


for m in modems:
	try:
		reset('192.168.0.' + m)
		runCMD('config ' + ' '.join(c[m]) + '\n',m)
		runCMD('ref tmp/ShortLFM','136')		
		for FileID in FileIDVec:
			runCMD('rx ' + str(Fs*20) + ' tmp/rx_LobsterSecond' + FileID,'136')
			print("# another reception ended " )

	except:
		print("# Cannot connect to modem : " + m )
		continue



#for m in modems:
	#try:
		#reset('192.168.0.' + m)
	#except:
		#print("# Cannot connect to modem : " + m )
		#continue
	#runCMD('config ' + ' '.join(c[m]) + '\n',m)
	#runCMD('tx tmp/ShortLFM',m)
	#sleep(0.25)
	#runCMD('tx tmp/LFM',m)
	#sleep(1)
	#runCMD('tx tmp/ShortLFM',m)
	#runCMD('tx tmp/ShortLFM',m)
	#runCMD('ref tmp/ShortLFM',m)
	#runCMD('rx 125000 tmp/rx1',m)
	#sleep(1)
