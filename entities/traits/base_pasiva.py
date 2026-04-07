

class PasivaBase:
    """
    esta es una plantilla para implementar mecanicas pasivas unicas para cada bestia.
    en este directorio se juntan las logicas de pasivas que no encajarían en el molde
    base de construcción de monstruos en entities/monster.py
    """
    def on_tick(self, monstruo, delta_time):
        """
        aca podemos EJECUTAR LOGICAS PARA CADA FRAME,
        como regeneracion de vida, o endurecimiento progresivo
        """
    def on_atacar(self, monstruo, intencion_ataque):
        """
        aca podemos MODIFICAR la intencion de ataque del monstruo
        ANTES DE QUE EL OPERADOR LA EJECUTE, o ejecutar efectos secundarios
        como daño al atacar, o curacion al atacar.
        """
    def on_recibir_ataque(self, monstruo, parte, cantidad):
        """
        aca podemos EJECUTAR LOGICAS AL RECIBIR UN ATAQUE, como daño reflejado,
        o curacion al recibir daño.
        """