import RPi.GPIO as GPIO
import time
#12 02 21


canCsPin = 8
canSclkPin = 11
canMosiPin = 10
canMisoPin = 9
canIntPin = 25

MODE_NORMAL = 0x00
MODE_LOOPBACK = 0x40
MODE_CONFIG = 0x80

STX0 = 0x81
STX1 = 0x82
STX2 = 0x84

LTX0 = 0x40
LTX1 = 0x42
LTX2 = 0x44

RX0 = 0
RX1 = 1

def f_initCanGpio():
    #GPIO.setwarnings(False)
    #GPIO.setmode(GPIO.BCM)
    GPIO.setup(canCsPin,GPIO.OUT)
    GPIO.setup(canSclkPin,GPIO.OUT)
    GPIO.setup(canMosiPin,GPIO.OUT)    
    GPIO.setup(canMisoPin,GPIO.IN)
    GPIO.setup(canIntPin,GPIO.IN)


def f_canW8(buffer):
    for i in range(8):
        if buffer & 0x80:
            GPIO.output(canMosiPin, 1)
        else:
            GPIO.output(canMosiPin,0)
        #print(buffer & 0x80)
        buffer <<= 1
        GPIO.output(canSclkPin, 1)
        GPIO.output(canSclkPin, 0)
        
def f_canR8():
    data = 0
    for ik in range(8):
        data <<= 1
        if GPIO.input(canMisoPin):
            data |= 0x1
        else:
            data |= 0
        GPIO.output(canSclkPin, 1)
        GPIO.output(canSclkPin, 0)     
    #GPIO.output(canCsPin, 1)
    return data
        
def f_canRegistreW(adr, data):
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(0x02)
    f_canW8(adr)
    f_canW8(data)
    GPIO.output(canCsPin, 1)

def f_canRegistreR(adr):
    tmp = 0
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin,0)
    GPIO.output(canCsPin, 0)
    f_canW8(0x03)
    f_canW8(adr)
    tmp = f_canR8()
    GPIO.output(canCsPin, 1)    
    return tmp



def f_canReset():
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(0xc0)
    GPIO.output(canCsPin, 1)

def f_canInitHorloge():#                      ***** Horloge ****
    f_canRegistreW(0x2a, 0x02)
    f_canRegistreW(0x29, 0xb1)
    f_canRegistreW(0x28, 0x06)

def f_canMode(mode):
    f_canRegistreW(0xf, mode)
    
def f_canRts(regis):#                       *** STX0, STX1,  STX2 ***
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(regis)
    GPIO.output(canCsPin, 1)
    
def f_canBitModify(registre, masque, data):
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(0x05)
    f_canW8(registre)
    f_canW8(masque)
    f_canW8(data)
    GPIO.output(canCsPin, 1) 

def f_canReadRxStatut():
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(0xb0)
    return(f_canR8())

def f_canReadStatut():
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(0xa0)
    return(f_canR8())



def f_canEcriture(com, donnees):# com >> LTX0, LTX1, LTX2
    while f_canReadStatut() & 0x04 == True:
        pass
    #ime.sleep(.03)
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    f_canW8(com)
    for i in range(13):
        f_canW8(donnees[i])
    GPIO.output(canCsPin, 1)
    f_canRts(STX0)

def ff_canLecture(rx):#                         RX0, RX1
    #while f_canReadRxStatut() & 0x40 == 0:
        #pass
    #print(10)
    d13 = []
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    if rx == 0 :
        f_canW8(0x90)
    else:
        f_canW8(0x94)
    for i in range(13):
        d13.append(f_canR8())
    GPIO.output(canCsPin, 1)
    #print(d13, 777)
    return d13

def f_canLecture(rx):#                         RX0, RX1
    #print(103)
    rxx = f_canReadRxStatut()
    d13 = []
    GPIO.output(canCsPin, 1)
    GPIO.output(canSclkPin, 0)
    GPIO.output(canCsPin, 0)
    if rxx & 0x80 == 0x80:
        f_canW8(0x96)
    else:
        f_canW8(0x90)
    for i in range(13):
        d13.append(f_canR8())
    GPIO.output(canCsPin, 1)
    #print(d13, 777)
    return d13


def f_filtre0(typ, eme, rec):
    f_canRegistreW(0x0, typ)
    f_canRegistreW(0x01, 0x08)
    f_canRegistreW(0x02, eme)
    f_canRegistreW(0x03, rec)

def f_masque0(ty, em, re):
    f_canRegistreW(0x20, ty)
    f_canRegistreW(0x21, 0x00)
    f_canRegistreW(0x22, em)
    f_canRegistreW(0x23, re)
    
def f_masque1(ty, em, re):
    f_canRegistreW(0x24, ty)
    f_canRegistreW(0x25, 0x00)
    f_canRegistreW(0x26, em)
    f_canRegistreW(0x27, re)    
    
def f_canINIT():
    #print(102)
    f_initCanGpio()
    f_canReset()
    f_canInitHorloge()
    f_canMode(MODE_CONFIG)
    f_filtre0(5,45,220)
    f_masque0(0x00,0xff,0x00)
    f_masque1(0x00,0xff,0x00)
    f_canRegistreW(0x60, 0x04)## mode filtrage + roll over rx0 rx1
    f_canRegistreW(0x70, 0x00)
    f_canMode(MODE_NORMAL)    

"""

f_initCanGpio()
f_canReset()
f_canInit()
f_canMode(MODE_LOOPBACK)
f_canW_registre(0x60, 0x60)# regime filtres
donnees13 = [5,0x0b,45,50,8,10,20,30,40,50,60,78,0x00]
f_canLoadBuffer(LTX0, donnees13)
#f_canRts(STX0)
while f_canReadRxStatut() & 0x40 == 0:
    pass
ds13 = []
ds13 = f_canLecture(0)
print(ds13, 999)
print(f_canReadRxStatut())# & 0x40)


for ik in range(5):
    f_canLoadBuffer(LTX0, donnees13)
    #f_canRts(STX0)
    while f_canReadRxStatut() & 0x40 == 0:
        pass
    ds13 = []
    ds13 = f_canLecture(0)
    print(ds13, 900+ik)
    donnees13[11] += 1
   

emetteur = 36
recepteur = 100
type = 5
effectif = 4
niveau = 3
passage = 1
record = 600

r_emetteur = 0
r_recepteur = 0
r_type = 0
r_effectif = 0
r_niveau = 0
r_passage = 0
r_record = 0

bE = []
#bR = []

for l in range(13):
    bE.append(0)
print(bE)

bE[0] = type
bE[1] = 0x08
bE[2] = emetteur
bE[3] = recepteur
bE[4] = 0x8
bE[5] = effectif
bE[6] = niveau
bE[7] = passage
bE[8] = record//256
bE[9] = record % 256

print(bE)

f_canLoadBuffer(LTX0, bE)
bR = f_canLecture(RX0)
print(bR, 900+ik)    

r_type = bR[0]
r_emetteur = bR[2]
r_recepteur = bR[3]
r_record = bR[8] * 256 + bR[9]

print(r_type, r_emetteur, r_recepteur, r_record)"""



  
    
    
    
    