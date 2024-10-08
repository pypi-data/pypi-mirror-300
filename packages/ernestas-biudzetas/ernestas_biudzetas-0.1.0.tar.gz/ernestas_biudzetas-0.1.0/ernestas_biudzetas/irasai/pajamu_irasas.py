from ernestas_biudzetas.irasai.irasas import Irasas


class PajamuIrasas(Irasas):
    def __init__(self, suma: int,  siuntejas: str, papildoma_informacija: str):
        super().__init__(suma)
        self.siuntejas = siuntejas
        self.papildoma_informacija = papildoma_informacija
