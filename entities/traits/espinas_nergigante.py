from .base_pasiva import PasivaBase

class EspinasNergigante(PasivaBase):
    def __init__(self):
        self.nivel_endurecimiento = 0.0 # de 0 a 100 de espinas blancas a negras
    
    def on_tick(self, monstruo, delta_time):
        self.nivel_endurecimiento += 2.0 * delta_time
        if self.nivel_endurecimiento >= 100.0:
            self.nivel_endurecimiento = 100.0

            if "brazos" in monstruo.partes:
                monstruo.partes["brazos"].def_cortante = 0.5 # los ataques rebotan

    def on_atacar(self, monstruo, intencion_ataque):
        if self.nivel_endurecimiento >= 100.0 and intencion_ataque.naturaleza == "impacto":
            intencion_ataque.potencia_extra += 50