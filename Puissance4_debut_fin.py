from bibliCAN import *
from can2_rfid import *
from P4Datas import *

#Puissance4_debut_fin

class CanDatas:
    def __init__ (self):
        br = [0] * 13
        #pour envoi vers serveur
        """self.rfid = [10,20,30,40,50]        
        self.points = 10        
        self.cause =6  """     
        
        #pour reception du serveur        
        """self.equipe = 2
        self.joueurs = 18
        self.passage = 1"""
        self.points_precedents = 112
        self.record = 458
        
        #self.pseudo = 'Les meilleur'
        
       
        
    def can_reception_autorisation(self):    
        br3 = f_canLecture(RX0)
        P4Datas.autorisation = br3[5]
        P4Datas.equipe = br3[6]
        P4Datas.joueurs = br3[7]
        P4Datas.passages = br3[8]
        #self.record = br3[9] * 256 + br3[10]
        #self.points_precedents = br3[11] * 256 + br3[12]
        
    def can_reception_pseudo(self):
        pseud =''
        br1 = f_canLecture(RX0)
        for i in range(8):
            pseud += chr(br1[i+5])
        br2 = f_canLecture(RX0)
        for i in range(8, 16):
            pseud += chr(br2[i-3])        
        pseu = pseud.strip()
        P4Datas.pseudo = pseu

    def can_envoi_rfid(self, rfid):
        self.be = [0] * 13
        self.be[0] = 1
        self.be[1] = 0x08 #id extend
        self.be[2] = 45 #salle emetrice 
        self.be[3] = 0 # destinataire serveur
        self.be[4] = 0x08 # longueur des datas                
        for j in range(5):
            self.be[j+5] = rfid[j]
        print(self.be)
        f_canEcriture(LTX0, self.be)
        

    def can_envoi_fin(self, points, cause):    
        self.be = [0] * 13
        self.be[0] = 2
        self.be[1] = 0x08 #id extend
        self.be[2] = 45 #salle emetrice 
        self.be[3] = 0 # destinataire serveur
        self.be[4] = 0x08 # longueur des datas 
        self.be[5] = P4Datas.numero_equipe
        self.be[6] = points//256       
        self.be[7] = points % 256
        self.be[8] = cause
        print(self.be)
        f_canEcriture(LTX0, self.be)
        
def f_ouverure_gache():
    pass

def f_porte_fermee():
    pass

def f_debut_session():
    print(P4Datas.pseudo)
    f_canINIT()#(5, 0, 1)
    f_initGpioRfid()
    time.sleep(.1)
    canDatas = CanDatas() #objet
    autorisation_serveur = False
    """while autorisation_serveur == False:
        P4Datas.rfid = f_can_rfid()
        print(P4Datas.rfid)
        #led verte cligno rapide
        canDatas.can_envoi_rfid(P4Datas.rfid)
        #canDatas.can_reception_autorisation()
        if P4Datas.autorisation == True:
            autorisation_serveur = True
            print(autorisation_serveur)"""
    print("session autorisée")
    #canDatas.can_reception_pseudo()
    #led verte allumee
    #eclairage ambiance
    f_ouverure_gache()
    if f_porte_fermee():
        pass
    if not f_porte_fermee():
        pass
    
def f_fin_session():
    pass

"""

f_canINIT()#(5, 0, 1)
f_initGpioRfid()
time.sleep(.1)
canDatas = CanDatas() #objet

#canDatas.can_envoi_rfid(canDatas.rfid)
#canDatas.can_reception_autorisation()
#canDatas.can_envoi_fin(canDatas.points, canDatas.cause)
f_debut_session()"""

