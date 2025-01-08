class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []
        self.touche = 0

    def est_coule(self):
        return self.touche == self.taille
