from bibliDUREE import *
import RPi.GPIO as GPIO
#11/04/21  BIBLI RFID
        
pin_rfid = 26

trame = Duree(time.time(), 0.000104)#objet
cligno = Duree(time.time(), .5)#objet

def f_initGpioRfid():
    GPIO.setup(pin_rfid,GPIO.IN)#RFID
    #GPIO.setup(21attention,GPIO.OUT, initial=GPIO.LOW)#LED RFID

def f_portRf():
    return GPIO.input(pin_rfid)

def f_tempsBit(coeff = 1):
    trame.a_hInit = time.time()
    while trame.m_duree(coeff):
        pass

def f_rf():#lit 8 bit de rfid
    data = 0
    cligno.a_hInit = time.time()
    
    while  f_portRf():#attente bit start
        if cligno.m_duree() == False:
            #GPIO.output(21, not GPIO.input(21))
            cligno.a_hInit = time.time()
    
    f_tempsBit(.5)# espace bit start/ frame
    for i in range(8):
        data >>= 1
        f_tempsBit()# espace inter bit
        if f_portRf():
            data |= 0x80        
    f_tempsBit()# espace inter trame
    #GPIO.output(21, 1)
    return data

def f_verifRfid(suite):
    print(9)
    drap = 0
    if suite[0] != 2:
        drap = 1
    if suite[13] != 3:
        drap = 1
    if suite[1] == 48:
        drap = 1
    for i in range(1,13):
        if (suite[i] < 48) or (suite[i] > 70):
            drap = 1
        if (suite[i] >57) and (suite[i] < 65):
            drap = 1
    if drap == 0:
        return True
    else:
        return False

erreur = 0 #variable globale
def f_rfid():
    print('ATTENTE BADGE')
    global erreur
    drap = 0
    while drap == False:
        su = []
        drap = 0
        for k in range(14):
            su.append(f_rf())
        drap = f_verifRfid(su)        
        if not drap:
            erreur += 1
        print(drap, erreur, 'e', su)    
    return su[1:11]

def f_can_rfid():#compacte les 10 octets rfid en 5 octets hexa pour transmission bus can
    su_hexa = [0] * 10
    su_can_rfid = [0] * 5
    su_ascii = f_rfid()     #[54, 54,48,48,66,68,52,70,51,57,65] 
    for kk in range(10):
        if (su_ascii[kk] > 47) and (su_ascii[kk] < 58):
            su_hexa[kk] = su_ascii[kk] - 48
        else:
            su_hexa[kk] = su_ascii[kk] - 55
    #print(su_hexa)
    for kk in range(5):
        su_can_rfid[kk] = su_hexa[kk * 2] * 16
        su_can_rfid[kk]= su_can_rfid[kk] | su_hexa[kk * 2 + 1]
    return su_can_rfid




 


