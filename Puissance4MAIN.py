from Puissance4_paniers import *
from Puissance4classes import *
from Puissance4_debut_fin import *

#28/07/21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
root = Tk()
root.geometry("1918x1080")
#root.attributes('-fullscreen',True)

while True:
    gpi = Gpio()
    gpi.fm_init_gpio()
    
    root.title("P4 rfid") 
    canvas = Canvas(root, width = 1920, height = 1080 , bg = 'blue', borderwidth = 0)
    canvas.place(x = 0, y = 0)
    canvas.update()    
    f_debut_session()    
    asd = Choix(root)
    numero_option = asd.fm_retour_option()
    print(numero_option, 5000)

    if numero_option == 1:
        Option1_2(1, root)
    elif numero_option == 3:
        Option1_2(3, root)
    elif numero_option == 5:
        f_option3(5, root)
    elif numero_option == 7:
        f_option3(7, root)
    else :
        f_option3(7, root)
        #quit()
    #f_son(kling)
    f_fin_session()
    root.bind('<Escape>', lambda e: root.destroy())
pygame.quit()
quit( ) 
