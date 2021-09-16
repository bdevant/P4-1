from tkinter import *
from bibliDUREE import *
from bibli_barre_temps import *
from Puissance4_debut_fin import *
from P4Datas import *
import time
import RPi.GPIO as GPIO
import random
import pygame
from PIL import ImageTk

#/28/08/21

pygame.init()
pygame.mixer.init()
dictPassages = {0 : "Premier", 1: "Deuxième", 2 : "Troisième"}
passages = 1

kling = pygame.mixer.Sound('sons_images/kling.wav')
cow = pygame.mixer.Sound('sons_images/cow.wav')
gong = pygame.mixer.Sound('sons_images/gong.wav')
#mambo = pygame.mixer.Sound('mambo.wav')
def f_son(fichier):
    pygame.mixer.Sound.play(fichier, loops=0)
    pygame.mixer.Sound.set_volume(fichier, 0.8)  

class Gpio():
    liste_pins_paniers = [16, 12, 20, 21, 22, 23, 24]
    dict_pins_paniers = {16:1, 12:2, 20:3, 21:4, 22:5, 23:6, 24:7}
    def __init__(self):
        pass
    def fm_init_gpio(self):
        #GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for j in Gpio.liste_pins_paniers:
            GPIO.setup(j, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class Fond():
    def __init__(self, canevas):    
        (r, g, b) = (255., 0., 0.)
        y = 0
        x_debut = 0.
        x_fin = 1922.
        for k in range(540):    
            canevas.create_line(int(x_debut), y, int(x_fin), y, fill = self.f_rgb(int(r), int(g), int(b)))
            y += 1
            x_debut  += 1.78
            x_fin  -= 1.78
            g += .45
            b += .45
   
        (r, g, b) = (255., 0., 0.)
        g= 0
        b= 0
        y = 1080
        x_debut = 0.
        x_fin = 1922.
        for k in range(540):    
            canevas.create_line(int(x_debut), y, int(x_fin), y, fill = self.f_rgb(int(r), int(g), int(b)))
            y -= 1
            x_debut  += 1.78
            x_fin  -= 1.78
            g += .455
            b += .455
  
        (r, g, b) = (255., 0., 0.)
        x = 0
        y_debut = 0.
        y_fin = 1080.

        for k in range(960):    
            canevas.create_line(x, int(y_debut), x, int(y_fin), fill = self.f_rgb(int(r), int(g), int(b)))
            x += 1
            y_debut  += .55
            y_fin  -= .55
            g += .25
            b += .25   

        (r, g, b) = (255., 0., 0.)
        x = 1920
        y_debut = 0.
        y_fin = 1080.
        for k in range(960):    
            canevas.create_line(x, int(y_debut), x, int(y_fin), fill = self.f_rgb(int(r), int(g), int(b)))
            x -= 1
            y_debut  += .55
            y_fin  -= .55
            g += .25
            b += .25         
    def f_rgb(self, r, g, b):
        return '#%02x%02x%02x' % (r,g,b)

class EcranSortieP4():
    def __init__(self, root):        
        f_son(gong)
        #root.overrideredirect(1)   #Plein ecran 1920 1080
        root.title("P4 SORTIE")
        self.canevas = Canvas(root, width = 1920, height = 1080 , bg = 'blue', borderwidth = 0)
        self.canevas.place(x = 0, y = 0)
        self.image10 = ImageTk.PhotoImage(file = "sons_images/fond bleu.jpeg")
        self.canevas.create_image(0, 0,image = self.image10, anchor = 'nw')
        self.canevas.update()
        centre = 960
        texte = 'Joueurs : ' + str(P4Datas.joueurs) + '         '  + '                   ' +  'Passages : ' + dictPassages[P4Datas.passages] 
        self.canevas.create_text(30, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'EQUIPE ' + str(P4Datas.numero_equipe)) 
        self.canevas.create_text(1830, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'SALLE 12')
        self.ovale = self.canevas.create_oval(centre-500, 70, centre+500, 190, fill="cornflower blue", outline='black', width=2)
        self.canevas.create_text(centre, 85, anchor='n', font=("times", 60, 'bold'), fill = 'black', text = 'LA PUISSANCE DU 4')
        self.canevas.create_text(centre, 400 , text = ('Vous avez gagné  ' +str(P4Datas.etoiles) + '  ETOILES'), anchor='center', font=('', 50, 'bold')) 
        
        if P4Datas.elimine_temps:
            h_alarme = 550
            l = 700
            h = 50
            self.canevas.create_rectangle(centre-l, h_alarme-h, centre+l, h_alarme+h, fill = 'red') 
            self.canevas.create_text(centre, 550 , text = ('ÉLIMINÉ : TEMPS DÉPASSÉ'), anchor='center', font=('', 50, 'bold'), fill='black')
        self.canevas.create_text(centre, 700 , text = ('Vous pouvez sortir'), anchor='center', font=('', 80, 'bold'))     
        self.canevas.update()
        time.sleep(5)
        self.canevas.destroy()
    

        
class EcranSortiePaniers():
    def __init__(self, root):        
        f_son(gong)
        #root.overrideredirect(1)   #Plein ecran 1920 1080
        root.title("P4 SORTIE")
        self.canevas = Canvas(root, width = 1920, height = 1080 , bg = 'blue', borderwidth = 0)
        self.canevas.place(x = 0, y = 0)
        self.image10 = ImageTk.PhotoImage(file = "sons_images/fond bleu.jpeg")
        self.canevas.create_image(0, 0,image = self.image10, anchor = 'nw')        
        centre = 960
        texte = 'Joueurs : ' + str(P4Datas.joueurs) + '         '  + '                   ' +  'Passages : ' + dictPassages[P4Datas.passages] 
        self.canevas.create_text(30, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'EQUIPE ' + str(P4Datas.numero_equipe)) 
        self.canevas.create_text(1830, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'SALLE 12')
        self.ovale = self.canevas.create_oval(centre-500, 70, centre+500, 190, fill="cornflower blue", outline='black', width=2)
        self.canevas.create_text(centre, 85, anchor='n', font=("times", 60, 'bold'), fill = 'black', text = 'LA PUISSANCE DU 4')
        self.canevas.create_text(centre, 400 , text = ('Vous avez gagné  ' +str(P4Datas.etoiles) + '  ETOILES'), anchor='center', font=('', 50, 'bold')) 
        
        #if P4Datas.elimine_temps:
            #self.canevas.create_text(centre, 550 , text = ('ELIMINE TEMPS DÉPASSE'), anchor='center', font=('', 50, 'bold'), fill='red')
        self.canevas.create_text(centre, 700 , text = ('Vous pouvez sortir'), anchor='center', font=('', 80, 'bold'))     
        self.canevas.update()
        time.sleep(5)
        self.canevas.destroy()

class Choix():
    def __init__(self, root):
        f_son(kling)
        root.overrideredirect(1)   #Plein ecran 1920 1080
        root.title("P4 choix")
        self.canvas = Canvas(root, width = 1920, height = 1080 , bg = 'blue', borderwidth = 0)
        self.canvas.place(x = 0, y = 0)#, width = 200, height = 300
        #Fond(self.canvas)


        self.image10 = ImageTk.PhotoImage(file = "sons_images/fond bleu.jpeg")
        self.canvas.create_image(0, 0,image = self.image10, anchor = 'nw')
        
        centre = 960
        texte = 'Joueurs : ' + str(P4Datas.joueurs) + '         '  + '                   ' +  'Passages : ' + dictPassages[P4Datas.passages] 
        self.canvas.create_text(30, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'EQUIPE ' + str(P4Datas.numero_equipe)) 
        self.canvas.create_text(1830, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'SALLE 12')
        self.ovale = self.canvas.create_oval(centre-500, 70, centre+500, 190, fill="cornflower blue", outline='black', width=2)
        self.canvas.create_text(centre, 85, anchor='n', font=("times", 60, 'bold'), fill = 'black', text = 'LA PUISSANCE DU 4')
        self.canvas.create_text(centre, 215, anchor='n', font=("", 40, 'bold', 'italic'), fill = 'blue', text = '"'+P4Datas.pseudo+'"')
        self.canvas.create_text(centre, 330, anchor='n', font=("", 30, 'bold'), fill = 'black', text = texte)
        
        marge_gauche = 280
        marge_centre = 930
        self.canvas.create_text(centre, 440, anchor='n', font=("", 40, 'bold'), fill = 'black', text = 'CHOIX DES OPTIONS')
        self.canvas.create_text(centre, 510, anchor='n', font=("", 30, 'bold'), fill = 'black', text = 'Lancer 1 ballon')

        self.canvas.create_text(marge_gauche, 600, anchor='nw', font=("", 30, 'bold'), fill = 'black', text = 'Ballon dans panier 1  :')
        self.canvas.create_text(marge_gauche, 690, anchor='nw', font=("", 30, 'bold'), fill = 'black', text = 'Ballon dans panier 3  :')
        self.canvas.create_text(marge_gauche, 780, anchor='nw', font=("", 30, 'bold'), fill = 'black', text = 'Ballon dans panier 5  :')
        self.canvas.create_text(marge_gauche, 870, anchor='nw', font=("", 30, 'bold'), fill = 'black', text = 'Ballon dans panier 7  :')
        self.canvas.create_text(marge_centre, 600, anchor='nw', font=("", 30, 'bold'), fill = 'blue', text = 'BASKET  niveau Explorateur')
        self.canvas.create_text(marge_centre, 690, anchor='nw', font=("", 30, 'bold'), fill = 'blue', text = 'BASKET  niveau Expert')
        self.canvas.create_text(marge_centre, 780, anchor='nw', font=("", 30, 'bold'), fill = 'blue', text = 'LA PUISSANCE DU 4  niveau Expert')
        self.canvas.create_text(marge_centre, 870, anchor='nw', font=("", 30, 'bold'), fill = 'blue', text = 'LA PUISSANCE DU 4  niveau Maître')
        self.barre_de_temps_opt = BarreDeTemps(self.canvas, 960, 960, P4Datas.duree_option, 72, 40)#   creation objet
        self.canvas.update()
        
#***********        
        self.numero_option = 0
        #for k in range(7):
            #GPIO.add_event_detect(Gpio.liste_pins_paniers[k], GPIO.RISING, callback = lambda arg = k: self.fm_choix_callback(arg), bouncetime=250)
            #print(k, 642,liste_pins_paniers[k] )
            
#******* BOUCLE OPTION
        temps_ecoule = 0
        duree_session_opt = Duree(time.time(), P4Datas.duree_option)   #OBJET        
        while duree_session_opt.m_duree() and self.numero_option == 0:# and f_porteFermee():
            if time.time() - duree_session_opt.a_hInit > temps_ecoule:
                temps_ecoule += 1                
                self.barre_de_temps_opt.fm_affichage_temps_ecoule(temps_ecoule)#(int(temps_ecoule))
            self.fm_panier_choix()
            f_urgences()   #ouverture porte et demandes bus can
            self.canvas.update()
            #root.bind('<Escape>', lambda e: root.destroy())
            
#********            
        if self.numero_option == 0:
            self.numero_option = 3
        print(642, self.numero_option)
        gpio1 = Gpio()
        #for ii in range(7):
            #GPIO.remove_event_detect(gpio1.liste_pins_paniers[ii])
        self.canvas.delete(self.image10)
        self.canvas.destroy()
        
    def fm_retour_option(self):
        return self.numero_option
    
    """def fm_choix_callback(self, numero_choix):
        print(123, numero_choix)
        gpio = Gpio()
        self.numero_option = Gpio.dict_pins_paniers[numero_choix]
        print(456, self.numero_option)
        for ii in range(7):
            GPIO.remove_event_detect(gpio.liste_pins_paniers[ii])"""

    def fm_panier_choix(self):
        i = 0
        while i < 7:
            if (GPIO.input(Gpio.liste_pins_paniers[i]) == 0):
                time.sleep(0.05)
                if (GPIO.input(Gpio.liste_pins_paniers[i]) == 0):
                    while GPIO.input(Gpio.liste_pins_paniers[i]) == 0:
                        pass
                    self.numero_option = i + 1 
            i += 1
        #print(i)
        #print(456, self.numero_option)
        
class Option1_2():
    """basket explorateur"""    
    def __init__(self, opt, root):
        f_son(kling)
        print(opt)
        self.opt = opt
        self.liste_total_panier = [0] * 8
        self.liste_masque_panier = [False] * 8
        self.liste_masque_false = [False] * 8
        #root.overrideredirect(1)   #Plein ecran 1920 1080
        root.title("P4 option1")
        self.canvas = Canvas(root, width = 1920, height = 1080 , bg = 'blue')#, borderwidth = 10, relief = 'ridge')
        self.canvas.place(x = 0, y = 0)#, width = 200, height = 300
        self.canvas.update()
        self.image101 = ImageTk.PhotoImage(file = "sons_images/fond bleu.jpeg")
        self.canvas.create_image(0, 0,image = self.image101, anchor = 'nw')        
        centre = 960
        texte = 'Nombre de Joueurs : ' + str(P4Datas.joueurs) + '         ' +  'Passage : ' + dictPassages[P4Datas.passages]
        self.canvas.create_text(30, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'EQUIPE ' + str(P4Datas.numero_equipe))         
        self.canvas.create_text(1830, 20, anchor='nw', font=("", 10, 'bold'), fill = 'white', text = 'SALLE 12')
        self.ovale = self.canvas.create_oval(centre-500, 70, centre+500, 190, fill="cornflower blue", outline='black', width=2)
        self.canvas.create_text(centre, 85, anchor='n', font=("times", 60, 'bold'), fill = 'black', text = 'LA PUISSANCE DU 4')
        self.canvas.create_text(centre, 215, anchor='n', font=("", 40, 'bold', 'italic'), fill = 'blue', text = '"'+P4Datas.pseudo+'"')
        self.canvas.create_text(centre, 310, anchor='n', font=("", 30, 'bold'), fill = 'black', text = texte)        
        self.op = self.canvas.create_text(centre, 380, anchor='n', font=("", 40, 'bold'), fill = 'black', text = 'Option : BASKET Explorateur')
        if self.opt == 3:
            self.canvas.itemconfigure(self.op, text= 'Option : Basket Expert')
#******
        ytot = 850
        self.canvas.create_rectangle(220, ytot, 830, ytot+50, fill = 'medium sea green', width=2) 
        self.tot_pan = self.canvas.create_text(230, ytot+2, anchor='nw', font = ('', 30, 'bold'), text = 'TOTAL1')
        self.canvas.create_rectangle(1100, ytot, 1704, ytot+50, fill = 'medium sea green', width=2) 
        self.tot_points = self.canvas.create_text(1114, ytot+2, anchor='nw', font = ('', 30, 'bold'), text = 'TOTAL2')
               
        self.index_tk_rectangle = [0] * 8
        x0 = 220
        y0 = 520
        for valide in range(1, 8):
            x = x0 + (valide - 1) * 218        
            if valide % 2 == 0:
                y = y0
            else:
                y = y0 + 100                
            self.index_tk_rectangle[valide] = self.canvas.create_rectangle(x, y, x + 176, y+140, fill = 'red2', width=2)
            self.canvas.create_text(x+5, y+10, anchor='nw', font = ('', 30), text = "panier " +str(valide))
           
        x0 =333
        y0 = 600        
        self.index_tk_paniers = [0]*8
        for i in range(1, 8):
            if i % 2 == 0:
                y = y0
            else:
                y = y0 + 100
            self.index_tk_paniers[i] = self.canvas.create_text(x0 + (i - 1) *218, y, anchor='ne', font = ('', 30), text = "zzzz")
#*******        
        self.barre_de_temps = BarreDeTemps(self.canvas, 960, 960, P4Datas.duree_session_1, 8, 40)#   creation objet
        #self.canvas.update()
        #time.sleep(3)
        if self.opt == 1:
            self.liste_masque_panier = [True] * 8
        else:
            self.fm_aleatoire(P4Datas.joueurs)
        
        
        
        #self.inhib_panier = Duree(time.time(), 1) #OBJETS
        self.l_inhib_panier =  [Duree(time.time(), 1)]  * 7  
            
#****** BOUCLE PANIERS
        
        temps_ecoule = 0
        #session_en_cours = True
        duree_session = Duree(time.time(), P4Datas.duree_session_1)   #OBJET        
        while duree_session.m_duree():# and f_porteFermee():
            if time.time() - duree_session.a_hInit > temps_ecoule:
                temps_ecoule += 1
                self.barre_de_temps.fm_affichage_temps_ecoule(int(temps_ecoule))
            self.fm_panier()                
            self.fm_affiche()
            self.canvas.update()
            f_urgences()  #ouverture porte et demandes bus can
            #self.canvas.itemconfigure(self.ovale, fill='yellow')
            
#******FIN OPTION 1-2               
        #for ii in range(7):
            #GPIO.remove_event_detect(Gpio.liste_pins_paniers[ii])
        #f_son(gong)
        EcranSortiePaniers(root)
        #time.sleep(4)    
        self.canvas.destroy()
        

    def fm_affiche(self):
        for valide in range(1, 8):
            if self.liste_masque_panier[valide]:
                self.canvas.itemconfigure(self.index_tk_rectangle[valide], fill = 'medium sea green', width=2)
            else:
                self.canvas.itemconfigure(self.index_tk_rectangle[valide], fill = 'red2', width=2)
                
        self.liste_total_panier[0] = 0
        for i in range(1, 8):
            self.canvas.itemconfigure(self.index_tk_paniers[i], text = str(self.liste_total_panier[i]))
            self.liste_total_panier[0] += self.liste_total_panier[i]        
        self.canvas.itemconfigure(self.tot_pan, text = 'TOTAL DES PANIERS :  ' + str(self.liste_total_panier[0]))
        P4Datas.etoiles = self.liste_total_panier[0] // 5
        self.canvas.itemconfigure(self.tot_points, text = 'TOTAL DES ETOILES :  ' + str(P4Datas.etoiles))


    def fm_aleatoire(self,nombre, parmi = 7):
        su = [0]*0
        while (len(su)  < nombre):
            a =random.randrange(1, parmi + 1)
            if a not in su:
                su.append(a)
        for ik in su:
            self.liste_masque_panier[ik] = True
        return su               


    """def fm_panier_callback(self, numero_pin):
        self.ind_paniers = Gpio.dict_pins_paniers[numero_pin]
        if self.liste_masque_panier[self.ind_paniers] == True:
            self.liste_total_panier[self.ind_paniers] += 1
            f_son(kling)
            if self.opt == 3:
                self.liste_masque_panier[self.ind_paniers] = False
                if self.liste_masque_panier == self.liste_masque_false:
                    self.fm_aleatoire(P4Datas.joueurs)                
        else:
            self.liste_total_panier[self.ind_paniers] -= 2
            f_son(cow)
            #print(ind_paniers, liste_total_panier, 1001)"""

    def fm_panier(self):
        i = 0
        self.ind_paniers = 0
        while i < 7:
            if not self.l_inhib_panier[i].m_duree():
                if (GPIO.input(Gpio.liste_pins_paniers[i]) == 0):
                    time.sleep(0.05)
                    if (GPIO.input(Gpio.liste_pins_paniers[i]) == 0):
                        while GPIO.input(Gpio.liste_pins_paniers[i]) == 0:
                            pass
                        self.l_inhib_panier[i] = Duree(time.time(), 3) #OBJET    
                        self.ind_paniers = i + 1 
            #i += 1
                        #time.sleep(.5)
                        if self.liste_masque_panier[self.ind_paniers] == True:
                            self.liste_total_panier[self.ind_paniers] += 1
                            f_son(kling)
                            if self.opt == 3:
                                self.liste_masque_panier[self.ind_paniers] = False
                                if self.liste_masque_panier == self.liste_masque_false:
                                    self.fm_aleatoire(P4Datas.joueurs)                
                        else:
                            self.liste_total_panier[self.ind_paniers] -= 1
                            f_son(cow)
                        time.sleep(.1)
            i += 1           #print(ind_paniers, liste_total_panier, 1001)1

def f_urgences():
        P4Datas.elimine_porte = True
        #print(2021, P4Datas.elimine_porte)
   
        
#******************************
"""
joueurs = 2      
niveau = 1
passages = 0
dictNiveau = {0 : "Espoir", 1: "Expert", 2 : "Maître"}
dictPassages = {0 : "Premier", 1: "Deuxième", 2 : "Troisième"}
numero_option = 0


gp = Gpio()
gpi.fm_init_gpio()
root1_2 = Tk()
Choix()
print(numero_option, 5000)
if numero_option == 1:
    Option1_2(1)
elif numero_option == 2:
    Option1_2(2)
elif numero_option == 3:
    Option1_2(3)
else :
    Option1_2(4)
f_son(gong)   
#fin programme"""
"""    
root = Tk()
#self.root.overrideredirect(1)   #Plein ecran 1920 1080
root.title("tk")
root.geometry("1920x1080")  #"800x700+1100+200")
                
fenetreLargeur, fenetreHauteur = 1700, 100# 1920, 1080
canvas = Canvas(root, width = fenetreLargeur, height =fenetreHauteur, bg = 'white')
 
canvas.place(x = 10, y = 10)#, width = 200, height = 300)

def f_rgb(tup):
    return '#%02x%02x%02x' % (tup)"""
"""
cr = 255
cg = 255
cb = 255
couleur = cr, cg, cb
for i in range(1, 128):
    cr = 255
    cg = 0 + 2 * i
    cb = 0 + 2 * i
    couleur = (cr, cg, cb)
    canvas.create_line(0, 5 * i, 1600, 5 * i, fill = f_rgb(couleur), width = 5)"""
"""
x0 = -70
y0 = 10
longueur = 65
hauteur = 65
for i in range(900):
    canvas.create_rectangle(x0 + longueur - 2, y0, x0 + longueur, y0 + hauteur, fill = 'red', width = 0)
    canvas.update()
    canvas.create_rectangle(x0, y0, x0 + 2, y0 + hauteur, fill = 'white', width = 0)
    x0 += 2
    time.sleep(0.0001)"""



"""
cr = 200
cg = 200
cb = 250
tuc =(cr, cg, cb)
gris = (50, 50, 50)

def f_rgb(r, g, b):
    return '#%02x%02x%02x' % (r,g,b)

def f_rgb_tuc(tuc):
    return '#%02x%02x%02x' % (tuc)

print(f_rgb(100, 100, 100))
print(f_rgb_tuc((60, 60, 60)))

ma_couleur = '#%02x%02x%02x' % (tuc)
print(ma_couleur)
print(tuc)

root = Tk()
#self.root.overrideredirect(1)   #Plein ecran 1920 1080
root.title("tk")
root.geometry("1920x1080")  #"800x700+1100+200")

root.option_add('*Font', 'Times, 30')
                
fenetreLargeur, fenetreHauteur = 1700, 800# 1920, 1080
canvas = Canvas(root, width = fenetreLargeur, height =fenetreHauteur, bg = f_rgb(250,200,200))
canvas2 = Canvas(root, width = 50, height = 50,bg = 'yellow')
#canvas.grid(row=0, column = 0, sticky=(N, W, E, S))
#anvas.pack()
canvas.place(x = 10, y = 10)#, width = 200, height = 300)
canvas2.place(x = 500, y = 100)

canvas.create_line(0,0,600,600, fill = 'red', width = 5)
canvas.create_line(600,600,700,700, fill = 'red', width = 1)
canvas.create_rectangle(100,100, 400,300, outline = 'yellow', width = 1, fill = 'grey80')
canvas.create_oval(1000,100, 1500, 600, outline = 'yellow', width = 30, fill = 'orchid2')
canvas.create_oval(1000,100, 1500, 600, outline = 'black', width = 1)

co = canvas.create_text(100, 100, anchor='nw', font=("Times"), fill = 'red', text = 'BONNEnuitiiimm')
#canvas.itemconfigure(co, font=("",40))
co = canvas.create_text(100, 160, text = str(cb), anchor='nw', fill = 'red')#, font=("", 50))
co = canvas2.create_text(25, 10, text = 'bonjour', fill = 'black', font=("", 10))

b = ttk.Label(canvas, text = 'marche ARRET MARCHE', foreground='white', background='black', font=('', 40, 'bold', 'italic'))
canvas.create_window(400, 400, window = b)

style = ttk.Style()
style.configure("n.TButton", foreground="yellow", background="black", font=('Purisa'))#,20, 'bold', 'italic'))
f= ttk.Button(canvas, text = 'ARRET IIIIMARCHE', style="n.TButton")
canvas.create_window(800, 500, window = f)

value = 0
c = ttk.Progressbar(canvas, orient=HORIZONTAL, length=1200, variable=value, maximum=100, mode ='determinate')
canvas.create_window(700, 700, window=c)
c["value"] = 20

e = ttk.Progressbar(canvas, orient=HORIZONTAL, length=1200, variable=value, maximum=100, mode ='determinate')
canvas.create_window(700, 717, window=e)
e["value"] = 20

value = 0
d = ttk.Scale(canvas, orient=HORIZONTAL, length=600, variable=value)
canvas.create_window(700, 750, window=d)
d["value"] = .5



                               

root.update()
print(100)
time.sleep(1)


class Quiz9():
    def __init__(self):
        self.root = Tk()
        #self.root.overrideredirect(1)   #Plein ecran
        self.root.title("QUIZ9")
                
        self.fenetreLargeur, self.fenetreHauteur = 1920, 1080#self.fenetreHauteur = 1080
        self.fen9Largeur, self.fen9Hauteur = self.fenetreLargeur // 3, self.fenetreHauteur // 3
        self.ecran = Canvas(self.root, width = self.fenetreLargeur, height = self.fenetreHauteur, bg = 'white')
        self.ecran.grid(row=0, column = 0, sticky=(N, W, E, S))
        
        self.l_ambo = ['z_ambo0.jpg', 'z_ambo1.jpg', 'z_ambo2.jpg']
        self.l_azay = ['z_azay0.jpg', 'z_azay1', 'z_azay2']
        self.l_bloi = ['z_bloi0.bmp', 'z_bloi1', 'z_bloi2']
        self.l_chat = [self.l_ambo, self.l_azay, self.l_bloi]#, l_cham, l_chau, l_chen, l_chi, l_lang, l_usse, l_vill]
             
    def f_aleatoire(self, nombre, parmi):
        su = []
        while (len(su)  < nombre):
            a =random.randrange(0, parmi)
            if a not in su:
                su.append(a)
        return su               

    def f_selection(self, selection):
        dicPos = {0:0, 1:1, 2:2, 3:5, 4:8, 5:7, 6:6, 7:3}
        
        self.f_traceCadre(dicPos[(selection-1) % 8],'grey')
        #if selection != 4:
        self.f_traceCadre(dicPos[selection % 8],'yellow')

    def f_traceCadre(self,position, couleur):
        x0 = (position % 3) * self.fen9Largeur
        y0 = (position // 3) * self.fen9Hauteur
        self.ecran.create_rectangle(x0, y0+2, x0 + 640-3, y0 + 360-3, width = 6, outline = couleur)
        self.root.update()

    def f_affiche(self, l_photos2):
        self.l_image = [0]*len(l_photos2)
        for indexImage in range (len(self.l_image)):
            x2 = (indexImage % 3) * self.fen9Largeur
            y2 = (indexImage // 3) * self.fen9Hauteur
            if indexImage != 4:
                self.l_image[indexImage] = ImageTk.PhotoImage(file = l_photos2[indexImage])
                self.ecran.create_image((indexImage % 3) * self.fen9Largeur, (indexImage // 3) * self.fen9Hauteur, image = self.l_image[indexImage], anchor = 'nw')
            else:
                #print(100)
                self.ecran.create_rectangle(640, 360, 1280,720, fill = 'white')
        #self.ecran.create_text(750, 400, text = s_ale, font = ('', 200), fill = 'red')
            self.f_traceCadre(indexImage, 'grey')
        self.root.update()
        time.sleep(.5)
        
    def f_blanc(self, duree):
        self.ecran.create_rectangle(0, 0, self.fenetreLargeur, self.fenetreHauteur, fill = 'white')
        self.root.update()
        time.sleep(duree)
        
#print(1000)
quizObjet = Quiz9()
#s_ale = quizObjet.f_aleatoire(3, 3)
#print(s_ale)

l_photos = ['/media/pi/EMTEC B250/z_bloi0.bmp'] * 9# + ['z_ambo0.jpg'] * 3
quizObjet.f_affiche(l_photos)
#dicPos = {0:0, 1:1, 2:2, 3:5, 4:8, 5:7, 6:6, 7:3}
pos = 0
while pos < (32):
    #print(pos)
    quizObjet.f_selection(pos)
    #print(pos % 8, dicPos[pos % 8])
    pos += 1
    time.sleep(.6)
    """





