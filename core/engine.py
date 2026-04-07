import time
from core.operator import Operador

class CombatEngine:
    def __init__(self):
        self.combatientes = []
        self.ultimo_frame_time = time.time()
        self.pausado = False
        self.historial = []

    def registrar_monstruo(self, monstruo):
        """Añade una bestia a la lista de arena."""
        self.combatientes.append(monstruo)
        self.agregar_log(f"[ENGINE] 🟢 {monstruo.nombre} ha entrado en la arena.")
    
    def agregar_log(self, mensaje):
        self.historial.append(mensaje)
        if len(self.historial) > 8:
            self.historial.pop(0)
    
    def update(self):
        """
        El que define el tiempo del simulador.
        Calcula el delta_time y actualiza a todos los combatientes.
        """
        if self.pausado:
            return
        
        # calcula cuanto tiempo ha pasado desde el último frame
        ahora = time.time()
        delta_time = ahora - self.ultimo_frame_time
        self.ultimo_frame_time = ahora

        # fase de tick
        for monstruo in self.combatientes:
            if monstruo.esta_vivo():
                # llamada al metodo tick() en monster.py
                monstruo.tick(delta_time)
                # buscar si hay estados de LISTO_PARA_ACTUAR
                if monstruo.estado == "LISTO_PARA_ACTUAR":
                    self.gestionar_accion(monstruo)
    
    def gestionar_accion(self, actor):
        """
        transicion de la fase tick a la fase de accion.
        """
        rivales = [m for m in self.combatientes if m != actor and m.esta_vivo()]
        if not rivales:
            self.agregar_log(f"\n[!] 🏆 ¡Combate finalizado! {actor.nombre} es el ganador.")
            self.detener()
            return
        
        objetivo = rivales[0]

        intencion = actor.cerebro.elegir_accion(objetivo)
        if intencion:
            reporte = Operador.resolver_ataque(intencion)
            
            if reporte["tipo"] == "FALLO":
                self.agregar_log(f"❌ {actor.nombre} intenta usar [{intencion['ataque']['nombre']}] pero FALLÓ! ({reporte['motivo']})")
            else:
                msg = f" ⚔️ {actor.nombre} atacó con [{intencion['ataque']['nombre']}] a [{reporte['parte']}] de {objetivo.nombre}. -> Daño infligido: {reporte['daño']} HP"            
                if reporte["debil"]: msg += "   -> ¡Es súper efectivo!"
                if reporte["resistente"]: msg += "   -> El ataque no fue muy efectivo..."
                if reporte["rota"]: msg += "   -> 💥 ¡PARTE ROTA!"
                self.agregar_log(msg)

            actor.cerebro.aprender_de_suceso(reporte)
        actor.reiniciar_turno()

    def detener(self):
        self.pausado = True
