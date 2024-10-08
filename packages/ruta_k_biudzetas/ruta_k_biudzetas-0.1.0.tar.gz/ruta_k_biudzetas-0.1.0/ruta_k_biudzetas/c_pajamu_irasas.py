from module import c_irasas

class PajamuIrasas(c_irasas.Irasas):
    def __init__(self,suma,siuntejas,papildoma_informacija,tipas="Pajamos"):
        super().__init__(suma)
        self.tipas=tipas
        self.siuntejas=siuntejas
        self.papildoma_informacija = papildoma_informacija