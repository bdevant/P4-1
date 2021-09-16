from tkinter import *

class BarreDeTemps():
    def __init__(self, cv, x_centre, y_centre, temps_max, echelle, hauteur, couleur='red', couleur_bordure='black', orientation='h'):
        self.cv = cv
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.temps_max = temps_max
        self.echelle = echelle
        self.hauteur = hauteur
        self.couleur = couleur
        self.couleur_bordure = couleur_bordure
        self.orientation = orientation
        
        longueur = temps_max * echelle
        x_debut = x_centre - longueur//2
        x_fin = x_centre + longueur//2
        self.x_debut = x_debut
        
        self.temps_affiche = cv.create_rectangle(x_debut, y_centre-hauteur//2, x_centre-longueur//2+longueur*0, y_centre+hauteur//2, fill=couleur)
        cv.create_rectangle(x_debut-2, y_centre-hauteur//2-2, x_fin+3, y_centre+hauteur//2+3, outline=couleur_bordure, width=4)
        cv.create_text(x_fin + 10, y_centre, text=str(temps_max), anchor='w', font=("", 25, 'bold'), fill = 'red')
        self.temps_ecoule = cv.create_text(x_debut - 10, y_centre, text=str(0), anchor='e', font=("", 25, 'bold'), fill = 'red')
        
    def fm_affichage_temps_ecoule(self, temps):
        self.cv.itemconfigure(self.temps_ecoule, text = str(temps))
        self.cv.coords(self.temps_affiche, self.x_debut, self.y_centre-self.hauteur//2, self.x_debut + temps * self.echelle, self.y_centre+self.hauteur//2)

    def fm_get_temps_max(self):
        return self.temps_max + 1
        


