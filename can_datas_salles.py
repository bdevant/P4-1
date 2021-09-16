from bibliCAN import *
#25/01/21
class CanDatas:
    def __init__ (self):
        br = [0] * 13
        #pour envoi vers serveur
        self.rfid = [56, 54,48,48,66,68,52,70,51,57,70]        
        self.points = 10        
        self.cause =6       
        
        #pour reception du serveur        
        self.equipe = 0
        self.joueurs = 4
        self.passage = 1
        self.points_precedents = 112
        self.record = 458
        
        self.pseudo = 'Les meilleur'
        
       
        
    def can_reception_autorisation(self):    
        br3 = f_canLecture(RX0)       
        self.equipe = br3[5]
        self.joueurs = br3[6]
        self.passages = br3[7]
        self.record = br3[9] * 256 + br3[10]
        self.points_precedents = br3[11] * 256 + br3[12]
        pseud =''
        br1 = f_canLecture(RX0)
        for i in range(8):
            pseud += chr(br1[i+5])
        br2 = f_canLecture(RX0)
        for i in range(8, 16):
            pseud += chr(br2[i-3])        
        pseu = pseud.strip()
        self.pseudo = pseu

    def can_envoi_rfid(self, rfid):
        self.be = [0] * 13
        self.be[0] = 1
        self.be[1] = 0x08 #id extend
        self.be[2] = 45 #salle emetrice 
        self.be[3] = 0 # destinataire serveur
        self.be[4] = 0x08 # longueur des datas                
        for j in range(8):
            self.be[j+5] = rfid[j]
        f_canEcriture(LTX0, self.be)
        """        for j in range(5, 13):
            self.be[j] = 0
        for j in range(8, 11):
            self.be[j-3] = rfid[j]        
        time.sleep(.01)
        f_canEcriture(LTX0, self.be)"""

    def can_envoi_fin(self, points, cause):    
        self.be = [0] * 13
        self.be[0] = 2
        self.be[1] = 0x08 #id extend
        self.be[2] = 45 #salle emetrice 
        self.be[3] = 0 # destinataire serveur
        self.be[4] = 0x08 # longueur des datas 
        self.be[5] = self.equipe
        self.be[6] = points//256       
        self.be[7] = points % 256
        self.be[8] = cause
        f_canEcriture(LTX0, self.be)


f_canINIT(5, 0, 1)
time.sleep(.1)
canDatas = CanDatas() #objet

abc = time.time()
for i in range(5):
    #time.sleep(.001)
    #canDatas.can_envoi_rfid(canDatas.rfid)
    #canDatas.can_reception_autorisation()
    #time.sleep(.01)
    canDatas.can_envoi_fin(canDatas.points, canDatas.cause)
    canDatas.points += 1
    canDatas.equipe += 1
    #canDatas.be[2] += 5
    canDatas.can_envoi_rfid(canDatas.rfid)
    #time.sleep(0.01)
print(f_canRegistreR(0x1d), f_canRegistreR(0x2d), i, f_canRegistreR(0x1c))
print(canDatas.pseudo, canDatas.equipe)#, canDatas.joueurs, canDatas.passages,canDatas.record, canDatas.points_precedents)
        
defg = time.time()
print( defg - abc)
#print(canDatas.pseudo, type(canDatas.pseudo))








