import os
import sys

def preparar_terminal():
    """Limpia la pantalla una sola vez al inicio y oculta el cursor."""
    # Limpia pantalla
    sys.stdout.write("\033[2J\033[H")
    # Oculta el cursor para que no parpadee (opcional)
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def reset_cursor():
    """Mueve el cursor al inicio (0,0) sin borrar nada."""
    # \033[H es el código ANSI para 'ir a casa' (arriba a la izquierda)
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def mostrar_cursor():
    """Vuelve a mostrar el cursor al cerrar el programa."""
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def dibujar_barra(actual, maximo=100, ancho=15, simbolo="█"):
    """Genera la barra de carga"""
    # Evitar divisiones por cero por seguridad
    if maximo <= 0: return f"[ MUERTO ]"
    
    porcentaje = actual / maximo
    porcentaje = max(0.0, min(1.0, porcentaje)) # Mantiene el valor entre 0 y 1
    
    relleno = int(porcentaje * ancho)
    vacio = ancho - relleno
    
    # Colores básicos de terminal (ANSI)
    if porcentaje > 0.5:
        color = "\033[92m" # Verde
    elif porcentaje > 0.2:
        color = "\033[93m" # Amarillo
    else:
        color = "\033[91m" # Rojo

    reset = "\033[0m" # Resetea el color de la terminal
        
    return f"[{color}{simbolo * relleno}{'.' * vacio}{reset}]"
