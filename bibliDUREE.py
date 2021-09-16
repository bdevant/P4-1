import time

class Duree:
    def __init__(self, hInit, duree):
        self.a_hInit = hInit
        self.a_duree = duree
        
    def m_duree(self, coeff=1):
        if time.time() < self.a_hInit + self.a_duree * coeff:
            return True
        else:
            return False   #temps écoulé
        
    def m_tempsEcoule(self):
        return (time.time() - self.a_hInit)# / self.a_duree