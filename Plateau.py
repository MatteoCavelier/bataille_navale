from Navire import Navire


class Plateau:
    def __init__(self, taille=10):
        self.taille = taille
        self.grille = []
        self.grille = []
        for i in range(taille):
            ligne = []
            for j in range(taille):
                ligne.append(None)
            self.grille.append(ligne)

    def peut_placer(self, navire, x, y, orientation):
        if orientation == "horizontal":
            if y + navire.taille > self.taille:
                return False
            for i in range(navire.taille):
                if self.grille[x][y + i] is not None:
                    return False
        else:
            if x + navire.taille > self.taille:
                return False
            for i in range(navire.taille):
                if self.grille[x + i][y] is not None:
                    return False
        return True

    def placer_navire(self, navire, x, y, orientation):
        if orientation == "horizontal":
            for i in range(navire.taille):
                self.grille[x][y + i] = navire
                navire.positions.append((x, y + i))
        else:
            for i in range(navire.taille):
                self.grille[x + i][y] = navire
                navire.positions.append((x + i, y))

    def recevoir_tir(self, x, y):
        cible = self.grille[x][y]
        if cible is None:
            return "manque"
        elif isinstance(cible, Navire):
            cible.touche += 1
            self.grille[x][y] = "touche"
            return "touche" if not cible.est_coule() else "coule"
        return "deja_tire"
