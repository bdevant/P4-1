from tkinter import *
from Puissance4_paniers import *
import time

#28/08/21

pygame.init()
"""
c0 = [0,0,0,0,0,0]
c1 = [0,0,0,0,0,0]
c2 = [0,0,0,0,0,0]
c3 = [0,0,0,0,0,0]
c4 = [0,0,0,0,0,0]
c5 = [0,0,0,0,0,0]
c6 = [0,0,0,0,0,0]
t_grille = [c0,c1,c2,c3,c4,c5,c6]"""

t_grille = [[0] * 6 for k in range(7)]

JETONROUGE = 1
JETONJAUNE = 2
grillePleine = False
places_libres = 42
gpi = Gpio()
gpi.fm_init_gpio()
PORT = Gpio.liste_pins_paniers

#******************************************************************************
class P4P4():
    def puissance4H(self, li, couleurJeton):
        p4 = 0
        col = 0
        retour = False
        while col < 7:
            if t_grille[col][li] != couleurJeton :
                p4 = 0
            else:
                p4 += 1
                if p4 > 3:
                    print("HOR")
                    retour = True
            col += 1
        return(retour)
            

    def puissance4V(self, col, couleurJeton):
        p4 = 0
        li = 0
        retour = False
        while li < 6:
            if t_grille[col][li] != couleurJeton:
                p4 = 0
            else:
                p4 += 1
                if p4 > 3:
                    print("VER")
                    retour = True
            li += 1
        return(retour)

    def puissance4DiagM(self, col,li, couleurJeton):
        p4 = 0
        retour = False
        if col + li < 6:
            li += col 
            col = 0
            while li > -1:
                if t_grille[col][li] != couleurJeton:
                    #print(150,col, li)
                    p4 = 0
                else:
                    p4 += 1
                    #print(151, col, li)
                    if p4 > 3:
                        print("DIAG M SUP")                    
                        retour =True
                li -= 1
                col += 1
        else :
            col = col + li - 5 
            li = 5
            while col < 7 :
                if t_grille[col][li] != couleurJeton:
                    #print(120, col, li)
                    p4 = 0
                else:
                    p4 += 1
                    #print(121, col, li)                
                    if p4 > 3:
                        print("DIAG M INF")                    
                        retour = True
                col += 1
                li -= 1       
          
        return(retour)
            
    def puissance4DiagD(self, col, li, couleurJeton):
        p4 = 0
        retour = False
        if col - li > 0:
            col = col - li
            li = 0
            while col < 7:
                if t_grille[col][li] != couleurJeton:
                    #print(10,col, li)
                    p4 = 0
                else:
                    p4 += 1
                    #print(11, col, li)
                    if p4 > 3 :
                        print("DIAG D SUP")                    
                        retour =True
                li += 1
                col += 1
        else:
            li -= col
            col = 0
            while li < 6 :
                if t_grille[col][li] != couleurJeton:
                    #print(20, col, li)
                    p4 = 0
                else:
                    p4 += 1
                    #print(21, col, li)                
                    if p4 > 3:
                        print("DIAG D INF")                    
                        retour = True
                li += 1
                col += 1        
          
        return(retour) 
    
    def fm_puissance4(self, col, li, cj):    
        if ((self.puissance4H(li, cj) == False) and (self.puissance4V(col, cj) == False) and \
            (self.puissance4DiagM(col, li, cj) == False) and (self.puissance4DiagD(col, li, cj) == False)):
            return(False)
        else:
            return True    
#******************************************************************************

def f_cercle(canevas, x, y, r, couleur = "", identite="base",ligne_ext="blue", epaisseur = 2):
    id = canevas.create_oval(x+r, y+r, x-r, y-r, fill=couleur, tags=identite, outline=ligne_ext, width=epaisseur)  
    return id

class Grille():
    def __init__(self, canevas):
        self.canevas = canevas
        self.image10 = ImageTk.PhotoImage(file = "sons_images/fond bleu.jpeg")
        self.canevas.create_image(0, 0,image = self.image10, anchor = 'nw')
        #self.canevas.create_rectangle(self.x0+35, self.y0-2, self.x0-35+self.largeurGrille, self.y0+2+self.hauteurGrille, fill = 'white', width=0)         
  
        self.module = 140
        self.rayon = 62
        self.r1 = 70
        self.r2 = 60
        self.bordureLaterale = 60
        self.bordureHaute = 20
        self.bordureBasse = 20
        self.largeurGrille = 6*self.module + 2*self.rayon + 2*self.bordureLaterale
        self.hauteurGrille = 5*self.module + 2*self.rayon + self.bordureHaute + self.bordureBasse

        self.x0 = (1920 - self.largeurGrille) //2 #415  #coordonnees ecran (haut gauche grille)
        self.y0 = 60 
        self.x2 = self.x0 + self.bordureLaterale + self.rayon #coordonnees ecran (trou haut gauche)
        self.y2 = self.y0 + self.bordureHaute + self.rayon
        self.x1 = self.bordureLaterale + self.rayon #coordonnees grille (trou haut gauche)
        self.y1 = self.bordureHaute + self.rayon
        self.canevas.create_rectangle(self.x0+35, self.y0-2, self.x0-35+self.largeurGrille, self.y0+2+self.hauteurGrille, fill = 'light goldenrod yellow', width=0)         
        
        self.texto = self.canevas.create_text(30, 100, text="a", anchor='w', font=('', 25, 'bold'))
        self.texto2 = self.canevas.create_text(30, 150, text=str(42), anchor='w', font=('', 25, 'bold'))
        #self.elimine_temps = canevas.create_text(30, 200, text="", anchor='w', font=('', 25, 'bold'))
        self.elimine = canevas.create_text(30, 200, text="", anchor='w', font=('', 25, 'bold'))


    def fm_dessin(self, opt):
        iLi = 0
        iCo = 0
        #self.canevas.create_rectangle(self.x0+35, self.y0-2, self.x0-35+self.largeurGrille, self.y0+2+self.hauteurGrille, fill = 'light goldenrod yellow', width=0)         
  
        while iCo < 7:
            while iLi < 6:
                cercle1 = f_cercle(self.canevas, self.x2+self.module*iCo, self.y2+ self.module* iLi, self.r1, ligne_ext= 'blue2', epaisseur=20)
                iLi += 1
            iCo += 1
            iLi = 0
        iCo = 0; iLi = 0
        while iCo < 8:
            while iLi < 7:
                cercle1 = f_cercle(self.canevas, self.x2+self.module*iCo-self.module//2, self.y2+ self.module* iLi-self.module//2, 32, ligne_ext= '', epaisseur=0, couleur='blue2') 
                iLi += 1
            iCo += 1
            iLi = 0
        self.canevas.create_rectangle(self.x0+35, self.y0-2, self.x0-35+self.largeurGrille, self.y0+2+self.hauteurGrille, outline='blue2', width=35)         
        centre = 960
        h = 80
        y_v = 200
        of = 740
        self.ovale1 = self.canevas.create_oval(centre-of-200, y_v-h, centre-of+200, y_v+h, fill="cornflower blue", outline='black', width=2)
        self.canevas.create_text(centre-of, y_v + 10, fill = 'black', text='LA PUISSANCE\nDU 4', font=('', 30, 'bold'), justify='center')
        if opt == 5:
            texte_niveau = 'NIVEAU\nEXPERT'
        else:
            texte_niveau = 'NIVEAU\nMAÎTRE'
        self.ovale2 = self.canevas.create_oval(centre+of-200, y_v-h, centre+of+200, y_v+h, fill="cornflower blue", outline='black', width=2)
        self.canevas.create_text(centre+of, y_v + 10, fill = 'black', text=texte_niveau, font=('', 30, 'bold'), justify='center')
        y_v = 760
        self.ovale3 = self.canevas.create_oval(centre-of-200, y_v-h, centre-of+200, y_v+h, fill="cornflower blue", outline='black', width=2)
        self.canevas.create_text(centre-of, y_v + 10, fill = 'black', text=P4Datas.pseudo, font=('', 30, 'bold'), justify='center')
        self.ovale4 = self.canevas.create_oval(centre+of-200, y_v-h, centre+of+200, y_v+h, fill="lime green", outline='black', width=2)
        self.texte_ovale4 = self.canevas.create_text(centre+of, y_v + 10, fill = 'black', text='Jouer', font=('', 30, 'bold'), justify='center')
    



        self.canevas.update()
        time.sleep(1)
        
        #self.canevas.itemconfigure('jet_rouge', fill='grey')
        #self.canevas.update()
        #time.sleep(1)
        #self.canevas.delete('jet_rouge')
        #self.canevas.delete('jet_jaune')
        """t_grille[0][5] = 1
        t_grille[1][4] = 2
        t_grille[5][1] = 2
        print(t_grille)"""
        
    def fm_texte_ovale4(self,texte, couleur_bg):
        self.canevas.itemconfigure(self.texte_ovale4, text = texte)
        self.canevas.itemconfigure(self.ovale4, fill = couleur_bg)                
        
    def fm_jetons(self, col, li, couleur, iden='pions'):
        #print(iden)
        if couleur == JETONROUGE:
            coul = 'red2'
            couleur_f = 'red3'
        else:
            coul = 'yellow'
            couleur_f = 'yellow3'
        f_cercle(self.canevas, self.x2+self.module*col, self.y2+self.module*li, self.r2, couleur=coul, identite=iden)
        f_cercle(self.canevas, self.x2+self.module*col, self.y2+self.module*li, self.r2-20, ligne_ext=couleur_f, epaisseur=8, identite=iden)
        f_cercle(self.canevas, self.x2+self.module*col, self.y2+self.module*li,  5, ligne_ext=couleur_f, epaisseur=5, identite=iden) 
        self.canevas.update()

    def fm_raz_grille(self):
        iLi = 0; iCo = 0
        while iCo < 7:
            while iLi < 6 :
                t_grille[iCo][iLi] = 0
                iLi += 1
            iCo += 1; iLi = 0
        #self.fm_delete('pions')
        self.canevas.delete('pions')
        self.canevas.update()    
            

    def fm_descente_jeton(self,iCo, iLi, couleur):
        print(6666, iCo, iLi, couleur)
        f_son(kling)
        if couleur == JETONROUGE:
            id_jeton = 'jet_rouge'
        else:
            id_jeton = 'jet_jaune'
            time.sleep(.4)
            f_son(kling)
        self.canevas.move(id_jeton, self.module*iCo, 0)
        for i in range((iLi+2)*14):        
            self.canevas.move(id_jeton, 0,10)
            time.sleep(.008)#vitesse descente
            self.canevas.update()        
        self.fm_jetons(iCo, iLi, couleur)
        self.canevas.move(id_jeton, -self.module*iCo, -(iLi+2)*self.module)         
        self.canevas.update()
    
    def fm_jeton_colonne(self, col, couleur):
        global t_grille
        global grillePleine
        global places_libres
        obp4 = P4P4()
        iLi = 5
        while t_grille[col][iLi] != 0:
            iLi -=1
            if iLi < 0:
                return(False)          
        self.fm_descente_jeton(col, iLi, couleur)
        t_grille[col][iLi] = couleur
        places_libres = places_libres - 1
        if places_libres <= 30:
            grillePleine = True
            print(places_libres)
            print(grillePleine)
        
        pu = obp4.fm_puissance4(col, iLi, couleur)
        if pu:
            if couleur == JETONROUGE:
                print("gagne rouge")
                self.canevas.itemconfigure(self.texto, text = "GAGNE ROUGE")
                self.fm_texte_ovale4('GAGNÉ ROUGE\nSTOP', 'red')
                
                P4Datas.gagne_rouge = True
                self.canevas.update()
                time.sleep(4)
                self.fm_raz_grille()
                places_libres = 42
            else:
                print("gagne jaunej")
                f_son(cow)
                self.canevas.itemconfigure(self.texto, text = "GAGNE JAUNE")
                self.fm_texte_ovale4('GAGNÉ JAUNE\nREJOUER', 'YELLOW') 
                print(999)
                self.canevas.update()
                time.sleep(2)
                self.canevas.itemconfigure(self.texto, text = "")
                self.canevas.update()
                time.sleep(2)
                self.fm_raz_grille()
                self.fm_texte_ovale4('REJOUER', 'lime green') 
                places_libres = 42
                self.canevas.update()
            #time.sleep(3)
        self.canevas.itemconfigure(self.texto2, text = str(places_libres))
        #self.canevas.update()
        print(555, places_libres, grillePleine)    
        return(True)

    def fm_test_jetonColonne(self, col,couleur):
        global t_grille
        obp4 = P4P4()
        iLi = 5
        while t_grille[col][iLi] != 0:
            iLi -=1
            if iLi < 0:
                return(False, False, iLi)          
        t_grille[col][iLi] = couleur
        pu = obp4.fm_puissance4(col, iLi, couleur)      
        return (True, pu, iLi)

    def fm_test(self,opt):
        securite = False; puissance4 = False; li = 0
        print(1942, opt)

        u = 0
        while u < 7 and opt == 7:
            securite, puissance4, li = self.fm_test_jetonColonne(u, JETONJAUNE)
            if securite :
                t_grille[u][li] = 0
            if puissance4 == True:
                self.fm_jeton_colonne(u, JETONJAUNE)
                return
            u += 1
        k = 1
        while (self.fm_jeton_colonne(random.randrange(0,7),JETONJAUNE) == False) and (k < 50):
            k += 1
            print("securiteJaune")
                      
    def fm_paniers(self,opt):#(termine):
        i = 0
        jetonRougeRefuse = False
        while i < 7:
            if (GPIO.input(PORT[i]) == 0):
                time.sleep(0.05)
                if (GPIO.input(PORT[i]) == 0):
                    while GPIO.input(PORT[i]) == 0:
                        pass
                    if (self.fm_jeton_colonne(i, JETONROUGE) == False):
                        jetonRougeRefuse = True                                        
                        print("securite rouge")                
                    time.sleep(.1)
                    if (P4Datas.gagne_rouge == False) and (jetonRougeRefuse == False):
                        self.fm_test(opt)
            i += 1

def f_option3(opt, root):
    f_son(kling)
    P4Datas.elimine_temps = False
    #root.overrideredirect(1)   #Plein ecran 1920 1080
    root.title("PUISSANCE 4")
    #root1_2.geometry("1920x1080")  #"800x700+1100+200")
    canevas = Canvas(root, width = 1920, height = 1080 , bg =  'light goldenrod yellow')#, borderwidth = 10, relief = 'ridge')
    canevas.place(x = 0, y = 0)                
    ob = Grille(canevas)
    ob.fm_jetons(0, -2, JETONROUGE, iden='jet_rouge') #objets jeton derriere grille
    ob.fm_jetons(0, -2, JETONJAUNE, iden='jet_jaune')
    ob.fm_dessin(opt) 
    barre_de_temps_p4 = BarreDeTemps(canevas, 960, 1010, P4Datas.duree_p4, 8, 40)#   creation objet
#******* BOUCLE P4
    temps_ecoule = 0
    duree_session_p4 = Duree(time.time(), P4Datas.duree_p4)   #OBJET
    while ( P4Datas.elimine_temps == False) and (P4Datas.gagne_rouge == False):# and (P4Datas.elimine_porte == False):        
            if duree_session_p4.m_duree() == False: 
                P4Datas.elimine_temps = True
            ob.fm_paniers(opt)
            if time.time() - duree_session_p4.a_hInit > temps_ecoule:
                temps_ecoule += 1                
                barre_de_temps_p4.fm_affichage_temps_ecoule(temps_ecoule-1)#(int(temps_ecoule))
                #print(P4Datas.elimine_temps, P4Datas.gagne_rouge)
            f_urgences()   #ouverture porte et demandes bus can
            canevas.update()
#********FIN BOUCLE P4
    if P4Datas.gagne_rouge :
        #print(P4Datas.gagne_rouge)
        if opt == 7:
            P4Datas.etoiles = 10
        else:
            P4Datas.etoiles = 5
    else:
        P4Datas.etoiles = 0
    #print(P4Datas.etoiles, "etoiles")
    #canevas.create_text(50, 500 , text = (str(P4Datas.etoiles) + '  ETOILES'), anchor='w', font=('', 25, 'bold'))
    canevas.update()    
    P4Datas.gagne_rouge = False
    if P4Datas.elimine_temps:
        canevas.itemconfigure(ob.elimine, text = "ELIMINE : TEMPS")
        ob.fm_texte_ovale4('ÉLIMINÉ\nTEMPS', "RED")
        canevas.update()
        f_son(cow)
    if P4Datas.elimine_porte:
        canevas.itemconfigure(ob.elimine, text = "ELIMINE : PORTE")
        canevas.update()   
        
    ob.fm_raz_grille()
    #f_son(gong)
    #time.sleep(.5)
    EcranSortieP4(root)
    canevas.destroy()


    

