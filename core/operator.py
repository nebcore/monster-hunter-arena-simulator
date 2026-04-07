import random

class Operador:
    @staticmethod
    def resolver_ataque(intencion: dict) -> dict:
        """
        toma la intencion de ataque y calcula el exito, daño,
        aplica las consecuencias fisicas y entrega un reporte del suceso.
        """
        atacante = intencion["atacante"]
        objetivo = intencion["objetivo"]
        ataque = intencion["ataque"]
        parte_nombre = intencion["parte_nombre"]
        naturaleza = intencion["naturaleza"]

        parte_objetivo = objetivo.partes.get(parte_nombre)

        if not parte_objetivo: # por si intenta pegar a una parte que no existe, falla.
            return {"tipo": "FALLO", "motivo": "PARTE_INEXISTENTE"}
        
        # ----------costo de stamina----------
        # asigno 50 de stamina por defecto si es que no se especifica en el json
        costo_stamina = ataque.get("costo_stamina", 50)
        atacante.gastar_stamina(costo_stamina)

        # ----------calcular exito del ataque. precision y esquive----------
        precision_base = 100

        porcentaje_stamina = atacante.stamina_actual / atacante.stamina_maxima
        penalizacion_fatiga = 0
        if porcentaje_stamina < 0.3:
            penalizacion_fatiga = 40 * (1.0 - (porcentaje_stamina / 0.3))

        esquive_defensor = parte_objetivo.tasa_esquive
        if objetivo.estado == "INACTIVO":
            # si el objetivo esta desprevenido es mas facil de acertar
            esquive_defensor = esquive_defensor / 2.0
        
        # ---- calculo final ------
        probabilidad_acierto = precision_base - esquive_defensor - penalizacion_fatiga
        tirada = random.randint(1,100)

        if tirada > probabilidad_acierto:
            return {
                "tipo": "FALLO",
                "motivo": "ESQUIVE",
                "atacante": atacante.nombre,
                "objetivo": objetivo.nombre,
                "parte": parte_nombre,
                "ataque": ataque["nombre"]
            }
        
        # ----------calcular daño----------
        potencia_base = ataque.get("potencia", 10)

        multiplicador = 1.0
        if naturaleza == "cortante":
            multiplicador = parte_objetivo.def_cortante
        elif naturaleza == "impacto":
            multiplicador = parte_objetivo.def_impacto
        elif naturaleza == "punzante":
            multiplicador = parte_objetivo.def_punzante
        elif naturaleza == "distancia":
            multiplicador = parte_objetivo.def_distancia

        daño_final = int(potencia_base * multiplicador)

        # ----------aplicar consecuencias físicas----------
        se_rompio = parte_objetivo.recibir_dano(daño_final)
        objetivo.recibir_dano(daño_final)

        # evaluar efectividad para la memoria del cerebro
        debil = multiplicador > 1.0
        resistente = multiplicador < 1.0

        # construccion de reporte de sucesos
        reporte = {
            "tipo": "GOLPE",
            "atacante": atacante.nombre,
            "objetivo": objetivo.nombre,
            "parte": parte_nombre,
            "ataque": ataque["nombre"],
            "daño": daño_final,
            "rota": se_rompio,
            "debil": debil,
            "resistente": resistente
        }
        return reporte
