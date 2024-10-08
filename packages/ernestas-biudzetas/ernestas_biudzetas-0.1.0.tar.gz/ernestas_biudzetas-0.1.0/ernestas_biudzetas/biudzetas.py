from ernestas_biudzetas.irasai.islaidu_irasas import IslaiduIrasas
from ernestas_biudzetas.irasai.pajamu_irasas import PajamuIrasas


class Biudzetas:
    def __init__(self):
        self.zurnalas = []

    def prideti_pajamu_irasa(self, suma, siuntejas, papildoma_informacija):
        self.zurnalas.append(PajamuIrasas(
            suma, siuntejas, papildoma_informacija))
        return True

    def prideti_islaidu_irasa(self, suma, atsiskaitymo_budas, isigyta_preke_paslauga):
        self.zurnalas.append(IslaiduIrasas(
            suma, atsiskaitymo_budas, isigyta_preke_paslauga))
        return
        # self.zurnalas.append({'tipas': 'islaidos', 'suma': suma})

    def gauti_balansa(self):
        # pajamos = 0
        balansas = 0
        for item in self.zurnalas:
            if isinstance(item, PajamuIrasas):
                balansas += item.suma
            if isinstance(item, IslaiduIrasas):
                balansas -= item.suma

        return balansas

    def patodyti_ataskaita(self):
        ataskaita = ''
        for irasas in self.zurnalas:
            if isinstance(irasas, PajamuIrasas):
                ataskaita += f"""Pajamos: {irasas.siuntejas}, {
                    irasas.papildoma_informacija} - {irasas.suma} \n"""
            if isinstance(irasas, IslaiduIrasas):
                ataskaita += f"""Islaidos: {irasas.isigyta_preke_paslauga}, {
                    irasas.atsiskaitymo_budas} - {irasas.suma} \n"""
        print(ataskaita)
        # return '\n'.join(f'{irasas}' for irasas in self.zurnalas)
        # for item in self.zurnalas:
        #     print(item)

    def __len__(self):
        return len(self.zurnalas)
