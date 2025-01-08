import tkinter as tk
import random
import time
import winsound
from Navire import Navire
from Joueur import Joueur


class BatailleNavale:
    def __init__(self, master):
        # Colors
        self.grid_color = "blue"
        self.miss_color = "white"
        self.hit_color = "red"
        self.kill_color = "black"
        self.ship_color = "gray"
        self.player_color = "lightblue"
        self.computer_color = "lightgreen"
        self.separator_color = "black"
        # Text
        self.label_place_ship = "Placez vos navires"
        self.label_tour = "Tour : Joueur"
        self.label_score = "Tirs : 0 réussis, 0 ratés"
        self.label_button_horizontal = "Changer Orientation (Horizontal)"
        self.label_win = "Vous avez gagné !"
        self.label_lose = "L'ordinateur a gagné !"
        self.five_length_ship = "Porte-avions"
        self.four_length_ship = "Croiseur"
        self.three_length_ship = "Destroyer"
        self.two_length_ship = "Sous-marin"

        self.navire_selectionne = None
        self.boutons_navires = None
        self.bouton_orientation = None
        self.stats_label = None
        self.tour_label = None
        self.label = None
        self.grille_ordinateur = None
        self.grille_joueur = None
        self.master = master
        self.master.title("Bataille Navale")
        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")

        self.navires_disponibles = [
            Navire(self.five_length_ship, 5),
            Navire(self.four_length_ship, 4),
            Navire(self.three_length_ship, 3),
            Navire(self.three_length_ship, 3),
            Navire(self.two_length_ship, 2),
            Navire(self.two_length_ship, 2)
        ]

        self.phase = "placement"
        self.orientation = "horizontal"
        self.tirs_reussis_joueur = 0
        self.tirs_rates_joueur = 0
        self.tirs_reussis_ordi = 0
        self.tirs_rates_ordi = 0
        self.temps_debut = time.time()
        self.creer_interface()

    def creer_interface(self):
        tk.Label(self.master, text="Plateau Joueur", bg=self.player_color).grid(row=0, column=0, columnspan=10)
        tk.Label(self.master, text="Plateau Ordinateur", bg=("%s" % self.computer_color)).grid(row=0, column=12, columnspan=10)

        self.grille_joueur = []
        for i in range(10):
            ligne = []
            for j in range(10):
                bouton = tk.Button(self.master, width=2, height=1, bg=self.grid_color,
                                   command=lambda x=i, y=j: self.placer_navire(x, y))
                ligne.append(bouton)
            self.grille_joueur.append(ligne)

        self.grille_ordinateur = []
        for i in range(10):
            ligne = []
            for j in range(10):
                bouton = tk.Button(self.master, width=2, height=1, bg=self.grid_color,
                                   command=lambda x=i, y=j: self.tirer(x, y))
                ligne.append(bouton)
            self.grille_ordinateur.append(ligne)

        for i in range(10):
            for j in range(10):
                self.grille_joueur[i][j].grid(row=i + 1, column=j)
                self.grille_ordinateur[i][j].grid(row=i + 1, column=j + 12)

        for i in range(11):
            tk.Label(self.master, text="", width=2, bg=self.separator_color).grid(row=i, column=11)

        self.label = tk.Label(self.master, text=self.label_place_ship)
        self.label.grid(row=12, column=0, columnspan=10)

        self.tour_label = tk.Label(self.master, text=self.label_tour)
        self.tour_label.grid(row=12, column=12, columnspan=10)

        self.stats_label = tk.Label(self.master, text=self.label_score)
        self.stats_label.grid(row=13, column=0, columnspan=10)

        self.bouton_orientation = tk.Button(self.master, text=self.label_button_horizontal, command=self.changer_orientation)
        self.bouton_orientation.grid(row=13, column=12, columnspan=10)

        self.boutons_navires = []
        for index, navire in enumerate(self.navires_disponibles):
            bouton = tk.Button(self.master, text=f"{navire.nom} ({navire.taille} cases)",
                               command=lambda n=navire: self.selectionner_navire(n))
            bouton.grid(row=14 + index, column=0, columnspan=10)
            self.boutons_navires.append(bouton)

    def selectionner_navire(self, navire):
        self.navire_selectionne = navire
        self.label.config(text=f"Navire sélectionné : {navire.nom} ({navire.taille} cases)")

    def changer_orientation(self):
        self.orientation = "vertical" if self.orientation == "horizontal" else "horizontal"
        orientation_text = "Horizontal" if self.orientation == "horizontal" else "Vertical"
        self.bouton_orientation.config(text=f"Changer Orientation ({orientation_text})")

    def mettre_a_jour_stats(self):
        self.stats_label.config(text=f"Tirs Joueur : {self.tirs_reussis_joueur} réussis, {self.tirs_rates_joueur} ratés")

    def placer_navire(self, x, y):
        if not self.navires_disponibles:
            return

        navire = self.navire_selectionne if hasattr(self, 'navire_selectionne') and self.navire_selectionne in self.navires_disponibles else \
            self.navires_disponibles[0]
        if self.joueur.plateau.peut_placer(navire, x, y, self.orientation):
            self.joueur.plateau.placer_navire(navire, x, y, self.orientation)
            self.joueur.ajouter_navire(navire)
            for pos in navire.positions:
                self.grille_joueur[pos[0]][pos[1]].config(bg=self.ship_color)
            self.navires_disponibles.remove(navire)

            for bouton in self.boutons_navires:
                if bouton.cget("text") == f"{navire.nom} ({navire.taille} cases)":
                    bouton.destroy()
                    self.boutons_navires.remove(bouton)
                    break

        if not self.navires_disponibles:
            self.phase = "jeu"
            self.label.config(text="Tirez sur l'ordinateur")
            self.placer_navires_ordinateur()

    def placer_navires_ordinateur(self):
        navires_a_placer = [
            Navire(self.five_length_ship, 5),
            Navire(self.four_length_ship, 4),
            Navire(self.three_length_ship, 3),
            Navire(self.three_length_ship, 3),
            Navire(self.two_length_ship, 2),
            Navire(self.two_length_ship, 2)
        ]
        for navire in navires_a_placer:
            place = False
            while not place:
                x, y = random.randint(0, 9), random.randint(0, 9)
                orientation = random.choice(["horizontal", "vertical"])
                if self.ordinateur.plateau.peut_placer(navire, x, y, orientation):
                    self.ordinateur.plateau.placer_navire(navire, x, y, orientation)
                    self.ordinateur.ajouter_navire(navire)
                    for pos in navire.positions:
                        self.grille_ordinateur[pos[0]][pos[1]].config(bg=self.grid_color)
                    place = True

    def tirer(self, x, y):
        if self.phase != "jeu":
            return

        resultat = self.ordinateur.plateau.recevoir_tir(x, y)
        if resultat == "manque":
            self.grille_ordinateur[x][y].config(bg=self.miss_color)
            self.tirs_rates_joueur += 1
        elif resultat == "touche":
            self.grille_ordinateur[x][y].config(bg=self.hit_color)
            self.tirs_reussis_joueur += 1
            winsound.Beep(1000, 200)
        elif resultat == "coule":
            self.grille_ordinateur[x][y].config(bg=self.kill_color)
            self.tirs_reussis_joueur += 1
            winsound.Beep(500, 500)

        self.mettre_a_jour_stats()

        if self.ordinateur.tous_coules():
            self.phase = "fin"
            self.afficher_resultat(self.label_win)
        else:
            self.tour_label.config(text="Tour : Ordinateur")
            self.tir_ordinateur()

    def tir_ordinateur(self):
        time.sleep(1)
        x, y = random.randint(0, 9), random.randint(0, 9)
        while self.joueur.plateau.grille[x][y] in ["touche", "manque"]:
            x, y = random.randint(0, 9), random.randint(0, 9)

        resultat = self.joueur.plateau.recevoir_tir(x, y)
        if resultat == "manque":
            self.grille_joueur[x][y].config(bg=self.miss_color)
            self.tirs_rates_ordi += 1
        elif resultat == "touche":
            self.grille_joueur[x][y].config(bg=self.hit_color)
            self.tirs_reussis_ordi += 1
            winsound.Beep(800, 200)
        elif resultat == "coule":
            self.grille_joueur[x][y].config(bg=self.kill_color)
            self.tirs_reussis_ordi += 1
            winsound.Beep(400, 500)

        self.mettre_a_jour_stats()

        if self.joueur.tous_coules():
            self.phase = "fin"
            self.afficher_resultat(self.label_lose)
        else:
            self.tour_label.config(text="Tour : Joueur")

    def afficher_resultat(self, message):
        temps_total = time.time() - self.temps_debut
        self.label.config(text=f"{message}\nTemps de jeu : {temps_total:.2f} secondes")
        winsound.Beep(100, 1000)


if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
