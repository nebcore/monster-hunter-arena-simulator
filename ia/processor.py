import random

class BaseBrain:
    """
    Para que el cerebro decida que hacer implemento el concepto de
    informacion imperfecta y estado de creencia; el cerebro no tiene acceso a
    toda la informacion del rival, a medida que combate se construye un modelo
    mental del rival, con lo que sabe de sus ataques, partes, debilidades.
    
    Implemento el concepto de inteligencia de utilidad con ponderación inversa;
    el cerebro asigna pesos de utilidad segun la tasa de esquive de cada parte,
    para evaluar que atacar si no tiene informacion suficiente.
    """

    def __init__(self):
        self.cuerpo = None

        self.agresividad = 0.5
        self.velocidad_pensamiento = 20
        self.memoria = {}

    def set_cuerpo(self, monstruo):
        """
        conecta el cerebro con el cuerpo
        """
        self.cuerpo = monstruo

    def elegir_accion(self, rival):
        """
        decide QUE ATAQUE USAR, QUE PARTE ATACAR.
        devuelve un diccionario con la intencion de ataque
        """
        if not self.cuerpo or not rival:
            return None

        # seleccionar ataque y parte
        ataque_elegido = self._seleccionar_ataque()
        parte_objetivo = self._seleccionar_objetivo(rival)

        # Crear el objeto para el operador
        intencion = {
            "atacante": self.cuerpo,
            "objetivo": rival,
            "ataque": ataque_elegido,
            "parte_nombre": parte_objetivo,
            "naturaleza": ataque_elegido.get("naturaleza", "impacto"),
            "elemento": ataque_elegido.get("elemento", "neutral")
        }

        return intencion
    
    def _seleccionar_ataque(self):
        """
        logica que elige un ataque de la lista creada del monstruo.
        """
        ataques = self.cuerpo.ataques
        if not ataques:
            return {"nombre": "ataque basico", "potencia": 10, "naturaleza": "impacto"}
        
        pesos = []
        for atk in ataques:
            peso = 10

            peso += (atk.get("potencia", 0) * self.agresividad)
            pesos.append(peso)

        return random.choices(ataques, weights=pesos, k=1)[0]
    
    def _seleccionar_objetivo(self, rival):
        """decide que parte del rival atacar"""
        partes_disponibles = list(rival.partes.keys())
        if not partes_disponibles:
            return "cuerpo_general"
        
        pesos = []
        for nombre_parte in partes_disponibles:
            parte = rival.partes[nombre_parte]

            # instinto visual
            facilidad_impacto = 100 - parte.tasa_esquive
            peso_actual = facilidad_impacto

            # memoria de lo que lleva aprendiendo durante la pelea
            if nombre_parte in self.memoria:
                recuerdos = self.memoria[nombre_parte]

                if recuerdos.get("debil", False):
                    peso_actual += 100
                if recuerdos.get("rota", False):
                    peso_actual += 50
                if recuerdos.get("resistente", False):
                    peso_actual = max(10, peso_actual - 50)

            pesos.append(peso_actual)
                
        # seleccion de parte usando los pesos.
        objetivo_elegido = random.choices(partes_disponibles, weights=pesos, k=1)[0]
        return objetivo_elegido
    
    def aprender_de_suceso(self, reporte: dict):
        """
        se recibe reporte del operador para actualiar el estado de creencia.
        """
        if reporte["tipo"] == "FALLO":
            return # no hay novedad
        
        parte = reporte["parte"]

        # registra en su memoria si golpea una parte nueva
        if parte not in self.memoria:
            self.memoria[parte] = {}
        
        # actualiza el contenido de la memoria con los datos del reporte
        self.memoria[parte]["debil"] = reporte["debil"]
        self.memoria[parte]["resistente"] = reporte["resistente"]

        # registra la rotura de partes
        if reporte["rota"]:
            self.memoria[parte]["rota"] = True