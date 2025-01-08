from Plateau import Plateau


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()
        self.navires = []

    def ajouter_navire(self, navire):
        self.navires.append(navire)

    def tous_coules(self):
        for navire in self.navires:
            if not navire.est_coule():
                return False
        return True

