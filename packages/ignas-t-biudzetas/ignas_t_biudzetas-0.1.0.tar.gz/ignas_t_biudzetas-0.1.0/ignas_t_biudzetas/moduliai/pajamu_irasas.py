from ignas_t_biudzetas.moduliai.irasas import Irasas

class PajamuIrasas(Irasas):
    def __init__(self,suma,siuntejas,papildoma_informacija):
        super().__init__(suma)
        self.siuntejas = siuntejas
        self.papildoma_informacija = papildoma_informacija

    def __str__(self):
        width1 = 10
        width2 = 15
        return f'|{'Pajamos: ':<{width1}} {self.suma:<{8}}|{'Siuntėjas:    ':<{width1}} {self.siuntejas:<{width2}}|{'Papildoma info: ':<{width1}} {self.papildoma_informacija:<{20}}|'
