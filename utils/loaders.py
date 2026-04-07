# se dedica a leer el json y construye las instancias de las bestias en la arena.
import json
import os
from entities.monster import Monster
from entities.body_part import BodyPart

def cargar_datos_monstruo(nombre_monstruo: str):
    """
    va a buscar en el archivo json los datos de un monstruo específico
    """
    ruta_archivo = os.path.join("data", "monsters.json")

    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            biblioteca = json.load(f)

        if nombre_monstruo in biblioteca:
            return biblioteca[nombre_monstruo]
        else:
            print(f"Error: monstruo '{nombre_monstruo}' no encontrado en {ruta_archivo}")
            return None
    except FileNotFoundError:
        print(f"Error: archivo {ruta_archivo} no encontrado.")
        return None

def fabricar_monstruo(nombre_especie: str, cerebro_instancia):
    """
    este es el buscador y constructor de objetos para cada monstruo
    """
    datos = cargar_datos_monstruo(nombre_especie)
    if not datos:
        return None
    
    # construimos la base del monstruo usando los datos del json
    nuevo_monstruo = Monster(datos, cerebro_instancia)

    # fabricamos y conectamos las partes del cuerpo
    dict_partes_datos = datos.get("partes", {})
    for nombre_parte, stats_parte in dict_partes_datos.items():
        # creamos el bodypart como objeto
        objeto_parte = BodyPart(nombre_parte, stats_parte)
        # lo metemos en el diccionario de partes del monstruo
        nuevo_monstruo.partes[nombre_parte] = objeto_parte

    # aqui se podrían agregar las pasivas específicas de cada monstruo, por ejemplo:

    print(f"[SISTEMA] {nuevo_monstruo.nombre} generado con éxito.")
    return nuevo_monstruo