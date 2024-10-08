from ernestas_biudzetas.irasai.irasas import Irasas


class IslaiduIrasas(Irasas):
    def __init__(self, suma: int,  atsiskaitymo_budas: str, isigyta_preke_paslauga: str):
        super().__init__(suma)
        self.atsiskaitymo_budas = atsiskaitymo_budas
        self.isigyta_preke_paslauga = isigyta_preke_paslauga
