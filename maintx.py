import numpy as np
import math as m
import scipy as sp
import binascii

#########################################################
#########################################################
############   VARIABLES    #############################
#########################################################

DataBits = '101010101010101010101010101'
#Fs = 67500
Fs = 250000
Fc1 = 48000 # 7000

Fc2 = 78000 #17000
BW = Fc2 - Fc1
M = 8
Ts = 0.1
Tref = 0.2
Tguard = 0.01
Amp = 32000
FVec = np.linspace(Fc1, Fc2, M)
r = 0.3
Tshort = 1024/Fs

######### Do not touch below this line  #################
#########################################################
#########################################################

def tukeywin(window_length, alpha=0.5):
    # Special cases
    if alpha <= 0:
        return np.ones(window_length) #rectangular window
    elif alpha >= 1:
        return np.hanning(window_length)
 
    # Normal case
    x = np.linspace(0, 1, window_length)
    w = np.ones(x.shape)
 
    # first condition 0 <= x < alpha/2
    first_condition = x<alpha/2
    w[first_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[first_condition] - alpha/2) ))
 
    # second condition already taken care of
 
    # third condition 1 - alpha / 2 <= x <= 1
    third_condition = x>=(1 - alpha/2)
    w[third_condition] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[third_condition] - 1 + alpha/2))) 
 
    return w

#from sdmpy import sdmControl
#s = sdmControl()
#modem = b'192.168.0.148'
#s.addModem(modem)
#s.connect()

BitNum = len(DataBits)

SymbolNum = int(BitNum / m.log2(M))
SymbolVec = []
Sig = []

for SymbolID in range(int(SymbolNum)):
    CurrentBit = DataBits[int(SymbolID*m.log2(M)): int(SymbolID*m.log2(M) + min(m.log2(M), len(DataBits)))]
    diff = m.log2(M) - len(CurrentBit)
#    print(diff)
#    CurrentBit = [zeros(1,diff), CurrentBit]
    Data = int(CurrentBit,2) #bin2dec(CurrentBit)
    SymbolVec.append(Data) # = [SymbolVec, dec2base(Data, M)]

t = np.linspace(0, Ts, round(Ts*Fs))

TxSig = []
for SymInd in range(len(SymbolVec)):
  CurrentF = FVec[int(SymbolVec[SymInd])]
  for tt in t:
    TxSig.append( Amp * m.cos(2*m.pi*CurrentF*tt)) 
  for i in range(round(Tguard*Fs)):
    TxSig.append(0)

TxSigTukey = tukeywin(len(TxSig),r)
Res = []
l = np.std(TxSig)
max = 0
min = 0
for ind in range(len(TxSigTukey)):
  tempTxSigTukey= TxSigTukey[ind]*TxSig[ind]/l
  Res.append(tempTxSigTukey)
  if (tempTxSigTukey > max): max = tempTxSigTukey
  if (tempTxSigTukey < min): min = tempTxSigTukey

min = min * -1
if (max > min):
  factor = int(32000/max)
else:
  factor = int(32000/min)
for ind in range(len(TxSigTukey)):
  Res[ind] = int(Res[ind]*factor)
  Sig.append(int(Res[ind]))

ShortLFM = []
LFMSignal = []
# ======================== START SHORT CHIRP ===============
t = np.linspace(0, Tshort, round(Tshort*Fs))
#c = chirp(t,Fc1,Ts,Fc2)
for j in range(len(t)):
  beta = (Fc2-Fc1) * (m.pow((len(t)/Fs), -1 ))
  i = j / Fs
  sample = m.cos(m.pi * 2 * (beta / (2) * m.pow(i, (2)) + Fc1 * i))
  sample *= Amp
  LFMSignal.append(sample)

LFMTukey = tukeywin(len(LFMSignal),r)
l = np.std(LFMSignal)
max = 0
min = 0

for ind in range(len(LFMTukey)):
  ShortLFM.append(LFMTukey[ind]*LFMSignal[ind]/l)
  if (ShortLFM[ind] > max): max = ShortLFM[ind]
  if (ShortLFM[ind] < min): min = ShortLFM[ind]

min = min * -1
if (max > min):
  factor = int(32000/max)
else:
  factor = int(32000/min)
for ind in range(len(ShortLFM)):
  ShortLFM[ind] = int(ShortLFM[ind]*factor)


# ======================== END SHORT CHIRP ===============
LFM = []
LFMSignal = []
LFMTX = [0]*64
# ======================== START CHIRP ===============
t = np.linspace(0, Tref, round(Tref*Fs))
#c = chirp(t,Fc1,Ts,Fc2)
for j in range(len(t)):
  beta = (Fc2-Fc1) * (m.pow((len(t)/Fs), -1 ))
  i = j / Fs
  sample = m.cos(m.pi * 2 * (beta / (2) * m.pow(i, (2)) + Fc1 * i))
  sample *= Amp
  LFMSignal.append(sample)

LFMTukey = tukeywin(len(LFMSignal),r)
l = np.std(LFMSignal)
max = 0
min = 0

for ind in range(len(LFMTukey)):
  LFM.append(LFMTukey[ind]*LFMSignal[ind]/l)
  if (LFM[ind] > max): max = LFM[ind]
  if (LFM[ind] < min): min = LFM[ind]

min = min * -1
if (max > min):
  factor = int(32000/max)
else:
  factor = int(32000/min)
counter = 0
for ind in range(len(LFM)):
  LFM[ind] = int(LFM[ind]*factor)
  #LFMTX[counter] =hex(LFM[ind])
  #s.tx(modem,hex(LFM[ind]))
  #print(hex(LFM[ind]))
  #counter = counter + 1
  #if(counter % 64 == 0):
  #  print(''.join(LFMTX))
  #  s.tx(modem,''.join(LFMTX))
  #  counter = 0


# ======================== END CHIRP ===============
Guard = []

for i in range(round(Tguard*Fs)):
  Guard.append(int(0))

#TxSig = tukeywin(len(TxSig),r) #.'.*TxSig/std(TxSig)
print(ShortLFM)
toFile = ShortLFM
with open('tmp/ShortLFM','w') as w1:
	for f in range(len(ShortLFM)):
		w1.write(str(int(ShortLFM[f]))+'\n')
#np.savetxt("./ShortLFM",toFile,delimiter="\n")

print(LFM)
toFile = LFM
with open('tmp/LFM','w') as w2:
	for f in range(len(LFM)):
		w2.write(str(int(LFM[f]))+'\n')

Sig2Tx = np.concatenate((Guard, ShortLFM, Guard, LFM, Guard, Sig), axis=0)
#for f in range(len(toFile)):
#  toFile[f] = int(toFile[f])
#np.savetxt("./fullSignal",toFile,delimiter="\n")


#LFMSignal = tukeywin(len(LFMSignal),r).'.*LFMSignal/std(LFMSignal)

#t = np.linspace(0, Tshort, round(Tshort*Fs))
#ShortLFMSignal = Amp*chirp(t,Fc1,Ts,Fc2)
#ShortLFMSignal = tukeywin(len(ShortLFMSignal),r).'.*ShortLFMSignal/std(ShortLFMSignal)

#Sig2Tx = [ShortLFM, Guard, LFM,Guard, Sig]
with open('tmp/Sig2Tx','w') as w1:
	for f in range(len(Sig2Tx)):
		w1.write(str(int(Sig2Tx[f]))+'\n')
#print (FVec)

