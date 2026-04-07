# MONSTER HUNTER ARENA/main.py
import time
import sys
from core.engine import CombatEngine
from utils.loaders import fabricar_monstruo
from ia.processor import BaseBrain
from utils.visuals import dibujar_barra, preparar_terminal, reset_cursor, mostrar_cursor

def main():
    print("="*50)
    print("   INICIANDO MONSTER HUNTER ARENA SIMULATOR   ")
    print("="*50)

    # iniciar motor
    engine = CombatEngine()

    # montar los cerebros
    cerebro_rathalos = BaseBrain()
    cerebro_rathalos.velocidad_pensamiento = 25 # Rathalos piensa rápido
    
    cerebro_tigrex = BaseBrain()
    cerebro_tigrex.velocidad_pensamiento = 15 # Tigrex es más impulsivo y lento de mente
    cerebro_tigrex.agresividad = 0.8 # Tiende a usar ataques que gastan más estamina

    # generar monstruos con loader
    rathalos = fabricar_monstruo("rathalos", cerebro_rathalos)
    tigrex = fabricar_monstruo("tigrex", cerebro_tigrex)

    if not rathalos or not tigrex:
        print("Error crítico: No se pudieron cargar las bestias. Revisa el JSON.")
        return

    # registrar combatientes en la arena
    engine.registrar_monstruo(rathalos)
    engine.registrar_monstruo(tigrex)

    print("\n¡QUE COMIENCE EL COMBATE!\n")
    time.sleep(2) # Pausa dramática antes de empezar

    # 5. El Bucle Principal (Game Loop)
    preparar_terminal()

    try:
        while not engine.pausado:
            engine.update()
            
            # Resetear el cursor al inicio en lugar de borrar todo
            reset_cursor()
            
            # Dibujamos el estado
            print("="*50)
            print("           📊 ESTADO DE LA ARENA")
            print("="*50)
            
            for m in engine.combatientes:
                barra_hp = dibujar_barra(m.vida_actual, m.vida_maxima, ancho=15, simbolo="♥")
                barra_stm = dibujar_barra(m.stamina_actual, m.stamina_maxima, ancho=15, simbolo="⚡")
                barra_atb = dibujar_barra(m.barra_preparacion, 100, ancho=15, simbolo="█")
                
                # Usamos \033[K para borrar el resto de la línea por si el texto nuevo es más corto
                print(f" 🐉 {m.nombre.upper().ljust(15)} [{m.estado}]\033[K")
                print(f"    HP:  {barra_hp} {int(m.vida_actual)}/{m.vida_maxima}\033[K")
                print(f"    STM: {barra_stm} {int(m.stamina_actual)}/{m.stamina_maxima}\033[K")
                print(f"    ATB: {barra_atb} {int(m.barra_preparacion)}%\033[K")
                print("-" * 50 + "\033[K")

            print("           📜 REGISTRO DE COMBATE")
            print("="*50 + "\033[K")
            
            # Imprimir historial (añadimos \033[K al final de cada línea)
            for mensaje in engine.historial:
                print(f"{mensaje}\033[K")
            
            print("="*50 + "\033[K")
            print("Presiona Ctrl+C para detener...\033[K")

            time.sleep(0.05)
        
        # --- NUEVO BLOQUE DE CIERRE ---
        # Si el juego salió del while porque alguien ganó (pausado = True)
        if engine.pausado:
            print("\n\033[92mSimulación terminada\033[0m\033[K")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n[!] Simulación detenida.\033[K")
    
    finally:
        mostrar_cursor()
        # Empujamos el prompt de Bash hacia abajo con varios saltos de línea
        print("\n" * 10)

if __name__ == "__main__":
    main()