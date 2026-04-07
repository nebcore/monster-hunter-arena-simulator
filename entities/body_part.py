class BodyPart:
    def __init__(self, nombre: str, datos: dict):
        """
        representa una parte especifica del cuerpo de la bestia,
        como la cabeza o la cola.
        """
        self.nombre = nombre
        self.vida_maxima = datos.get("vida", 500)
        self.vida_actual = self.vida_maxima
        self.rota = False

        # la tasa de esquive. dificultad de acertar ataques a esta parte.
        self.tasa_esquive = datos.get("tasa_esquive", 10)

        # ============== defensas fisicas ==============
        """
        multiplicadores de daño recibido.
        - 1.0 = daño normal. 100%
        - 0.8 = resistente. 80%
        - 1.5 = debil. 150%
        """
        self.def_cortante = datos.get("def_cortante", 1.0)
        self.def_punzante = datos.get("def_punzante", 1.0)
        self.def_impacto = datos.get("def_impacto", 1.0)
        self.def_distancia = datos.get("def_distancia", 1.0)

        # ============== resistencias elementales ==============
        self.res_fuego = datos.get("res_fuego", 1.0)
        self.res_agua = datos.get("res_agua", 1.0)
        self.res_trueno = datos.get("res_trueno", 1.0)
        self.res_hielo = datos.get("res_hielo", 1.0)
        self.res_dragon = datos.get("res_dragon", 1.0)

        # resistencia a estados alterados (ailments)
        self.res_veneno = datos.get("res_veneno", 1.0)
        self.res_paralisis = datos.get("res_paralisis", 1.0)
        self.res_sueño = datos.get("res_sueño", 1.0)
        self.res_nitro = datos.get("res_nitro", 1.0)
        self.res_stun = datos.get("res_stun", 1.0)

    def recibir_dano(self, cantidad: int) -> bool:
        """
        aplica daño a la parte del cuerpo. devuelve true si la parte
        se rompe.
        """
        if self.rota:
            return False # ya esta rota
        
        self.vida_actual -= cantidad

        if self.vida_actual <= 0:
            self.vida_actual = 0
            self.rota = True
            return True # se rompe
        
        return False
    
    def esta_rota(self) -> bool:
        return self.rota
    
    def __str__(self):
        estado = "ROTA" if self.rota else "INTACTA"
        return f"[{self.nombre}] Vida: {self.vida_actual}/{self.vida_maxima} - Estado: {estado}"

