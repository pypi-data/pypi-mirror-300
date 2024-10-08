from module import c_irasas

class IslaiduIrasas(c_irasas.Irasas):
    def __init__(self,suma,atsiskaitymo_budas,isigyta_preke_paslauga,tipas="Išlaidos"):
        super().__init__(suma)
        self.tipas = tipas
        self.atsiskaitymo_budas = atsiskaitymo_budas
        self.isigyta_preke_paslauga = isigyta_preke_paslauga