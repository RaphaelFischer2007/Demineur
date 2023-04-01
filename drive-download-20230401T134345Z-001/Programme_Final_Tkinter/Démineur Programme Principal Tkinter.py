##  Projet Démineur NSI Baptiste Hétier Maëlle Normand Raphaël Fischer



from tkinter import *
import random ##  Utilisé pour placer les mines
from os import chdir## Utilisé pour enregistrer le score dans un fichier externe
import time ##  Utilisé pour savoir le temps que le joueur a mis pour gagner
import threading ## Utilisé pour faire tourner le chronomètre

def menu(fenetre, tauxTailleX, tauxTailleY, nombreMines, canvasMenu, nom):
    """
    Crée le menu du démineur avec un bouton pour commencer à jouer et un bouton 
    pour connaitre les statistiques, avec une fenêtre d'entrée pour le 
    pseudonyme du joueur et des boutons + et - pour choisir le nombre de mines
    sur la grille
    """

    ##  Si le canvas du menu n'est pas défini (au tout début et pour les retours
    ##  au menu à la fin d'une partie), il faut le recréer. Sinon, il est 
    ##  conservé.
    if canvasMenu == None:

        canvasMenu = Canvas(fenetre, 
                          width = 1920*tauxTailleX, 
                          height = 1080*tauxTailleY, 
                          bg = "green", 
                          bd = -2)
        
        canvasMenu.pack()

        ##  On rajoute des fleurs dans le fond du canvas à des emplacements 
        ##  aléatoires
        for loop in range(30):
            fleur(canvasMenu, 
                  random.uniform(1*tauxTailleX, 19*tauxTailleX), 
                  random.uniform(0.3*tauxTailleY, 9*tauxTailleY), 
                  random.randint(0, 7))

        ##  Titre et crédits
        canvasMenu.create_text(1000*tauxTailleX, 150*tauxTailleY, 
                               text = "Démineur", 
                               font = ("Arial", int(40*tauxTailleX), "bold"))
        
        canvasMenu.create_text(1000*tauxTailleX, 220*tauxTailleY, 
                               text = "Par Maëlle Normand, Baptiste Hétier et \
Raphaël Fischer", 
                               font = ("Arial", int(20)))

        ##  Création des rectangles qui servent de bouton Jouer, Statistiques et
        ##  Comment jouer
        canvasMenu.create_rectangle(700*tauxTailleX, 350*tauxTailleY, 
                                    950*tauxTailleX, 450*tauxTailleY, 
                                    width = 4, 
                                    outline = "black", 
                                    fill = "#00AA00", 
                                    activefill = "#009900")
        
        canvasMenu.create_text(825*tauxTailleX, 400*tauxTailleY, 
                               text = "Jouer", 
                               font = ("Arial", int(25*tauxTailleX)))
        
        canvasMenu.create_rectangle(1050*tauxTailleX, 350*tauxTailleY, 
                                    1300*tauxTailleX, 450*tauxTailleY, 
                                    width = 4, 
                                    outline = "black", 
                                    fill = "#00AA00", 
                                    activefill = "#009900")
        
        canvasMenu.create_text(1175*tauxTailleX, 400*tauxTailleY, 
                               text = "Statistiques", 
                               font = ("Arial", int(25*tauxTailleX)))

        canvasMenu.create_rectangle(875*tauxTailleX, 500*tauxTailleY, 
                                    1125*tauxTailleX, 600*tauxTailleY, 
                                    width = 4, 
                                    outline = "black", 
                                    fill = "#00AA00", 
                                    activefill = "#009900")
        
        canvasMenu.create_text(1000*tauxTailleX, 550*tauxTailleY, 
                               text = "Comment jouer", 
                               font = ("Arial", int(25*tauxTailleX)))

    ##  Entrée du pseudonyme
    canvasMenu.create_text(1000*tauxTailleX, 20*tauxTailleY, 
                           text = "Pseudonyme", 
                           font = ("Arial", int(20*tauxTailleX)))
    
    entreeNom = Entry(canvasMenu, 
                      bd = 2, 
                      bg = "#E5E5E5", 
                      font = ("Arial", int(30*tauxTailleX)), 
                      width = int(10*tauxTailleX))

    ##  On met de base le nom du joueur dans la fenêtre d'entrée
    ##  (rien si le programme vient d'être lancé)
    entreeNom.insert(0, nom)

    ##  On enregistre la fenêtre d'entrée dans une fenêtre du canvas du menu
    canvasMenu.create_window(1000*tauxTailleX, 60*tauxTailleY, 
                             window = entreeNom)

    creerCompteurNombreMines(canvasMenu, 
                             nombreMines, 
                             tauxTailleX, 
                             tauxTailleY)

    ##  Si on clique sur le canvas du menu, on enregistre les coordonnées et on
    ##  effectue les actions en fonction des coordonnées du clic à l'aide de la
    ##  fonction commandeMenu
    canvasMenu.bind("<Button-1>", 
                    lambda typeClic = 1:commandeMenu(typeClic.x, 
                                                     typeClic.y, 
                                                     fenetre, 
                                                     tauxTailleX, 
                                                     tauxTailleY, 
                                                     nombreMines, 
                                                     entreeNom, 
                                                     canvasMenu))

    
def fleur(canvas, multiplicateurX, multiplicateurY, couleurAleatoire):
    """
    Crée une fleur à des coordonnées aléatoires en entrée et de couleur
    aléatoire
    couleurAleatoire est une valeur comprise entre 0 et 7
    """

    ##  Change les coordonnées aléatoires si celles-ci font apparaître la
    ##  fleur sur la zone du titre ou des boutons du menu
    while ((multiplicateurX<14*tauxTailleX
           and multiplicateurX>6*tauxTailleX
           and multiplicateurY<3*tauxTailleY)
           or
           (multiplicateurX<15*tauxTailleX
            and multiplicateurX>5*tauxTailleX
            and multiplicateurY>3*tauxTailleY
            and multiplicateurY<6*tauxTailleY)
           ):
        
        multiplicateurX = random.uniform(1*tauxTailleX, 19*tauxTailleX)
        multiplicateurY = random.uniform(1*tauxTailleY, 19*tauxTailleY)

    ##  On change le nom des variables pour plus de simplicité
    x = multiplicateurX
    y = multiplicateurY

    ##  La couleur est choisie parmis les 8 couleurs suivantes par la variable
    ##  aléatoire couleurAleatoire
    couleur = ("purple", 
               "white", 
               "pink", 
               "orange", 
               "blue", 
               "#96FCEE", 
               "#7E95EF", 
               "#DEA5F6", )[couleurAleatoire]

    ##  Tige
    canvas.create_line(100*x, 100*y, 
                       100*x, 100*y+50*tauxTailleY, 
                       width = 5*tauxTailleX, 
                       fill = "#00CC00")

    ##  Pétales
    canvas.create_oval(100*x+7*tauxTailleX, 100*y-11*tauxTailleY, 
                       100*x+29*tauxTailleX, 100*y+11*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)
    
    canvas.create_oval(100*x+2*tauxTailleX, 100*y-23*tauxTailleY, 
                       100*x+24*tauxTailleX, 100*y-1*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)
    
    canvas.create_oval(100*x-11*tauxTailleX, 100*y-28*tauxTailleY, 
                       100*x+11*tauxTailleX, 100*y-6*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)
    
    canvas.create_oval(100*x-23*tauxTailleX, 100*y-24*tauxTailleY, 
                       100*x-1*tauxTailleX, 100*y-2*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)
    
    canvas.create_oval(100*x-28*tauxTailleX, 100*y-12*tauxTailleY, 
                       100*x-6*tauxTailleX, 100*y+10*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)
    
    canvas.create_oval(100*x-20*tauxTailleX, 100*y-2*tauxTailleY, 
                       100*x+2*tauxTailleX, 100*y+20*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)
    
    canvas.create_oval(100*x-5*tauxTailleX, 100*y, 
                       100*x+17*tauxTailleX, 100*y+22*tauxTailleY, 
                       outline = 'black', 
                       fill = couleur)

    ##  Cercle central
    canvas.create_oval(100*x-10*tauxTailleX, 100*y-10*tauxTailleY, 
                       100*x+10*tauxTailleX, 100*y+10*tauxTailleY, 
                       outline = 'black', 
                       fill = 'yellow')


def creerCompteurNombreMines(canvasMenu, nombreMines, tauxTailleX, tauxTailleY):
    """
    Crée un compteur pour le nombre de mines sur la grille sous la forme
    | - | Nombre mines | + |
    """

    ##  Texte au dessus
    canvasMenu.create_text(650*tauxTailleX, 20*tauxTailleY,
                           text = "Nombre de mines",
                           font = ("Arial", int(20*tauxTailleX)))

    ##  Compteur des mines
    canvasMenu.create_rectangle(600*tauxTailleX, 35*tauxTailleY,
                                700*tauxTailleX, 85*tauxTailleY,
                                width = 3,
                                outline = "black",
                                fill = "#E1E1E1")
    
    canvasMenu.create_text(650*tauxTailleX, 60*tauxTailleY,
                           text = nombreMines,
                           font = ("Arial", int(25*tauxTailleX)))

    ##  Bouton -
    canvasMenu.create_rectangle(550*tauxTailleX, 35*tauxTailleY,
                                600*tauxTailleX, 85*tauxTailleY,
                                width = 3,
                                outline = "black",
                                fill = "#E1E1E1",
                                activefill = "#C9C9C9")
    
    canvasMenu.create_text(575*tauxTailleX, 60*tauxTailleY,
                           text = "-",
                           font = ("Arial", int(25*tauxTailleX)))

    ##  Bouton +
    canvasMenu.create_rectangle(700*tauxTailleX, 35*tauxTailleY,
                                750*tauxTailleX, 85*tauxTailleY,
                                width = 3,
                                outline = "black",
                                fill = "#E5E5E5",
                                activefill = "#C9C9C9")
    
    canvasMenu.create_text(725*tauxTailleX, 60*tauxTailleY,
                           text = "+",
                           font = ("Arial", int(25*tauxTailleX)))


def commandeMenu(x, y, fenetre, tauxTailleX, tauxTailleY, nombreMines,
                 entreeNom, canvasMenu):
    """
    Exécute les commandes relatives aux boutons Jouer, Statistiques, + et - à
    partir des coordonnées du clic
    """

    ##  Récupère le nom du joueur à partir de l'entrée de la fenêtre d'entrée
    nom = entreeNom.get()

    ##  Commande bouton Jouer
    if (x>700*tauxTailleX
        and x<950*tauxTailleX
        and y>350*tauxTailleY
        and y<450*tauxTailleY):
        
        debutJeu(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom,
                 canvasMenu)

    ##  Commande bouton Statistiques
    elif (x>1050*tauxTailleX
          and x<1300*tauxTailleX
          and y>350*tauxTailleY
          and y<450*tauxTailleY):
        
        afficherStatistiques(nom, canvasMenu, fenetre, tauxTailleX, tauxTailleY)

    ##  Commande bouton Comment jouer
    elif (x>875*tauxTailleX and
          x<1125*tauxTailleX and
          y>500*tauxTailleY and
          y<600*tauxTailleY):
        
        afficherReglesJeu(canvasMenu, fenetre, tauxTailleX, tauxTailleY)
    
    ##  Commande bouton -
    elif (x>550*tauxTailleX and
          x<600*tauxTailleX and
          y>40*tauxTailleY and
          y<100*tauxTailleY and
          nombreMines>1):

        ##  On réaffiche le menu avec 1 mine en moins au compteur, le même nom
        ##  en fenêtre d'entrée que celui au moment ou le joueur clique et le
        ##  canvas du menu pour éviter que les fleurs changent de place
        nombreMines -= 1
        menu(fenetre, tauxTailleX, tauxTailleY, nombreMines, canvasMenu, nom)

    ##  Commande bouton +    
    elif (x>700*tauxTailleX and
          x<750*tauxTailleX and
          y>40*tauxTailleY and
          y<100*tauxTailleY and
          nombreMines<91):
        
        ##  On réaffiche le menu avec 1 mine en plus au compteur, le même nom en
        ##  fenêtre d'entrée que celui au moment ou le joueur clique et le
        ##  canvas du menu pour éviter que les fleurs changent de place
        nombreMines += 1
        menu(fenetre, tauxTailleX, tauxTailleY, nombreMines, canvasMenu, nom)


def afficherReglesJeu(canvasMenu, fenetre, tauxTailleX, tauxTailleY):
    """
    Affiche les règles du jeu dans une fenêtre
    """

    ##  Création de la fenêtre    
    fenetreRegles = Canvas(fenetre,
                           width = 1501*tauxTailleX,
                           height = 1001*tauxTailleY,
                           bg = "black",
                           bd = -2)
    
    canvasMenu.create_window(1000*tauxTailleX, 500*tauxTailleY,
                             window = fenetreRegles)
    
    fenetreRegles.create_rectangle(2*tauxTailleX, 2*tauxTailleY,
                                   1499*tauxTailleX, 999*tauxTailleY,
                                   width = 6,
                                   outline = "black",
                                   fill = "#E5E5E5")
    texteTitre=""
    for loop in range(89):
        texteTitre+=" "
    texteTitre+="Règles du jeu :"
    for loop in range(89):
        texteTitre+=" "
        
    fenetreRegles.create_text(450*tauxTailleX, 50*tauxTailleY,
                              text = texteTitre,
                              font = ("Arial", int(35*tauxTailleX)))

    ##  Bouton retour
    retour = Button(fenetre,
                    text = "Retour", 
                    font = ("Arial", int(15*tauxTailleX)), 
                    bg = "#E5E5E5", 
                    command = lambda x = 1:fenetreRegles.destroy(), 
                    width = 8, 
                    height = 1)
    
    fenetreRegles.create_window(1400*tauxTailleX, 950*tauxTailleY, 
                                window = retour)

    fenetreRegles.create_text(800*tauxTailleX, 500*tauxTailleY,
                              text = "Tout \
d'abord, rentrez votre pseudonyme. Ensuite, entrez le nombre de\n\
mines sur la grille. Une fois ces étapes effectuées, \n\
vous pouvez maintenant lancer une partie, vos scores seront enregistrés.\n\
Lorsque vous lancerez une partie, vous tombez sur une grille contenant\n\
100 cases dont le nombre de mine de votre choix. Votre mission sera de \
devoiler\n\
toutes les cases à l'aide du clic gauche de votre souris, mais attention aux \n\
mines ! Lorsque vous dévoilez des cases, un chiffre apparaît à l'interieur de\n\
 celle-ci c'est le nombre de mines dans les 8 cases adjacentes\n\
à celle dévoilée. Si vous pensez savoir l'emplacement d'une mine, utilisez le\n\
clic droit pour mettre un drapeau ou l'enlever si nécessaire.\n\
\n\
La partie se termine si vous faite exploser une mine auquel cas vous avez\n\
perdu, ou alors si vous réussissez à dévoiler toutes les mines, vous avez \
alors\n\
gagné la partie!\n\
\n\
Bonne Chance !",
                                font = ("Arial", int(25*tauxTailleX)))

def debutJeu(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom, canvasMenu):
    """
    Commence le jeu si le pseudonyme du joueur est conforme
    """

    ##  Affiche un message pour prévenir le joueur que son score ne sera pas
    ##  enregistré si il n'a pas utilisé de pseudonyme
    if messageErreurPasDePseudonyme(fenetre,
                                    tauxTailleX,
                                    tauxTailleY,
                                    canvasMenu,
                                    nom,
                                    nombreMines):
        
        ##  return si le joueur n'a pas de pseudonyme
        return

    ##  Affiche un message d'erreur si le joueur a utilisé des caractères
    ##  spéciaux ou des accents
    if messageErreurCaractereSpeciaux(fenetre,
                                      tauxTailleX,
                                      tauxTailleY,
                                      canvasMenu,
                                      nom):
        
        ##  return si le joueur a utilisé des caractères spéciaux ou des accents
        ##  pour ne pas commencer le jeu
        return

    if nom == 1: ##  si le joueur a appuyé sur le bouton continuer dans la
                 ##  fenêtre d'erreur messageErreurPasDePseudonyme, 
                 ##  le pseudonyme du joueur devient 1 (indisponible pour le
                 ##  joueur puisqu'il ne peut rentrer que des chaines de
                 ##  caractères) et doit donc devenir "" après les messages
                 ##  d'erreur
        
        nom = ""
    
    grilleJoueur = initialisationGrilleJoueur() ##  Composé de "." pour
                                                ##  représenter les cases non
                                                ##  dévoilées
    
    grillePositions = {}  ##  Est vide au début parce qu'elle ne sera créée que
                          ##  la première fois que le joueur dévoile un case

    grilleAffichage = {}  ##  Grille contenant les éléments à afficher dans
                          ##  Tkinter

    ##  On supprime tous les éléments affichés dans la fenêtre Tkinter
    widgets = fenetre.winfo_children()
    for element in widgets:
        element.destroy()

    ##  On crée les canvas qui remplissent la grille pour faire le fond de la
    ##  fenêtre
    for abscisse in range(1, 28):
        for ordonnee in range(1, 16):

            ##  On réserve une case de la grille pour accueillir le canvas du
            ##  timer et on lui donne un nom différentiable
            if ordonnee == 1 and abscisse == 11:
                canvasTimer = Canvas(fenetre,
                                     width = 69*tauxTailleX,
                                     height = 67*tauxTailleY,
                                     bg = "green",
                                     bd = -2)
                
                canvasTimer.grid(column = abscisse,
                                 row = ordonnee,
                                 sticky = "nswe")
            
            else:
                canvas = Canvas(fenetre,
                                width = 69*tauxTailleX,
                                height = 67*tauxTailleY,
                                bg = "#008800",
                                bd = -2)
                
                canvas.grid(column = abscisse,
                            row = ordonnee,
                            sticky = "nswe")

                ##  Dans 10% des cases, on rajoute une fleur
                if random.random()<0.1:
                    fleur(canvas,
                          random.uniform(0.25*tauxTailleX,0.4*tauxTailleX),
                          random.uniform(0.25*tauxTailleX, 0.35*tauxTailleY),
                          random.randint(0, 7))

    ##  On initialise le timer à 120 s mais on ne le lance qu'au moment où le
    ##  joueur dévoile la première case
    canvasTexteTimer = actualiserTimer(fenetre, tauxTailleX, tauxTailleY,
                                       canvasTimer, None, 120)

    afficherGrille(grilleJoueur, grillePositions, grilleAffichage, fenetre,
                   tauxTailleX, tauxTailleY, nombreMines, nom, canvasTimer,
                   canvasTexteTimer)


def messageErreurPasDePseudonyme(fenetre, tauxTailleX, tauxTailleY, canvasMenu,
                                 nom, nombreMines):
    """
    Affiche un message si le joueur n'a pas utilisé de pseudonyme en lui
    proposant de revenir au menu ou de continuer sans pseudonyme. Si le joueur
    joue sans pseudonyme, son score ne sera pas enregistré
    """

    ##  On vérifie que le joueur n'a pas de pseudonyme et que le menu est
    ##  défini (et donc que le joueur n'a pas recommencé une partie)
    if nom == "" and canvasMenu != "":

        ##  On affiche la fenêtre pour prévenir le joueur et les boutons
        fenetreErreur = Canvas(fenetre,
                               width = 301*tauxTailleX,
                               height = 201*tauxTailleY,
                               bg = "black",
                               bd = -2)
        
        canvasMenu.create_window(845*tauxTailleX, 400*tauxTailleY,
                                 window = fenetreErreur)
        
        fenetreErreur.create_rectangle(2*tauxTailleX, 2*tauxTailleY,
                                       299*tauxTailleX, 199*tauxTailleY,
                                       width = 6,
                                       outline = "black",
                                       fill = "#E5E5E5")
        
        fenetreErreur.create_text(150*tauxTailleX, 70*tauxTailleY,
                                  text = "           Attention :\n\
Si vous n'utilisez pas\n\
de pseudonyme, votre score\n\
ne sera pas enregistré",
                                  font = ("Arial", int(15*tauxTailleX)))
        
        ##  Bouton continuer
        continuer = Button(fenetre,
                           text = "Continuer",
                           font = ("Arial", int(15*tauxTailleX)),
                           bg = "#E5E5E5",
                           command = lambda x = 1:debutJeu(fenetre, tauxTailleX,
                                                           tauxTailleY,
                                                           nombreMines, 1,
                                                           canvasMenu),
                           width = 8,
                           height = 1)
        
        fenetreErreur.create_window(90*tauxTailleX, 170*tauxTailleY,
                                    window = continuer)

        ##  Bouton annuler
        annuler = Button(fenetre,
                         text = "Annuler",
                         font = ("Arial", int(15*tauxTailleX)),
                         bg = "#E5E5E5",
                         command = lambda x = 1:fenetreErreur.destroy(),
                         width = 7,
                         height = 1)
        
        fenetreErreur.create_window(210*tauxTailleX, 170*tauxTailleY,
                                    window = annuler)
        
        return True ##  Si le joueur n'a pas utilisé de pseudonyme
    
    return False

    
def messageErreurCaractereSpeciaux(fenetre, tauxTailleX, tauxTailleY,
                                   canvasMenu, nom):
    """
    Affiche un message d'erreur si le joueur a utilisé des caractères spéciaux
    ou des accents
    """
    
    for lettre in str(nom):
        if  (lettre in ("&~é#'([{-|è`\ç^à@)°]} = +¤$£¨^%ùµ*/:.;§!?, ²êëïîüûôö")
             or lettre == '"') and canvasMenu != "":

            ##  Message d'erreur
            fenetreErreur = Canvas(fenetre,
                                   width = 301*tauxTailleX,
                                   height = 201*tauxTailleY,
                                   bg = "black",
                                   bd = -2)
            
            canvasMenu.create_window(845*tauxTailleX, 400*tauxTailleY,
                                     window = fenetreErreur)
            
            fenetreErreur.create_rectangle(2*tauxTailleX, 2*tauxTailleY,
                                           299*tauxTailleX, 199*tauxTailleY,
                                           width = 6,
                                           outline = "black",
                                           fill = "#E5E5E5")
            
            fenetreErreur.create_text(150*tauxTailleX, 30*tauxTailleY,
                                      text = "Erreur :\n\
N'utilisez pas de\n\
caractères speciaux\n\
ou d'accents dans\n\
votre pseudonyme",
                                      font = ("Arial", int(15*tauxTailleX)))

            ##  Bouton ok
            ok = Button(fenetre,
                        text = "ok",
                        font = ("Arial", int(15*tauxTailleX)),
                        bg = "#E5E5E5",
                        command = lambda x = 1:fenetreErreur.destroy(),
                        width = 4,
                        height = 1)
            
            fenetreErreur.create_window(150*tauxTailleX,
                                        160*tauxTailleY,
                                        window = ok)
            return True
        return False


def creationGrille(premiereAbscisse, premiereOrdonnee, nombreMineAPlacer):
    """
    Crée la grille avec toutes les valeurs des cases, celle que le joueur ne
    voit pas, en s'assurant que la première case que le joueur dévoile et les 8 
    cases adjascentes soient vides.
    renvoie la grille en question sous forme de dictionnaire
    """

    ##  Grille avec toutes les valeurs des cases.
    ##  Ne doit pas être montrée au joueur
    grillePositions = {}

    ##  s'assure que la première case que le joueur dévoile et les 8 cases 
    ##  adjascentes soient vides.
    listeCasesVides = []
    for abscisse in range(premiereAbscisse-1, premiereAbscisse+2):
        for ordonnee in range(premiereOrdonnee-1, premiereOrdonnee+2):
            if (abscisse >= 1 and abscisse <= 10 and ordonnee >= 1
                and ordonnee <= 10):
                
                grillePositions[abscisse, ordonnee] = 0
                listeCasesVides.append((abscisse, ordonnee))

    nombreMineAPlacer += 0
    
    ##  Parcourt toutes les positions de la grille
    for ordonnee in range(1, 11):
        for abscisse in range(1, 11):

            if (abscisse, ordonnee) not in listeCasesVides:
                position = len(grillePositions)-8

                ##  Probabilité qu'une mine soit placée, "92-position" au lieu
                ##  de "100-position" parce que la première case que le joueur 
                ##  dévoile et les 8 cases adjascentes sont vides 
                probabiliteMinePlacee = nombreMineAPlacer/(92-position)
            
                valeurAleatoire = random.random()
            
                ##  Placement des mines, représentées par des -1 sur la grille
                if probabiliteMinePlacee >= valeurAleatoire: 
                    grillePositions[abscisse, ordonnee] = -1
                    nombreMineAPlacer -= 1

                ##  Remplissage des valeurs par des cases vides, 
                ##  représentées par des 0
                else: 
                    grillePositions[abscisse, ordonnee] = 0

    
    for ordonnee in range(1, 11):
        for abscisse in range(1, 11):
            ##  Pour que chaque case vide soit le nombre de mines adjascentes
            grillePositions[abscisse, ordonnee] = calculNombreMine(
                                                              grillePositions,
                                                              abscisse,
                                                              ordonnee)
    return(grillePositions)


def calculNombreMine (grillePositions, abscisse, ordonnee):
    """
    Calcule le nombre de mines dans les 8 cases autours des cases vides

    Renvoie le nombre de mines sur les 8 cases autour ou renvoie -1 si la case
    centrale est une mine

    On Vérifie d'abord que la case sur laquelle il cherche une mine existe
    """
    
    nombreDeMine = 0

    #  Si la case est vierge :
    if grillePositions[abscisse, ordonnee]  != -1 :

        # On Parcourt toutes les positions des cases adjascentes
        for abscisseBis in range(abscisse-1, abscisse+2):
            for ordonneeBis in range(ordonnee-1, ordonnee+2):

                ##  On Vérifie que la case à observer existe 
                if (abscisseBis != 0 and abscisseBis != 11 and ordonneeBis != 0
                    and ordonneeBis != 11):

                    ##  On Vérifie si la case est une mine ou pas
                    if grillePositions[abscisseBis, ordonneeBis] == -1:
                        nombreDeMine += 1

    ##  Si la case est une mine, on renvoie -1 et la fonction ne change rien au
    ##  déroulement du programme
    else:
        nombreDeMine = -1
    return nombreDeMine


def initialisationGrilleJoueur():
    """
    Crée la grille du joueur avec seulement des '.'(représentent les cases non
    dévoilées)
    """
       
    grilleJoueur = {}

    ##  Parcourt toutes les positions de la grille
    for ordonnee in range(1, 11):
        for abscisse in range(1, 11):
            grilleJoueur[abscisse, ordonnee] = "."
    return(grilleJoueur)

    
def actualiserTimer(fenetre, tauxTailleX, tauxTailleY, canvasTimer,
                    canvasTexteTimer, temps):
    """
    affiche le timer avec un temps en entrée
    """

    ##  rénitialise le canvas qui accueillera le texte du timer si celui-ci est
    ##  déjà défini
    if canvasTexteTimer != None:
        canvasTexteTimer.destroy()

    ##  Crée le fond du timer
    canvasFondTimer = Canvas(fenetre,
                             bg = "#D1D1D1",
                             width = 438*tauxTailleX,
                             height = 135*tauxTailleY,
                             bd = -2)
    
    canvasTimer.create_window(219*tauxTailleX, 65*tauxTailleY,
                              window = canvasFondTimer)

    ##  affiche une bordure au fond
    canvasFondTimer.create_rectangle(1*tauxTailleX, 1*tauxTailleY,
                                     436*tauxTailleX, 250*tauxTailleY,
                                     width = 0,
                                     fill = "#D1D1D1")

    ##  Crée le canvas qui accueillera le texte du timer
    canvasTexteTimer = Canvas(fenetre,
                              bg = "#D1D1D1",
                              width = 400*tauxTailleX,
                              height = 100*tauxTailleY,
                              bd = -2)
    
    canvasFondTimer.create_window(219*tauxTailleX, 67*tauxTailleY,
                                  window = canvasTexteTimer)

    ##  Affiche le temps restant
    canvasTexteTimer.create_text(200*tauxTailleX, 20*tauxTailleY,
                                 text = "Temps restant",
                                 font = ("Arial", int(25*tauxTailleX)))
    
    ##  On affiche le temps en s
    if temps%60 >= 10:
        canvasTexteTimer.create_text(200*tauxTailleX, 80*tauxTailleY,
                                     text = str(temps//60)+" : "+str(temps%60),
                                     font = ("Arial", int(25*tauxTailleX)))
    else:
        canvasTexteTimer.create_text(200*tauxTailleX,
                                     80*tauxTailleY,
                                     text = str(temps//60)+" : 0"+str(temps%60),
                                     font = ("Arial", int(25*tauxTailleX)))
    
    return canvasTexteTimer


def afficherGrille(grilleJoueur, grillePositions, grilleAffichage, fenetre,
                   tauxTailleX, tauxTailleY, nombreMines, nom, canvasTimer,
                   canvasTexteTimer):
    """
    Affiche la grille du joueur dans la fenêtre avec des canvas pour chaque case
    """

    ##  Change la couleur du fond de la fenêtre
    fenetre.configure(bg = "#008800")

    ##  Parcourt toutes les valeurs de la grille
    for abscisse in range(1, 11):
        for ordonnee in range(1, 11):

            ##  Affiche le canvas correspondant à la case de la grille du joueur
            actualiser((abscisse, ordonnee), grilleJoueur, grillePositions,
                       grilleAffichage, fenetre, tauxTailleX, tauxTailleY,
                       nombreMines, nom, canvasTimer, canvasTexteTimer)

    ##  Est utile pour permettre au chronomètre de s'afficher
    fenetre.mainloop()
    
def actualiser(caseChoisie, grilleJoueur, grillePositions, grilleAffichage,
               fenetre, tauxTailleX, tauxTailleY, nombreMines, nom,
               canvasTimer, canvasTexteTimer):
    """
    Affiche le canvas correspondant à la case de la grille du joueur et
    l'enregistre dans la grille
    """

    ##  Case non dévoilée
    if grilleJoueur[caseChoisie] == ".":
        
        ##  Crée un canvas vert
        grilleAffichage[caseChoisie] = Button(bg = "green",
                                              activebackground = "green",
                                              width = int(9*tauxTailleX),
                                              height = int(4*tauxTailleY))
        
        ##  Effectue l'action désirée par le joueur selon le type de clic
        ##  (clic droit = placer un drapeau, clic gauche = dévoiler la case)
        grilleAffichage[caseChoisie].bind(
            "<Button-1>",
            lambda typeClic = 1 : tourDeJeu(grillePositions, grilleJoueur,
                                            caseChoisie[0], caseChoisie[1],
                                            typeClic, grilleAffichage, fenetre,
                                            tauxTailleX, tauxTailleY,
                                            nombreMines, nom, canvasTimer,
                                            canvasTexteTimer))
        
        grilleAffichage[caseChoisie].bind(
            "<Button-3>",
            lambda typeClic = 1 : tourDeJeu(grillePositions,
                                            grilleJoueur, caseChoisie[0],
                                            caseChoisie[1], typeClic,
                                            grilleAffichage, fenetre,
                                            tauxTailleX, tauxTailleY,
                                            nombreMines, nom, canvasTimer,
                                            canvasTexteTimer))

        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
    ##  Drapeau
    if grilleJoueur[caseChoisie] == "#":
        
        ##  Crée un canvas vert
        grilleAffichage[caseChoisie] = Canvas(fenetre, width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "green", bd = -2)
        
        ##  Effectue l'action désirée par le joueur selon le type de clic
        ##  (clic droit = retirer le drapeau, clic gauche = dévoiler la case)
        grilleAffichage[caseChoisie].bind(
            "<Button-1>",
            lambda typeClic = 1 : tourDeJeu(grillePositions, grilleJoueur,
                                            caseChoisie[0], caseChoisie[1],
                                            typeClic, grilleAffichage, fenetre,
                                            tauxTailleX, tauxTailleY,
                                            nombreMines, nom, canvasTimer,
                                            canvasTexteTimer))
        
        grilleAffichage[caseChoisie].bind(
            "<Button-3>",
            lambda typeClic = 1 : tourDeJeu(grillePositions, grilleJoueur,
                                            caseChoisie[0], caseChoisie[1],
                                            typeClic, grilleAffichage, fenetre,
                                            tauxTailleX, tauxTailleY,
                                            nombreMines, nom, canvasTimer,
                                            canvasTexteTimer))
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine un drapeau dans la case
        drapeau(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)

        
    ##  Case vide non dévoilée
    if grilleJoueur[caseChoisie] == 0:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)

        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
    ##  Case 1    
    if grilleJoueur[caseChoisie] == 1:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 1 dans la case
        un(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)
        
    ##  Case 2
    if grilleJoueur[caseChoisie] == 2:

        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 2 dans la case
        deux(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)
        
    ##  Case 3
    if grilleJoueur[caseChoisie] == 3:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 3 dans la case
        trois(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)
        
    ##  Case 4
    if grilleJoueur[caseChoisie] == 4:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 4 dans la case
        quatre(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)

    ##  Case 5
    if grilleJoueur[caseChoisie] == 5:
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 5 dans la case
        cinq(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)
        
    ##  Case 6
    if grilleJoueur[caseChoisie] == 6:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 6 dans la case
        six(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)
        
    ##  Case 7
    if grilleJoueur[caseChoisie] == 7:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)

        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 7 dans la case
        sept(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)
        
    ##  Case 8
    if grilleJoueur[caseChoisie] == 8:
        
        ##  Crée un canvas marron
        grilleAffichage[caseChoisie] = Canvas(fenetre,
                                              width = 69*tauxTailleX,
                                              height = 67*tauxTailleY,
                                              bg = "brown",
                                              bd = -2)
        
        ##  Place la case dans la grille au centre
        grilleAffichage[caseChoisie].grid(column = caseChoisie[1]+8,
                                          row = caseChoisie[0]+2,
                                          sticky = "nswe")
        
        ##  Dessine 8 dans la case
        huit(grilleAffichage[caseChoisie], tauxTailleX, tauxTailleY)

        
def tourDeJeu(grillePositions, grilleJoueur, x, y, typeClic, grilleAffichage,
              fenetre, tauxTailleX, tauxTailleY, nombreMines, nom, canvasTimer,
              canvasTexteTimer): 
    """
    Exécute l'action du joueur : demande la case à modifier puis le type de
    modification (mettre un drapeau : #, dévoiler une case ou supprimer un
    drapeau)
    Enregistre aussi le moment où le joueur commence à joueur

    Entrée : grille secrète, grille du joueur et le moment où le joueur à
    commencé à joueur (0 si aucun temps n'a été défini)
    Sortie : grille du joueur modifiée
    """
    
    caseChoisie = x, y

    ##  Une fois la case rentrée, on demande au joueur l'action
    resultatAction, grillePositions = actionJeu(caseChoisie, grillePositions,
                                                grilleJoueur, typeClic,
                                                nombreMines, fenetre,
                                                tauxTailleX, tauxTailleY,
                                                canvasTimer, canvasTexteTimer,
                                                nom)

    ##  resultatAction est assigné à "mine" si la case dévoilée est une mine
    ##  et la nouvelle grille du joueur sinon
    
    ##  Si la case dévoilée est une mine
    if resultatAction == "mine" :
        messageDefaite(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom)

    else:
        grilleJoueur = resultatAction

        ##  Parcourt les positions de la grille pour les afficher
        for ordonnee in range(1, 11):
            for abscisse in range(1, 11):
                actualiser((abscisse, ordonnee), grilleJoueur, grillePositions,
                           grilleAffichage, fenetre, tauxTailleX, tauxTailleY,
                           nombreMines, nom, canvasTimer, canvasTexteTimer)
                
        ##  Verification que toutes les cases sans mines sont dévoilées
        if devoileToutesLesCases(grilleJoueur, nombreMines):
            messageVictoire(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom)


def actionJeu(caseChoisie, grillePositions, grilleJoueur, clic, nombreMines,
              fenetre, tauxTailleX, tauxTailleY, canvasTimer, canvasTexteTimer,
              nom):
    """
    Exécute l'action désirée par le joueur
    Renvoie la grille modifiée
    """
    
    typeClic = clic.num

    if typeClic == 1: ##  Dévoiler une case
        
        if grillePositions == {}:
            lock = threading.Lock()
            grillePositions = creationGrille(caseChoisie[0], caseChoisie[1],
                                             nombreMines)
            
            timer = threading.Thread(target = commencerTimer,
                                     args = (canvasTimer,
                                             canvasTexteTimer,
                                             fenetre,
                                             tauxTailleX,
                                             tauxTailleY,
                                             lock,
                                             nom,
                                             nombreMines, ))
            
            timer.start()
            
        if grillePositions[caseChoisie] == -1: ## Renvoie "mine" si la case
                                               ##  dévoilée est une mine
            
            return("mine", grillePositions)
        
        else:
            grilleJoueur[caseChoisie] = grillePositions[caseChoisie]
            propagerLaDevoilation(grilleJoueur, grillePositions, caseChoisie)

    elif typeClic == 3: ##Placer ou supprimer un drapeau

        if grilleJoueur[caseChoisie] == ".": ## Vérifie que la case est un
                                             ##  point
            grilleJoueur[caseChoisie] = "#"
            
        elif grilleJoueur[caseChoisie] == "#": ## Vérifie que la case est un
                                               ##  drapeau
            grilleJoueur[caseChoisie] = "."

    return (grilleJoueur, grillePositions)


def propagerLaDevoilation(grilleJoueur, grillePositions, caseChoisie):
    """
    Dévoile toutes les cases adjascentes à une case vide et renvoie le grille
    du joueur modifié
    """

    ##  Le programme tourne en boucle jusqu'à ce que toutes les cases 
    ##  adjascentes aux cases vides soient dévoilées
    while True:

        ancienneGrilleJoueur = grilleJoueur.copy() 
        ##  On copie le dictionnaire pour éviter que l'ancien se modifie en
        ##  même temps que le dictionnaire modifié (pour comparer les deux)

        ##  On Parcourt toutes les positions de la grille
        for ordonnee in range(1, 11):
            for abscisse in range(1, 11):

                ##  On modifie toutes les cases adjascentes aux cases vides
                if grilleJoueur[abscisse, ordonnee] == 0:
                    grilleJoueur = devoilerLesCasesAdjascentes(grilleJoueur,
                                                               grillePositions,
                                                               abscisse,
                                                               ordonnee)
        
        ##  On ne sort de la boucle que si aucune modification n'a été faite
        ##  au dictionnaire
        if ancienneGrilleJoueur == grilleJoueur:
            break

    return grilleJoueur


def devoilerLesCasesAdjascentes(grilleJoueur, grillePositions, abscisse,
                                ordonnee):
    """
    Dévoile les cases autour de la case choisie par le joueur
    On Vérifie d'abord que la case à changer existe
    Renvoie la grille du joueur modifiée
    """


    ##  On Parcourt toutes les positions des cases adjascentes
    for abscisseBis in range(abscisse-1, abscisse+2):
        for ordonneeBis in range(ordonnee-1, ordonnee+2):

            ##  On Vérifie que la case à modifier existe 
            if (abscisseBis != 0 and abscisseBis != 11
                and ordonneeBis != 0 and ordonneeBis != 11):
                    
                ##  On dévoile la case
                grilleJoueur[abscisseBis, ordonneeBis] = grillePositions[
                    abscisseBis, ordonneeBis
                    ]
    return(grilleJoueur)


def devoileToutesLesCases(grilleJoueur, nombreMines):
    """
    Vérifie si toutes les cases sans mines ont été dévoilées, renvoie True si
    tel est le cas et False sinon

    La fonction doit être appelée après afficherMessageDefaite()
    """

    nombreCaseCachees = 0

    ##  On parcourt toute les cases de la grille
    for case in grilleJoueur.values():

        ##  Vérifie si la case n'est pas dévoilée
        if case == "." or case == "#":
            nombreCaseCachees += 1

    return(nombreCaseCachees == nombreMines) ##  True si le joueur à dévoilé
                                             ##  toutes les cases, False sinon


def commencerTimer(canvasTimer, canvasTexteTimer, fenetre, tauxTailleX, 
                   tauxTailleY, lock, nom, nombreMines):
    """
    Lance le timer en parallèle du programme principal grâce au threading
    C'est cette fonction qui enregistre le score des joueurs
    """

    ##  Lorsqu'on lance le timer, si le joueur gagne ou perd avant que le timer
    ##  finisse, pour éviter un message d'erreur, on utilise le try
    try:
        
        score = 0 ##  Correspond au temps passé depuis le début du jeu, au
                  ##  contraire de la variable temps qui correspond au temps
                  ##  restant au joueur

        ##  On utilise le lock pour faire tourner le chronomètre en parallèle du
        ##  reste du programme
        lock.acquire()

        ##  TLance le timer
        for temps in range(120, 0, -1):
            
            actualiserTimer(fenetre, tauxTailleX, tauxTailleY, canvasTimer,
                            canvasTexteTimer, temps)

            ##  On lache le lock pendant la seconde qui passe
            lock.release()

            ##  On passe une seconde
            time.sleep(1)
            score += 1

            ##  On reprend le lock
            lock.acquire()

        ##  Si le timer arrive à 0
        messageDefaite(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom)
        enregistreScore(nom, False, score, nombreMines)
        
        lock.release()

    ##  Si il y a une erreur (parce que le canvas du timer est supprimé lors
    ##  des messages de défaite et de victoire)
    except TclError:

        ##  On récupère le nombre d'éléments dans la fenêtre
        widgets = fenetre.winfo_children()

        ##  Il y a 2 éléments dans la fenêtre de défaite, donc dans ce cas on
        ##  enregistre le score en tant que défaite
        if len(widgets) == 2:
            enregistreScore(nom, False, score, nombreMines)

        ##  Il y a 3 éléments dans la fenêtre de défaite, donc dans ce cas on
        ##  enregistre le score en tant que victoire
        elif len(widgets) == 3:
            enregistreScore(nom, True, score, nombreMines)
        
        
def enregistreScore(nom, resultat, temps, nombreMines):
    """
    Enregistre dans un fichier externe les stats du joueur avec son nom, son
    nombre de parties, de victoires, de défaites et son meilleur temps
    """
 
    obFichier = open('Scores.txt', 'a') ##  Crée le fichier s'il n'a pas encore
                                        ##  été créé
    obFichier.close()

    obFichier = open('Scores.txt', 'r') ##  Ouvre le fichier en mode lecture


    ##  Cherche le nom du joueur et assigne la vartiable numeroLigne au numéro
    ##  de ligne de ce nom (0 pour la première ligne)
    numeroLigne = -1
    contenuLigne = " "
    while contenuLigne != "": ##  La valeur de la ligne ne vaut "" que si la
                              ##  ligne est vide, et donc que le lecteur a lu
                              ##  tout le fichier
        
        numeroLigne += 1
        contenuLigne = obFichier.readline() ## Lit le fichier ligne par ligne
        
        if contenuLigne == nom+"\n": ##   Il y a un "\n" à la fin de chaque
                                     ##  ligne
            break
    obFichier.close()

    
    if contenuLigne == "": ## Et donc que le lecteur a lu toutes les lignes du
                           ## fichier sans trouver le nom du joueur, puisqu'il
                           ## break quand il l'a trouvé
                           ## Dans ce cas, il faut créer le profil du joueur :
        
        obFichier = open('Scores.txt', 'a') ##  Ouvre le fichier en mode
                                            ##  écriture (concaténation)
        
        obFichier.write(nom) ## Profil du joueur
        obFichier.write("\n\
Parties jouees : 0\n\
Parties gagnees : 0\n\
Parties perdues : 0\n\
Meilleur score pour 12 mines (en secondes) : 120\n\
")
        obFichier.close()

    
    ##  Apporte les modifications au profil du joueur. Lignes contient
    ##  l'ensemble des profils, pas seulement celui du joueur
    lignes = modifierLeScore(nom, resultat, temps, numeroLigne, nombreMines)
    
    obFichier = open('Scores.txt', 'w') ##  Ouvre le fichier en mode écriture
                                        ##  (par remplacement)
    for ligne in lignes:
        obFichier.write(ligne)
            
    obFichier.close()


def modifierLeScore(nom, resultat, temps, numeroLigne, nombreMines):
    """
    Modifie le fichier contenant les informations à propos des joueurs pour
    modifier leurs statistiques à partir du nom du joueur, de l'issue de la
    partie, du temps du joueur et du numéro de ligne du début du profil (0
    pour la première ligne)
    Renvoie l'entièreté du contenu du fichier modifié
    """
    
    lignes = [] ##  Contiendra toutes les lignes du fichier sous forme de liste
                ##  de string
    
    obFichier = open('Scores.txt', 'r') ##  Ouvre le fichier en mode lecture

    ##  indice correspond à un numéro de ligne
    for indice in range(numeroLigne+5):
        
        lignes.append(obFichier.readline())## Lit le fichier ligne par ligne

        ##  Les différentes modifications sont enregistrées en sous-fonctions
        augmenterPartiesJouees(indice, lignes, nom)
        augmenterPartiesGagnees(indice, lignes, nom, resultat)
        augmenterPartiesPerdues(indice, lignes, nom, resultat)
        changerMeilleurTemps(indice, lignes, nom, resultat, nombreMines, temps)
        
    obFichier.close()
    return(lignes)
      

def augmenterPartiesJouees(indice, lignes, nom):
        
        ##  Le indice-1 >= 0 permet d'éviter les erreurs de type "out of range"
        if indice-1 >= 0 and lignes[indice-1] == nom+"\n":

            ##  On parcourt les caractères de la ligne de droite à gauche
            for position in range(len(lignes[indice])-2, 0, -1):

                ##  On cherche le dernier espace de la ligne qui est toujours
                ##  avant le nombre de parties jouées
                if lignes[indice][position] == " ":
                    
                    ancienScore = lignes[indice][position+1:len(lignes[indice])]

                    ##  On augmente l'ancienne valeur de 1a ligne et on la
                    ##  réécrit
                    nouvelleLigne = lignes[indice][0:position]+(" "
                                                + str(int(ancienScore)+1)+"\n\
")
                    lignes[indice] = nouvelleLigne
                    break ## Seul le dernier espace doit être pris en compte


def augmenterPartiesGagnees(indice, lignes, nom, resultat):
        
        ##  Le indice-2 >= 0 permet d'éviter les erreurs de type "out of range"
        ##  le "resultat" s'assure que le joueur a gagné sa partie
        if indice-2 >= 0 and lignes[indice-2] == nom+"\n" and resultat:

            ##  On parcourt les caractères de la ligne de droite à gauche
            for position in range(len(lignes[indice])-2, 0, -1):

                ##  On cherche le dernier espace de la ligne qui est toujours
                ##  avant le nombre de parties gagnées
                if lignes[indice][position] == " ":
                    
                    ancienScore = lignes[indice][position+1:len(lignes[indice])]

                    ##  On augmente l'ancienne valeur de 1a ligne et on la
                    ##  réécrit
                    nouvelleLigne = lignes[indice][0:position]+(" "
                                                +str(int(ancienScore)+1)+"\n\
")
                    lignes[indice] = nouvelleLigne
                    break ## Seul le dernier espace doit être pris en compte


def augmenterPartiesPerdues(indice, lignes, nom, resultat):
        
        ##  Le indice-3 >= 0 permet d'éviter les erreurs de type "out of range"
        ##  le "not(resultat)" s'assure que le joueur a perdu sa partie
        if indice-3 >= 0 and lignes[indice-3] == nom+"\n" and not(resultat):

            ##  On parcourt les caractères de la ligne de droite à gauche
            for position in range(len(lignes[indice])-2, 0, -1):

                ##  On cherche le dernier espace de la ligne qui est toujours
                ##  avant le nombre de parties perdues
                if lignes[indice][position] == " ":
                    
                    ancienScore = lignes[indice][position+1:len(lignes[indice])]

                    ##  On augmente l'ancienne valeur de 1a ligne et on la
                    ##  réécrit
                    nouvelleLigne = lignes[indice][0:position]+(" "
                                                +str(int(ancienScore)+1)+"\n\
")
                    lignes[indice] = nouvelleLigne
                    break ## Seul le dernier espace doit être pris en compte


def changerMeilleurTemps(indice, lignes, nom, resultat, nombreMines, temps):
        
        ##  Le indice-4 >= 0 permet d'éviter les erreurs de type "out of range"
        ##  le "resultat" s'assure que le joueur a gagné sa partie (sinon le
        ##  score ne serait pas comptabilisé
        if (indice-4 >= 0 and lignes[indice-4] == nom+"\n" and resultat
            and nombreMines == 12):

            ##  On parcourt les caractères de la ligne de droite à gauche
            for position in range(len(lignes[indice])-2, 0, -1):

                ##  On cherche le dernier espace de la ligne qui est toujours
                ##  avant l'acien score
                if lignes[indice][position] == " ":
                    
                    ancienScore = lignes[indice][position+1:len(lignes[indice])]

                    ##  On vérifie que le score du joueur est son record
                    if int(ancienScore)>temps:
                        
                        ##  On change le score et on réécrit la ligne
                        nouvelleLigne = lignes[indice][0:position]+(" "
                                                            +str(temps)+"\n\
")
                        lignes[indice] = nouvelleLigne
                    break ## Seul le dernier espace doit être pris en compte


def afficherStatistiques(nomJoueur, canvas, fenetre, tauxTailleX, tauxTailleY):
    """
    Affiche les statistiques du joueur à partir du fichier Scores.txt dans une
    nouvelle fenêtre avec un bouton retour
    """

    ##  Vérifie que le joueur a rentré un pseudonyme et affiche un message
    ##  d'erreur et renvoie True sinon (auquel cas on return pour ne pas
    ##  afficher les statistiques)
    if messageErreurPasDePseudonymeSatatistiques(nomJoueur, canvas, fenetre,
                                                 tauxTailleX, tauxTailleY):
        return

    ##  Affiche la fenêtre des statistiques
    fenetreStatistiques = Canvas(fenetre,
                                 width = 901*tauxTailleX,
                                 height = 601*tauxTailleY,
                                 bg = "black",
                                 bd = -2)
    
    canvas.create_window(1000*tauxTailleX, 500*tauxTailleY,
                         window = fenetreStatistiques)
    
    fenetreStatistiques.create_rectangle(2*tauxTailleX, 2*tauxTailleY,
                                         899*tauxTailleX, 699*tauxTailleY,
                                         width = 6,
                                         outline = "black",
                                         fill = "#E5E5E5")
    
    fenetreStatistiques.create_text(450*tauxTailleX, 50*tauxTailleY,
                                    text = "\
----------------------Vos Statistiques : ----------------------",
                                    font = ("Arial", int(35*tauxTailleX)))

    ##  Bouton retour
    retour = Button(fenetre,
                    text = "Retour",
                    font = ("Arial", int(15*tauxTailleX)),
                    bg = "#E5E5E5",
                    command = lambda x = 1:fenetreStatistiques.destroy(),
                    width = 8,
                    height = 1)
    
    fenetreStatistiques.create_window(800*tauxTailleX, 570*tauxTailleY,
                                      window = retour)

    ##  On lit le fichier et on affiche les statistiques dans la fenêtre
    obFichier = open('Scores.txt', 'a') ##  Crée le fichier s'il n'a pas encore
                                        ##  été créé pour éviter les messages
                                        ##  d'erreur
    obFichier.close()
    
    obFichier = open('Scores.txt', 'r') ##  Ouvre le fichier en mode lecture

    ##  AncienneLigne permet de vérifier si on est à la fin du fichier puisqu'à
    ##  la fin les lignes sont "" Normalement, aucune ligne du fichier
    ##  Scores.txt n'est ""
    ancienneLigne = ""
    
    while True: ##  Boucle jusqu'à ce que le lecteur trouve le nom du joueur ou 
                ##  qu'on arrive à la fin du fichier
        ligne = obFichier.readline()

        if ligne == nomJoueur+"\n": ##  Si on est au niveau du profil du joueur

            ##  Affiche les 5 lignes correspondant au profil du joueur
            for ordonnee in range(int(200*tauxTailleY), int(450*tauxTailleY),
                                  int(50*tauxTailleY)):

                fenetreStatistiques.create_text(450*tauxTailleX, ordonnee,
                                        text = ligne,
                                        font = ("Arial", int(25*tauxTailleX)))
                ligne = obFichier.readline()
            obFichier.close()
            return

        if ancienneLigne == ligne: ## Si le lecteur est arrivé à la fin du
                                   ##  fichier sans trouver le nom du joueur
            
            fenetreStatistiques.create_text(450*tauxTailleX, 200*tauxTailleY,
                                        text = "Vous n'avez pas encore joué",
                                        font = ("Arial", int(25*tauxTailleX)))
            obFichier.close()
            return


def messageErreurPasDePseudonymeSatatistiques(nomJoueur, canvas, fenetre,
                                              tauxTailleX, tauxTailleY):
    """
    Affiche un message d'erreur si le joueur n'a pas entré de pseudonyme avec
    un bouton ok
    
    Renvoie True si le joueur n'a pas utilisé de pseudonyme pour ne pas afficher
    la fenêtre de statistiques et False sinon
    """
    
    if nomJoueur == "":

        ##  Affichage de la fenêtre d'erreur
        fenetreErreur = Canvas(fenetre,
                               width = 301*tauxTailleX,
                               height = 201*tauxTailleY,
                               bg = "black",
                               bd = -2)
        
        canvas.create_window(1170*tauxTailleX, 400*tauxTailleY,
                             window = fenetreErreur)
        
        fenetreErreur.create_rectangle(2*tauxTailleX, 2*tauxTailleY,
                                       299*tauxTailleX, 199*tauxTailleY,
                                       width = 6,
                                       outline = "black",
                                       fill = "#E5E5E5")
        
        fenetreErreur.create_text(150*tauxTailleX, 50*tauxTailleY,
                                  text = "Erreur :",
                                  font = ("Arial", int(25*tauxTailleX)))
        
        fenetreErreur.create_text(150*tauxTailleX, 90*tauxTailleY,
                                  text = "vous n'avez pas rentré",
                                  font = ("Arial", int(15*tauxTailleX)))
        
        fenetreErreur.create_text(150*tauxTailleX, 110*tauxTailleY,
                                  text = "de pseudonyme",
                                  font = ("Arial", int(15*tauxTailleX)))

        ##  Bouton ok
        ok = Button(fenetre,
                    text = "ok",
                    font = ("Arial", int(15*tauxTailleX)),
                    bg = "#E5E5E5",
                    command = lambda x = 1:fenetreErreur.destroy(),
                    width = 4,
                    height = 1)
        
        fenetreErreur.create_window(150*tauxTailleX, 150*tauxTailleY,
                                    window = ok)
        
        return True
    
    return False


def messageDefaite(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom):
    """
    Affiche une explosion, un bouton 'Retour au menu' et un bouton 'Rejouer'
    """

    ##  Supprime tous les éléments de la fenêtre
    widgets = fenetre.winfo_children()
    for element in widgets:
        element.destroy()

    ##  Crée le canvas de fond
    canvas = Canvas(fenetre,
                    width = 1920*tauxTailleX,
                    height = 1500*tauxTailleY,
                    bg = "#008800",
                    bd = -2)
    
    canvas.pack()
    
    ##  Crée l'éxplosion
    canvas.create_polygon(395*tauxTailleX, 285*tauxTailleY, 636*tauxTailleX, 328*tauxTailleY, 584*tauxTailleX, 140*tauxTailleY, 772*tauxTailleX, 259*tauxTailleY, 915*tauxTailleX, 16*tauxTailleY, 1006*tauxTailleX, 206*tauxTailleY, 1348*tauxTailleX, 163*tauxTailleY, 1280*tauxTailleX, 324*tauxTailleY, 1443*tauxTailleX, 456*tauxTailleY, 1245*tauxTailleX, 533*tauxTailleY, 1251*tauxTailleX, 776*tauxTailleY, 1017*tauxTailleX, 741*tauxTailleY, 885*tauxTailleX, 867*tauxTailleY, 772*tauxTailleX, 721*tauxTailleY, 407*tauxTailleX, 772*tauxTailleY, 514*tauxTailleX, 585*tauxTailleY, 316*tauxTailleX, 503*tauxTailleY, 573*tauxTailleX, 459*tauxTailleY, fill = "red")
    canvas.create_polygon(686*tauxTailleX, 411*tauxTailleY, 799*tauxTailleX, 399*tauxTailleY, 739*tauxTailleX, 325*tauxTailleY, 822*tauxTailleX, 349*tauxTailleY, 889*tauxTailleX, 258*tauxTailleY, 961*tauxTailleX, 347*tauxTailleY, 1130*tauxTailleX, 313*tauxTailleY, 1127*tauxTailleX, 395*tauxTailleY, 1241*tauxTailleX, 403*tauxTailleY, 1154*tauxTailleX, 501*tauxTailleY, 1203*tauxTailleX, 591*tauxTailleY, 1075*tauxTailleX, 624*tauxTailleY, 1079*tauxTailleX, 717*tauxTailleY, 985*tauxTailleX, 633*tauxTailleY, 881*tauxTailleX, 752*tauxTailleY, 845*tauxTailleX, 587*tauxTailleY, 613*tauxTailleX, 676*tauxTailleY, 679*tauxTailleX, 578*tauxTailleY, 581*tauxTailleX, 541*tauxTailleY, 733*tauxTailleX, 480*tauxTailleY, fill = "orange")
    canvas.create_polygon(865*tauxTailleX, 424*tauxTailleY, 900*tauxTailleX, 445*tauxTailleY, 896*tauxTailleX, 372*tauxTailleY, 969*tauxTailleX, 421*tauxTailleY, 1041*tauxTailleX, 369*tauxTailleY, 1044*tauxTailleX, 440*tauxTailleY, 1114*tauxTailleX, 442*tauxTailleY, 1067*tauxTailleX, 505*tauxTailleY, 1133*tauxTailleX, 551*tauxTailleY, 991*tauxTailleX, 519*tauxTailleY, 1024*tauxTailleX, 586*tauxTailleY, 959*tauxTailleX, 557*tauxTailleY, 904*tauxTailleX, 631*tauxTailleY, 875*tauxTailleX, 533*tauxTailleY, 736*tauxTailleX, 581*tauxTailleY, 737*tauxTailleX, 542*tauxTailleY, 646*tauxTailleX, 544*tauxTailleY, 784*tauxTailleX, 492*tauxTailleY, 746*tauxTailleX, 465*tauxTailleY, 840*tauxTailleX, 452*tauxTailleY, fill = "yellow")

    ##  Bouton Rejouer
    canvas.create_rectangle(1550*tauxTailleX, 500*tauxTailleY,
                            1800*tauxTailleX, 600*tauxTailleY,
                            width = 4,
                            outline = "black",
                            fill = "#00AA00",
                            activefill = "green")
    
    canvas.create_text(1675*tauxTailleX, 550*tauxTailleY,
                       text = "Rejouer",
                       font = ("Arial", int(25*tauxTailleX)))

    ##  Bouton Retour au menu
    canvas.create_rectangle(1550*tauxTailleX, 350*tauxTailleY,
                            1800*tauxTailleX, 450*tauxTailleY,
                            width = 4,
                            outline = "black",
                            fill = "#00AA00",
                            activefill = "green")
    
    canvas.create_text(1675*tauxTailleX, 400*tauxTailleY,
                       text = "Retour au menu",
                       font = ("Arial", int(25*tauxTailleX)))

    ##  Crée une commande pour les boutons en fonction des coordonnées du clic
    canvas.bind("<Button-1>",
                lambda typeClic = 1 :commandeDefaite(typeClic.x, typeClic.y,
                                                     fenetre, tauxTailleX,
                                                     tauxTailleY, nombreMines,
                                                     nom))


def messageVictoire(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom):
    """
    Affiche 'Victoire' sur un canvas vert avec des fleurs en fond, un bouton
    'Retour au menu' et un bouton 'Rejouer'
    """

    ##  Supprime tous les éléments de la fenêtre
    widgets = fenetre.winfo_children()
    for element in widgets:
        element.destroy()

    ##  Crée un canvas caché qui permettra de reconnaître le message de victoire
    ##  dans la fonction commencerTimer
    canvasRepere = Canvas(fenetre,
                          width = 1920*tauxTailleX,
                          height = 1080*tauxTailleY,
                          bg = "#008800")

    ##  Canvas de fond
    canvas = Canvas(fenetre,
                    width = 1920*tauxTailleX,
                    height = 1080*tauxTailleY,
                    bg = "#008800")
    canvas.pack()

    ##  Crée une commande pour les boutons en fonction des coordonnées du clic
    canvas.bind("<Button-1>",
                lambda typeClic = 1:commandeVictoire(typeClic.x, typeClic.y,
                                                     fenetre, tauxTailleX,
                                                     tauxTailleY, nombreMines,
                                                     nom))

    ##  Message 'Victoire'
    canvas.create_text(1000*tauxTailleX, 150*tauxTailleY,
                       text = "Victoire",
                       fill = "#00EE00",
                       font = ("Arial", int(55*tauxTailleX), "bold"))

    ##  Crée les fleurs
    for loop in range(30):
        fleur(canvas,
              random.uniform(1*tauxTailleX, 19*tauxTailleX),
              random.uniform(0.3*tauxTailleY, 9*tauxTailleY),
              random.randint(0, 7))

    ##  Bouton Rejouer
    canvas.create_rectangle(1100*tauxTailleX, 450*tauxTailleY,
                            1325*tauxTailleX, 350*tauxTailleY,
                            width = 4,
                            outline = "black",
                            fill = "#00AA00",
                            activefill = "green")
    
    canvas.create_text(1212*tauxTailleX, 400*tauxTailleY,
                       text = "Rejouer",
                       font = ("Arial", int(20*tauxTailleX)))

    ##  Bouton Retour au menu
    canvas.create_rectangle(675*tauxTailleX, 450*tauxTailleY,
                            900*tauxTailleX, 350*tauxTailleY,
                            width = 4,
                            outline = "black",
                            fill = "#00AA00",
                            activefill = "green")
    
    canvas.create_text(787*tauxTailleX, 400*tauxTailleY,
                       text = "Retour au menu",
                       font = ("Arial", int(20*tauxTailleX)))


def commandeDefaite(x, y, fenetre, tauxTailleX, tauxTailleY, nombreMines, nom):
    """
    Exécute les commandes relatives aux boutons Rejouer et Retour au menu du
    message de défaite à partir des coordonnées du clic
    """

    ##  Commande du bouton 'Rejouer'
    if (x>1550*tauxTailleX and x<1800*tauxTailleX and y>500*tauxTailleY
        and y<600*tauxTailleY):
        
        debutJeu(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom, "")

    ##  Commande du bouton 'Retour au menu'
    elif (x>1550*tauxTailleX and x<1800*tauxTailleX and y>350*tauxTailleY
          and y<450*tauxTailleY):
        
        ##  On supprime tous les éléments de la fenêtre
        widgets = fenetre.winfo_children()
        for element in widgets:
            element.destroy()
            
        menu(fenetre, tauxTailleX, tauxTailleY, nombreMines, None, nom)


def commandeVictoire(x, y, fenetre, tauxTailleX, tauxTailleY, nombreMines, nom):
    """
    Exécute les commandes relatives aux boutons Rejouer et Retour au menu du
    message de victoire à partir des coordonnées du clic
    """

    ##  Commande du bouton 'Rejouer'
    if (x>1100*tauxTailleX and x<1325*tauxTailleX and y>350*tauxTailleY
        and y<450*tauxTailleY):
        
        debutJeu(fenetre, tauxTailleX, tauxTailleY, nombreMines, nom, "")

    ##  Commande du bouton 'Retour au menu'
    elif (x>675*tauxTailleX and x<900*tauxTailleX and y>350*tauxTailleY
          and y<450*tauxTailleY):

        ##  On supprime tous les éléments de la fenêtre
        widgets = fenetre.winfo_children()
        for element in widgets:
            element.destroy()
            
        menu(fenetre, tauxTailleX, tauxTailleY, nombreMines, None, nom)

def drapeau(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un drapeau dans le canevas can"""
    x1 = 60*tauxTailleX
    x2 = 10*tauxTailleX
    y1 = 40*tauxTailleY
    y2 = 10*tauxTailleY
    y3 = 60*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "Red")
    
    canvas.create_line(x2, y3,
                       x2, y2,
                       width = 2,
                       fill = "Black")

def un(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '1' dans le canevas can"""
    x1 = 40*tauxTailleX
    x2 = 35*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 25*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 10*tauxTailleY
    y3 = 55*tauxTailleY
    y4 = 15*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "blue",
                            outline = "blue")
    
    canvas.create_rectangle(x3, y1,
                            x4, y3,
                            width = 2,
                            fill = "blue",
                            outline = "blue")
    
    canvas.create_rectangle(x1, y2,
                            x4, y4,
                            width = 2,
                            fill = "blue",
                            outline = "blue")

def deux(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '2' dans le canevas can"""
    x1 = 55*tauxTailleX
    x2 = 20*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 25*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 55*tauxTailleY
    y3 = 38*tauxTailleY
    y4 = 33*tauxTailleY
    y5 = 15*tauxTailleY
    y6 = 10*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "green",
                            outline = "green")
    
    canvas.create_rectangle(x1, y3,
                            x2, y4,
                            width = 2,
                            fill = "green",
                            outline = "green")
    
    canvas.create_rectangle(x1, y5,
                            x2, y6,
                            width = 2,
                            fill = "green",
                            outline = "green")
    
    canvas.create_rectangle(x1, y4,
                            x3, y5,
                            width = 2,
                            fill = "green",
                            outline = "green")
    
    canvas.create_rectangle(x2, y2,
                            x4, y3,
                            width = 2,
                            fill = "green",
                            outline = "green")

def trois(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '3' dans le canevas can"""
    x1 = 55*tauxTailleX
    x2 = 20*tauxTailleX
    x3 = 50*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 55*tauxTailleY
    y3 = 38*tauxTailleY
    y4 = 33*tauxTailleY
    y5 = 15*tauxTailleY
    y6 = 10*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "red",
                            outline = "red")
    
    canvas.create_rectangle(x1, y3,
                            x2, y4,
                            width = 2,
                            fill = "red",
                            outline = "red")
    
    canvas.create_rectangle(x1, y5,
                            x2, y6,
                            width = 2,
                            fill = "red",
                            outline = "red")
    
    canvas.create_rectangle(x1, y4,
                            x3, y5,
                            width = 2,
                            fill = "red",
                            outline = "red")
    
    canvas.create_rectangle(x1, y2,
                            x3, y3,
                            width = 2,
                            fill = "red",
                            outline = "red")

def quatre(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '4' dans le canevas can"""
    x1 = 55*tauxTailleX
    x2 = 20*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 15*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 10*tauxTailleY
    y3 = 33*tauxTailleY
    y4 = 38*tauxTailleY
    canvas.create_rectangle(x1, y3,
                            x2, y4,
                            width = 2,
                            fill = "purple",
                            outline = "purple")
    
    canvas.create_rectangle(x1, y1,
                            x3, y2,
                            width = 2,
                            fill = "purple",
                            outline = "purple")
    
    canvas.create_rectangle(x2, y2,
                            x4, y4,
                            width = 2,
                            fill = "purple",
                            outline = "purple")

def cinq(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '5' dans le canevas can"""
    x1 = 55*tauxTailleX
    x2 = 20*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 25*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 55*tauxTailleY
    y3 = 38*tauxTailleY
    y4 = 33*tauxTailleY
    y5 = 15*tauxTailleY
    y6 = 10*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y3,
                            x2, y4,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y5,
                            x2, y6,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x2, y4,
                            x4, y5,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y2,
                            x3, y3,
                            width = 2,
                            fill = "black",
                            outline = "black")

def six(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '6' dans le canevas can"""
    x1 = 55*tauxTailleX
    x2 = 20*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 25*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 55*tauxTailleY
    y3 = 38*tauxTailleY
    y4 = 33*tauxTailleY
    y5 = 15*tauxTailleY
    y6 = 10*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y3,
                            x2, y4,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y5,
                            x2, y6,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x2, y2,
                            x4, y5,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y2,
                            x3, y3,
                            width = 2,
                            fill = "black",
                            outline = "black")

def sept(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '7' dans le canevas can"""
    x1 = 40*tauxTailleX
    x2 = 35*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 20*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 10*tauxTailleY
    y3 = 55*tauxTailleY
    y4 = 15*tauxTailleY
    y5 = 33*tauxTailleY
    y6 = 38*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x3, y5,
                            x4, y6,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y2,
                            x4, y4,
                            width = 2,
                            fill = "black",
                            outline = "black")

def huit(canvas, tauxTailleX, tauxTailleY):
    """Tracé d'un '8' dans le canevas can"""
    x1 = 55*tauxTailleX
    x2 = 20*tauxTailleX
    x3 = 50*tauxTailleX
    x4 = 25*tauxTailleX
    y1 = 60*tauxTailleY
    y2 = 55*tauxTailleY
    y3 = 38*tauxTailleY
    y4 = 33*tauxTailleY
    y5 = 15*tauxTailleY
    y6 = 10*tauxTailleY
    canvas.create_rectangle(x1, y1,
                            x2, y2,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y3,
                            x2, y4,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y5,
                            x2, y6,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x2, y2,
                            x4, y5,
                            width = 2,
                            fill = "black",
                            outline = "black")
    
    canvas.create_rectangle(x1, y2,
                            x3, y5,
                            width = 2,
                            fill = "black",
                            outline = "black")

"""-------------------------- Programme principal --------------------------"""

##  Pour adapter la fenêtre de jeu à tous les écrans, on applique un taux de
##  changement à appliquer aux coordonnées à partir de la taille verticale et
##  horizontale de l'écran en pouce
tailleEcranX = 24
tailleEcranY = 13

tauxTailleX = tailleEcranX/24
tauxTailleY = tailleEcranY/13

##  Création de la fenêtre
fenetre = Tk()
fenetre.geometry(str(int(1920*tauxTailleX))+"x"+str(int(1080*tauxTailleY)))
fenetre.title("Démineur")
fenetre.configure(bg = "green")

menu(fenetre, tauxTailleX, tauxTailleY, 12, None, "")
