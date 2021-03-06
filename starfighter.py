import random
from tkinter import *
from helper import *

# --------------------- VUE ------------------------- #

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.title("Starfighter")
        self.root.iconbitmap('Images\\starcraft_macos_bigsur_icon_189700.ico')
        # ****** Variables texte ******
        self.text_niveau = StringVar(value="Niveau: ")
        self.text_hp = StringVar(value="HP: ")
        self.text_mines = StringVar(value="Mines: ")
        self.text_score = StringVar(value="Score: ")
        self.text_highscores = StringVar()
        bg = PhotoImage(file='Images\\Background.png', width=600, height=750)
        self.root.bg = bg  # Previent le garbage collector d'effacer l'image
        self.creercadreprincipale()
        self.flicker = False

    def back(self):
        self.btnback.grid_forget()
        self.highscores.grid_forget()
        self.controlswindow.grid_forget()
        self.menu.grid(column=0, row=0)
        self.text_highscores.set("")

    def creercadreprincipale(self):

        self.cadre = Frame(self.root)
        self.menu = LabelFrame(self.cadre, text="Menu", width=600, height=750, font=("Arial", 24))
        self.highscores = LabelFrame(self.cadre, text="Highscores", width=600, height=750, font=("Arial", 24))
        self.createhighscoreswindow()
        self.createcontrolswindow()
        self.btnjouer = Button(self.menu, text="Démarrer Partie", font=("Arial", 16), command=self.demarrerpartie)
        self.btnscores = Button(self.menu, text="Afficher High Scores", font=("Arial", 16), command=self.showhighscores)
        self.btncontrols = Button(self.menu, text="Afficher les Contrôles", font=("Arial", 16), command=self.showcontrols)

        self.menu.grid(column=0, row=1)
        self.btnjouer.grid(column=0, row=0, padx=50, pady=50)
        self.btnscores.grid(column=0, row=1, padx=50, pady=50)
        self.btncontrols.grid(column=0, row=2, padx=50, pady=50)
        self.cadre.pack()

    def affichermenu(self):
        self.menu.grid(column=0, row=1)

    def demarrerpartie(self):

        self.menu.grid_forget()
        self.canevas = Canvas(self.cadre, width=600, height=750, bg="black")
        self.canevas.grid(column=0, row=1, sticky=NW)
        self.statwindow = LabelFrame(self.cadre, text="Stats", font=("Arial", 24))
        self.stat_niveau = Label(self.statwindow, textvariable=self.text_niveau, font=("Arial", 18))
        self.stat_hp = Label(self.statwindow, textvariable=self.text_hp, font=("Arial", 18))
        self.stat_mines = Label(self.statwindow, textvariable=self.text_mines, font=("Arial", 18))
        self.stat_score = Label(self.statwindow, textvariable=self.text_score, font=("Arial", 18))

        self.statwindow.grid(column=1, row=1, ipadx=10)
        self.stat_niveau.grid(ipadx=10, ipady=10, sticky=W)
        self.stat_hp.grid(ipadx=10, ipady=10, sticky=W)
        self.stat_mines.grid(ipadx=10, ipady=10, sticky=W)
        self.stat_score.grid(ipadx=10, ipady=10, sticky=W)

        self.parent.demarrerpartie()

    def afficherpartie(self, partie):
        self.canevas.delete(ALL)

        vais = partie.vaisseau

        self.text_niveau.set("Niveau: " + str(self.parent.partie.niveau))
        self.text_hp.set("HP: " + str(vais.hp))
        self.text_mines.set("Mines: " + str(vais.minesdisponibles))
        self.text_score.set("Score: " + str(self.parent.partie.points))
        self.canevas.create_image(0, 0, image=self.root.bg, anchor=NW)

        vaisseauimg = PhotoImage(file='Images\\Vaisseau.png', width=vais.taille, height=vais.taille)
        self.root.vaisseauimg = vaisseauimg  # Previent le garbage collector d'effacer l'image

        bossimg = PhotoImage(file='Images\\Boss.png', width=150, height=150)
        self.root.bossimg = bossimg

        ufoimg = PhotoImage(file='Images\\Ufos.png', width=30, height=30)
        self.root.ufoimg = ufoimg

        obusimg = PhotoImage(file='Images\\Obus.png', width=10, height=20)
        self.root.obusimg = obusimg

        torpilleimg = PhotoImage(file='Images\\Torpille.png', width=10, height=20)
        self.root.torpilleimg = torpilleimg

        mineimg = PhotoImage(file='Images\\mine.png', width=30, height=30)
        self.root.mineimg = mineimg

        shieldimg = PhotoImage(file='Images\\shield.png', width=50, height=50)
        self.root.shieldimg = shieldimg

        activeshieldimg = PhotoImage(file='Images\\shield_active.png', width=80, height=81)
        self.root.activeshieldimg = activeshieldimg

        if vais.shield > 0:
                self.canevas.create_image(vais.x, vais.y, image=activeshieldimg, anchor=CENTER)
                self.canevas.create_image(vais.x, vais.y, image=vaisseauimg, anchor=CENTER)
        elif vais.invincible == 0:
            self.canevas.create_image(vais.x, vais.y, image=vaisseauimg, anchor=CENTER)
        else:
            if self.flicker:
                self.flicker = False
            else:
                self.canevas.create_image(vais.x, vais.y, image=vaisseauimg, anchor=CENTER)
                self.flicker = True

        healimg = PhotoImage(file='Images\\heal.png', width=70, height=70)
        self.root.healimg = healimg

        tripleimg = PhotoImage(file='Images\\triple-missile.png', width=20, height=23)
        self.root.tripleimg = tripleimg

        ufos = partie.ufos
        mines = partie.vaisseau.mines
        shield = partie.shield
        heal = partie.heal
        triple = partie.triple

        for i in vais.obus:
            self.canevas.create_image(i.x, i.y, image=obusimg, anchor=CENTER)

        for i in ufos:
            if isinstance(i, Ufo):
                self.canevas.create_image(i.x, i.y, image=ufoimg, anchor=CENTER)
            elif isinstance(i, Boss):
                self.canevas.create_image(i.x, i.y, image=bossimg, anchor=CENTER)
                self.canevas.create_line(i.x - 50, i.y - 75, (i.x - 50) + (i.hp * 3.34), i.y - 75, width=10, fill="red")

        for i in partie.torpille:
            self.canevas.create_image(i.x, i.y, image=torpilleimg, anchor=CENTER)

        for i in mines:
            self.canevas.create_image(i.x, i.y, image=mineimg, anchor=CENTER)

        for i in shield:
            self.canevas.create_image(i.x, i.y, image=shieldimg, anchor=CENTER)

        for i in heal:
            self.canevas.create_image(i.x, i.y, image=healimg, anchor=CENTER)

        for i in triple:
            self.canevas.create_image(i.x, i.y, image=tripleimg, anchor=CENTER)

    def initpartie(self):
        self.canevas.bind("<Motion>", self.coordvaisseau)
        self.canevas.bind("<Button>", self.creerobus)
        self.canevas.bind("<Button-3>", self.creermines)

    def creerobus(self, evt):
        self.parent.creerobus()

    def creermines(self, evt):
        self.parent.creermines()

    def coordvaisseau(self, evt):
        x = evt.x
        y = evt.y
        self.parent.coordvaisseau(x, y)

    def createcontrolswindow(self):
        self.controlswindow = LabelFrame(self.cadre, text="Contrôles", font=("Arial", 24))

        controlstext = "Click gauche pour tirer des obus -- illimité -- 1 dmg\n" \
                       "Click droit pour placer une mine -- 2 par niveau -- max 10 -- 3 aoe dmg\n" \
                       "Missile powerup -- permet de tirer 3 missiles à la fois -- perdu lorsque touché\n" \
                       "Shield powerup -- invincible et fait 0.5 dmg par seconde aux ennemis sur vous\n" \
                       "HP powerup -- redonne 2 vies\n" \
                       "Le Vaisseau suit la souris\n" \
                       "5 ufos de plus par niveau\n" \
                       "1 Boss de plus par 5 niveaux\n" \
                       "Faites le plus de points possible! Enjoy"




        self.controls = Label(self.controlswindow, text=controlstext, font=("Arial", 12))
        self.controls.grid()

    def showcontrols(self):
        self.menu.grid_forget()
        self.controlswindow.grid()
        self.btnback = Button(self.controlswindow, text="Back", font=("Arial", 16), command=self.back)
        self.btnback.grid()

    def createhighscoreswindow(self):
        self.gameoverwindow = LabelFrame(self.cadre, text="GG WP", font=("Arial", 24))

        self.gameover = StringVar(0)
        self.points = StringVar(0)

        self.scores = Label(self.gameoverwindow, textvariable=self.gameover, font=("Arial", 18))
        self.nom = Label(self.gameoverwindow, text="Votre nom :", font=("Arial", 12))
        self.nomjoueur = Entry(self.gameoverwindow)
        self.savescore = Button(self.gameoverwindow, text="Enregistrer", command=self.savescore)
        self.cancel = Button(self.gameoverwindow, text="Annuler", command=self.cancel)

        self.scores.grid(column=1, row=1, padx=10, pady=10)
        self.nom.grid(column=0, row=3, padx=10, pady=10)
        self.nomjoueur.grid(column=1, row=3, padx=10, pady=10)
        self.savescore.grid(column=2, row=3, padx=2, pady=10)
        self.cancel.grid(column=3, row=3, padx=2, pady=10)

    def inputhighscores(self, points):
        self.gameoverwindow.grid(column=0, row=1, padx=10)
        self.gameover.set(value='GAME OVER\nPoints : ' + str(points))
        self.points.set(str(points))
        self.canevas.grid_forget()

    def savescore(self):
        if self.nomjoueur.get() != "" and self.points != 0:
            nom = self.nomjoueur.get()
            fichier = open("score.txt", "a")
            info = self.points.get() + ", " + nom + "\n"
            fichier.write(info)

        self.gameoverwindow.grid_forget()
        self.statwindow.grid_forget()
        self.affichermenu()

    def cancel(self):
        self.gameoverwindow.grid_forget()
        self.statwindow.grid_forget()
        self.affichermenu()

    def showhighscores(self):
        scores = []
        with open("score.txt", "r") as fichier:
            for line in fichier:
                strippedline = line.strip('\n')
                score = int(strippedline.split(", ")[0])
                nom = strippedline.split(", ")[1]
                newline = score, nom
                scores.append(newline)

        scores.sort(key=lambda x: x[0], reverse=True)

        self.menu.grid_forget()
        self.highscores = LabelFrame(self.cadre, text="Highscores", width=600, height=750, font=("Arial", 24))

        counter = 0

        for i in scores:
            t = self.text_highscores.get()
            t += str(i[0]) + "\t" + i[1] + "\n"
            self.text_highscores.set(t)
            counter += 1
            if counter == 14:
                break

        self.label_highscores = Label(self.highscores, textvariable=self.text_highscores, font=("Arial", 18))
        self.btnback = Button(self.highscores, text="Back", font=("Arial", 16), command=self.back)

        if scores:
            self.label_highscores.grid()
        self.btnback.grid()
        self.highscores.grid(column=0, row=1)

# --------------------- MODELE ----------------------- #

class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partie = None
        self.dimX = 600
        self.dimY = 750
        self.nbrufosparniveau = 5

    def demarrerpartie(self):
        self.partie = Partie(self)

    def coordvaisseau(self, x, y):
        self.partie.coordvaisseau(x, y)

    def gameover(self, points):
        self.parent.gameover(points)

class Partie():
    def __init__(self, parent):
        self.parent = parent
        x = self.parent.dimX / 2
        y = self.parent.dimY * 0.8
        self.vaisseau = Vaisseau(self, x, y)
        self.ufos = []
        self.shield = []
        self.heal = []
        self.triple = []
        self.niveau = 0
        self.points = 0
        self.ufosmorts = set()
        self.creerniveau()
        self.coordvaisseauX = 0
        self.coordvaisseauY = 0
        self.torpille = []
        self.torpillemorts = set()

    def creerniveau(self):
        self.niveau += 1

        randomshield = random.randrange(5)
        randomhp = random.randrange(5)
        randomtriple = random.randrange(5)

        if randomshield < 1:
            self.shield.append(Shield(self, random.randrange(0, self.parent.dimX), -30))  # il part en aléatoire en x
        if randomhp < 1:
            self.heal.append(Heal(self, random.randrange(0, self.parent.dimX), -30))
        if randomtriple < 1:
            self.triple.append(Triple(self, random.randrange(0, self.parent.dimX), -30))

        if self.vaisseau.minesdisponibles < 9:
            self.vaisseau.minesdisponibles += 2
        elif self.vaisseau.minesdisponibles == 9:
            self.vaisseau.minesdisponibles += 1
        nbrufos = self.niveau * self.parent.nbrufosparniveau
        nbrpos = []
        self.vaisseau.mines = []

        if self.niveau % 5 == 0:
            nbrufos = self.niveau / 5

        while len(nbrpos) < nbrufos:
            posx = random.randrange(self.parent.dimX)
            posy = random.randrange(-300, -10)
            if [posx, posy] not in nbrpos:
                nbrpos.append([posx, posy])

        for i in nbrpos:
            if self.niveau % 5 == 0:
                self.ufos.append(Boss(self, i[0], i[1]))
            else:
                self.ufos.append(Ufo(self, i[0], i[1]))

    def coordvaisseau(self, x, y):
        self.coordvaisseauX = x
        self.coordvaisseauY = y

    def jouercoup(self):
        if self.vaisseau.invincible > 0:
            self.vaisseau.invincible -= 1
        if self.vaisseau.shield > 0:
            self.vaisseau.shield -= 1
        self.vaisseau.deplacer(self.coordvaisseauX, self.coordvaisseauY)
        self.vaisseau.deplacerobus()
        for i in self.torpille:
            i.deplacer()
        for i in self.torpillemorts:
            self.torpille.remove(i)
        self.torpillemorts = set()
        for i in self.ufos:
            i.deplacer()
        for i in self.vaisseau.obusmorts:
            self.vaisseau.obus.remove(i)
        self.vaisseau.obusmorts = set()
        for i in self.vaisseau.minesmorts:
            self.vaisseau.mines.remove(i)
        self.vaisseau.minesmorts = set()
        for i in self.ufosmorts:
            if i in self.ufos:
                self.ufos.remove(i)
        self.ufosmorts = set()
        for i in self.shield:
            i.deplacer()
        for i in self.heal:
            i.deplacer()
        for i in self.triple:
            i.deplacer()
        if not self.ufos:
            self.creerniveau()
        if self.vaisseau.hp <= 0:
            self.parent.gameover(self.points)

    def creerobus(self):
        self.vaisseau.creerobus()

    def creermines(self):
        self.vaisseau.creermines()

class Vaisseau():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 50
        self.x = x
        self.y = y
        self.vitesse = 10
        self.obus = []
        self.obusmorts = set()
        self.hp = 10
        self.invincible = 0
        self.shield = 0
        self.triple = 0
        self.minesdisponibles = 0
        self.mines = []
        self.minesmorts = set()

    def deplacer(self, x, y):
        if self.x > x:
            self.x -= self.vitesse
        if self.x < x:
            self.x += self.vitesse
        if self.y > y:
            self.y -= self.vitesse
        if self.y < y:
            self.y += self.vitesse
        for i in self.parent.ufos:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille:
                if self.shield > 0:
                    i.hp -= 0.5
                    if i.hp <= 0:
                        self.parent.points += 5
                        self.parent.ufosmorts.add(i)
                if self.invincible == 0:
                    self.hp -= 1
                    self.triple = 0
                    self.invincible = 20
                    if i.hp <= 0:
                        self.parent.points += 5
                        self.parent.ufosmorts.add(i)
        for i in self.parent.torpille:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2:
                self.parent.torpillemorts.add(i)
                if self.invincible == 0:
                    self.hp -= 1
                    self.triple = 0
                    self.invincible = 30
        for i in self.parent.shield:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille:
                self.parent.shield = []
                self.shield = 50
                self.invincible = 50
        for i in self.parent.heal:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille:
                self.parent.heal = []
                self.hp += 2
        for i in self.parent.triple:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille:
                self.parent.triple = []
                if self.triple == 1:
                    self.parent.points += 25
                else:
                    self.triple = 1

    def creerobus(self):
        if self.triple > 0:
            self.obus.append(Obus(self, self.x - 20, self.y))
            self.obus.append(Obus(self, self.x + 20, self.y))

        self.obus.append(Obus(self, self.x, self.y))

    def creermines(self):
        if self.minesdisponibles > 0:
            self.minesdisponibles -= 1
            self.mines.append(Mines(self, self.x, self.y))

    def deplacerobus(self):
        for i in self.obus:
            i.deplacer()
        for i in self.obusmorts:
            self.obus.remove(i)
        self.obusmorts = set()

class Mines():
   def __init__(self, parent, x, y):
       self.parent = parent
       self.taille = 30
       self.x = x
       self.y = y

class Obus():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 8
        self.vitesse = 10
        self.x = x
        self.y = y

    def deplacer(self):
        self.y -= self.vitesse
        if self.y < 0:
            self.parent.obusmorts.add(self)

class Torpille():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.dimY = self.parent.parent.parent.dimY
        self.taille = 8
        self.vitesse = 12
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.parent.dimX)
        self.cibleY = self.parent.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def deplacer(self):
        if self.parent.parent.niveau % 5 == 0:
            self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        else:
            self.y += self.vitesse
        if self.y > self.dimY:
            self.parent.parent.torpillemorts.add(self)

class Ufo():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 30
        self.vitesse = 4
        self.hp = 1
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def creertorpille(self):
        self.random = random.randrange(100)                         # randomise un numero de 0 a 100
        if self.random < 1:                                         # si 0 on tire une torpille
            self.parent.torpille.append(Torpille(self, self.x, self.y))

    def deplacer(self):
        self.creertorpille()                                                             # 1% chance par appel de tirer une torpille
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y) # choisi un target random sur laxe x
        distancerestante = Helper.calcDistance(self.x, self.y, self.cibleX, self.cibleY)
        if distancerestante < self.vitesse:
            self.parent.ufosmorts.add(self)
        for i in self.parent.vaisseau.obus:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2:
                self.hp -= 1
                if self.hp <= 0:
                    self.parent.points += 5
                    self.parent.ufosmorts.add(self)
                self.parent.vaisseau.obusmorts.add(i)
        for i in self.parent.vaisseau.mines:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille + 3:
                self.parent.points += 5
                self.parent.ufosmorts.add(self)
                for j in self.parent.ufos:
                    if self != j:
                        distancerestante = Helper.calcDistance(self.x, self.y, j.x, j.y)
                        if distancerestante < 75:
                            j.hp -= 3
                            if j.hp <= 0:
                                self.parent.points += 5
                                self.parent.ufosmorts.add(j)
                self.parent.vaisseau.minesmorts.add(i)

class Boss():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 150
        self.vitesse = 8
        self.hp = 30
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = random.randrange(round(self.parent.parent.dimY / 3))
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def trouvercibletorpille(self):
        self.torcibleX = random.torcibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def creertorpille(self):
        self.random = random.randrange(100)  # randomise un numero de 0 a 100
        newx = random.randint(round(self.x) - round(self.taille / 2.5), round(self.x) + round(self.taille / 2.5))

        if self.random < 25:  # si 0 a 19 on tire une torpille
            self.parent.torpille.append(Torpille(self, newx, self.y))

    def deplacer(self):
        self.creertorpille()  # 2% chance par appel de tirer une torpille
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)  # choisi un target random sur laxe x
        distancerestantemouvement = Helper.calcDistance(self.x, self.y, self.cibleX, self.cibleY)
        for i in self.parent.vaisseau.obus:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2.5:
                self.hp -= 1
                if self.hp <= 0:
                    self.parent.points += 25
                    self.parent.ufosmorts.add(self)
                self.parent.vaisseau.obusmorts.add(i)
        for i in self.parent.vaisseau.mines:
            distancerestante = Helper.calcDistance(self.x, self.y, i.x, i.y)
            if distancerestante < self.taille / 2 + 15:
                self.hp -= 3
                if self.hp <= 0:
                    self.parent.ufosmorts.add(self)
                for j in self.parent.ufos:
                    if self != j:
                        distancerestante = Helper.calcDistance(self.x, self.y, j.x, j.y)
                        if distancerestante < 75:
                            self.hp -= 3
                            if self.hp <= 0:
                                self.parent.ufosmorts.add(self)
                self.parent.vaisseau.minesmorts.add(i)

        if distancerestantemouvement <= 20:
            self.trouvercible()

class Shield():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 30
        self.vitesse = 6
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def deplacer(self):
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)  # choisi un target random sur laxe x
        if self.y < -30:
            self.parent.shield = []

class Heal():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 20
        self.vitesse = 6
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def deplacer(self):
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        if self.y < -30:
            self.parent.heal = []

class Triple():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.taille = 20
        self.vitesse = 6
        self.x = x
        self.y = y
        self.cibleX = 0
        self.cibleY = 0
        self.angle = 0
        self.trouvercible()

    def trouvercible(self):
        self.cibleX = random.randrange(self.parent.parent.dimX)
        self.cibleY = self.parent.parent.dimY + 10
        self.angle = Helper.calcAngle(self.x, self.y, self.cibleX, self.cibleY)

    def deplacer(self):
        self.x, self.y = Helper.getAngledPoint(self.angle, self.vitesse, self.x, self.y)
        if self.y < -30:
            self.parent.triple = []

# ------------------- CONTROLEUR --------------------- #

class Controlleur():
    def __init__(self):
        self.modele = Modele(self)
        self.partie = None
        self.over = False
        self.vue = Vue(self)
        self.vue.root.mainloop()

    def demarrerpartie(self):
        self.over = 0
        self.modele.demarrerpartie()
        self.partie = self.modele.partie
        self.vue.initpartie()
        self.vue.root.after(25, self.jouercoup)       # appel apres 25 ms jouercoup()

    def coordvaisseau(self, x, y):
        self.modele.partie.coordvaisseau(x, y)

    def jouercoup(self):
        self.modele.partie.jouercoup()
        if not self.over:                            # si game pas terminee alors
            self.vue.afficherpartie(self.partie)
            self.vue.root.after(25, self.jouercoup)     # appel recursif a chaque 25 ms

    def creerobus(self):
        self.partie.creerobus()

    def creermines(self):
        self.partie.creermines()

    def gameover(self, points):
        self.over = True
        self.vue.inputhighscores(points)

if __name__ == '__main__':
    c = Controlleur()