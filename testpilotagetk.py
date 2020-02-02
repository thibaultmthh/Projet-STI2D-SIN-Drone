from tkinter import  *




etat = 0
def forwardD(x):
    etat = 1
    print(etat)

def stopForwardD(x):
    etat = 0
    print(etat)

def backwardD(x):
    drone.backward(SPEED)
    time.sleep(DELAY)
    drone.backward(0)

def leftD(x):
    drone.left(SPEED)
    time.sleep(DELAY)
    drone.left(0)

def rightD(x):
    drone.right(SPEED)
    time.sleep(DELAY)
    drone.right(0)

def stopD(x):
    time.sleep(DELAY)
    drone.land()
    drone.quit()

tk = Tk()

# Quelques exemples de touches
tk.bind("<KeyPress-e>", forwardD) # Flèche haut
tk.bind("<KeyRelease-e>", stopForwardD) # Flèche haut

tk.bind("<Down>", backwardD) # Bas
tk.bind("<Left>", leftD) # Gauche
tk.bind("<Right>", rightD) # Droite
tk.bind("<a>", stopD) # barre d'espace
tk.mainloop()
