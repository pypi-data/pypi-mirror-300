from ignas_t_biudzetas.moduliai.irasas import Irasas

class IslaiduIrasas(Irasas):
    def __init__(self,suma,atsiskaitymo_budas,isigyta_preke_paslauga):
        super().__init__(suma)
        self.atsiskaitymo_budas = atsiskaitymo_budas
        self.isigyta_preke_paslauga = isigyta_preke_paslauga
    def __str__(self):
        width1 = 10
        width2 = 15
        return f'|{'Išlaidos:':<{width1}} {self.suma:<{8}}|{'Atsisk.būdas: ':<{width1}} {self.atsiskaitymo_budas:<{width2}}|{'Prekė/paslauga: ':<{width1}} {self.isigyta_preke_paslauga:<{20}}|'

