class Monster:
    def __init__ (self, datos: dict, cerebro):
        """
        Crea un monstruo usando el diccionario de datos en 
        monster.json y le asigna una IA como cerebro.
        """
        self.id = datos.get("id", "desconocido")
        self.nombre = datos.get("nombre", "Monstruo Desconocido")

        # ============== estadisticas base ==============
        self.vida_maxima = datos.get("vida_maxima", 1000)
        self.vida_actual = self.vida_maxima
        self.agilidad = datos.get("agilidad", 10) #rapidez de la barra 1

        # ================== stamina ====================
        self.stamina_maxima = datos.get("stamina", 1000)
        self.stamina_actual = self.stamina_maxima
        self.regen_stamina = datos.get("regen_stamina", 40) # regen por segundo

        # ================== anatomía ===================
        # aqui guardamos instancias de la clase BodyPart
        self.partes = {}
        self.ataques = datos.get("ataques", [])

        # ================== cerebro ===================
        self.cerebro = cerebro # la instancia de un perfil de IA que controle el monstruo
        # se inyecta una referencia del monstruo en su propio cerebro para
        # que la IA entienda que cuerpo controla.
        self.cerebro.set_cuerpo(self)

        # ================ sistema ATB =================
        """
        Barras de progreso para el sistema de turno activo (ATB). El monstruo avanza
        en estas barras cada frame, y cuando llegan a 100, el monstruo puede actuar.

        - Barra de preparacion: representa el tiempo que tarda en estar fisicamente listo para actuar.
            [DEPENDE DE LA AGILIDAD DEL MONSTRUO]
        - Barra de pensamiento: representa el tiempo que tarda en decidir que acción tomar.
            [DEPENDE DE LA VELOCIDAD DE PENSAMIENTO DEL CEREBRO]

        Estados posibles:
            - "INACTIVO": el monstruo no puede actuar, la barra no se llena.
            - "PREPARADO": el monstruo ha llenado su barra y está listo para actuar.
            - "LISTO_PARA_ACTUAR": el monstruo sabe que quiere hacer y espera a actuar.
        """
        self.estado = "INACTIVO"
        self.barra_preparacion = 0.0 # de 0 a 100, representa el progreso para estar preparado
        self.barra_pensamiento = 0.0 # de 0 a 100, representa el progreso para decidir la acción

        # ================= rasgos pasivos ==================
        self.pasivas = [] # aqui se guardan instancias de clases que heredan de traits
    

    def tick(self, delta_time):
        """
        Paso uno del diagrama. se ejecuta en cada frame , avanza los
        relojes internos del monstruo basado en su agilidad y en la
        velocidad de pensamiento de su cerebro.
        """

        # respiracion. regeneracion de stamina pasiva
        if self.stamina_actual < self.stamina_maxima:
            self.stamina_actual += self.regen_stamina * delta_time
            if self.stamina_actual > self.stamina_maxima:
                self.stamina_actual = self.stamina_maxima

        for pasiva in self.pasivas:
            pasiva.on_tick(self, delta_time)

        if self.estado == "INACTIVO":
            # recuperando el aliento. fase fisica.
            self.barra_preparacion += self.agilidad * delta_time
            if self.barra_preparacion >= 100.0:
                self.barra_preparacion = 100.0
                self.estado = "PREPARADO"
            
        elif self.estado == "PREPARADO":
            # fase mental, esta pensando que hacer.
            # velocidad mental depende del arquetipo del cerebro.
            vel_pensamiento = self.cerebro.velocidad_pensamiento
            self.barra_pensamiento += vel_pensamiento * delta_time

            if self.barra_pensamiento >= 100.0:
                self.barra_pensamiento = 100.0
                self.estado = "LISTO_PARA_ACTUAR"

    def reiniciar_turno(self):
        """
        se llama desde el operador despues de que el monstruo ataca. paso 5.
        """
        self.barra_preparacion = 0.0
        self.barra_pensamiento = 0.0
        self.estado = "INACTIVO"
    
    def recibir_dano(self, cantidad: int):
        """
        el operador usar esto para restar vida al total del monstruo.
        """
        self.vida_actual -= cantidad
        if self.vida_actual < 0:
            self.vida_actual = 0
    
    def esta_vivo(self) -> bool:
        return self.vida_actual > 0
    
    def gastar_stamina(self, cantidad: int):
        """
        restar stamina cuando la bestia haga algun esfuerzo
        """
        self.stamina_actual -= cantidad
        if self.stamina_actual < 0:
            self.stamina_actual = 0
    
    def __str__(self):
        """ creo que es para que el estado del monstruo se imprima en la consola."""
        return f"[{self.nombre}] Vida: {self.vida_actual}/{self.vida_maxima} | Estado: {self.estado} (Prep: {int(self.barra_preparacion)}%, Pen: {int(self.barra_pensamiento)}%)"


