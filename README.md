# 🐉 Monster Hunter Arena Simulator

> Proyecto de pasatiempo personal. Un simulador de combate autónomo inspirado en Monster Hunter, donde dos bestias se enfrentan en una arena y la pelea se desarrolla sola — con lógica emergente, IA con personalidad y un sistema de tiempo activo.

---

## ¿Qué es esto?

Un simulador de combate **monstruo vs. monstruo** que corre completamente en la terminal. No hay jugador: la arena es autónoma. Cada bestia tiene sus propios stats, partes del cuerpo con resistencias individuales, una barra de stamina, y un cerebro con parámetros de comportamiento únicos.

El objetivo de diseño es que cada combate se sienta *vivo* — que el Rathalos y el Tigrex no peleen igual, y que el resultado no sea predecible de antemano.

---

## Vista rápida

```
==================================================
 📊 ESTADO DE LA ARENA
==================================================
 🐉 RATHALOS        [PREPARADO]
  HP:  ♥♥♥♥♥♥♥♥♥♥♥♥♥░░  850/1000
  STM: ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡░░░  600/750
  ATB: ████████████████░░  82%
--------------------------------------------------
 🐉 TIGREX          [INACTIVO]
  HP:  ♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥  780/780
  STM: ⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡░░░░  550/700
  ATB: ████████░░░░░░░░░░  43%
--------------------------------------------------
 📜 REGISTRO DE COMBATE
==================================================
  Rathalos usó Garra ígnea → Tigrex [ALAS] — CRÍTICO (x1.8)
  Tigrex usó Embestida bruta → Rathalos [CUERPO] — Normal
==================================================
```

---

## Cómo ejecutar

**Requisitos:** Python 3.8+, sin dependencias externas.

```bash
git clone https://github.com/nebcore/monster-hunter-arena-simulator
cd monster-hunter-arena-simulator
python main.py
```

Presiona `Ctrl+C` para detener la simulación en cualquier momento.

---

## Estructura del proyecto

```
monster-hunter-arena-simulator/
│
├── main.py                   # Game loop principal y orquestador
├── config.py                 # Configuración global (en construcción)
│
├── core/
│   ├── engine.py             # Motor de ticks: avanza las barras ATB y de pensamiento
│   └── operator.py           # El "juez": resuelve ataques, calcula daño, aplica efectos
│
├── entities/
│   ├── monster.py            # Clase base Monstruo: stats, barras, estado
│   └── body_part.py          # Partes del cuerpo con HP y multiplicadores de resistencia
│
├── ia/
│   ├── processor.py          # BaseBrain: cerebro configurable por parámetros
│   ├── memory.py             # Sistema de aprendizaje en combate (en construcción)
│   └── profiles/             # Perfiles de comportamiento por especie
│       ├── rathalos.py       # Lógica específica del Rathalos
│       └── tigrex.py         # Lógica específica del Tigrex
│
├── data/
│   └── monsters.json         # Stats base de cada monstruo (HP, agilidad, ataques, partes)
│
└── utils/
    ├── loaders.py            # Fabrica instancias de Monstruo desde el JSON
    └── visuals.py            # Barras de progreso, manejo del cursor en terminal
```

### Responsabilidad de cada módulo

| Módulo | Rol |
|--------|-----|
| `main.py` | Instancia monstruos, asigna cerebros, arranca el loop |
| `core/engine.py` | Avanza el tiempo: acumula las barras ATB y de pensamiento de cada bestia |
| `core/operator.py` | Árbitro del combate: resuelve probabilidades de acierto/fallo y aplica daño |
| `entities/monster.py` | Modelo de datos del monstruo: vida, stamina, estado actual |
| `entities/body_part.py` | Cada parte (cabeza, cola, alas) tiene HP propio y resistencias por tipo de daño |
| `ia/processor.py` | Cerebro conectable: decide qué ataque usar y a qué parte apuntar |
| `ia/memory.py` | Registra resultados de ataques pasados para informar decisiones futuras |
| `data/monsters.json` | Fuente de verdad de los stats: desacoplado del código |

---

## Sistema de tiempo activo (ATB)

El núcleo del combat loop se basa en **dos barras por monstruo**, no en turnos:

```
INACTIVO  →  barra_preparacion sube (según agilidad)
                    ↓ llega a 100%
PREPARADO →  barra_pensamiento sube (según velocidad_pensamiento)
                    ↓ llega a 100%
LISTO     →  IA genera intención de ataque → Operator la resuelve → vuelve a INACTIVO
```

Esto significa que un Rathalos rápido (`velocidad_pensamiento = 25`) puede actuar dos veces antes de que el Tigrex (`velocidad_pensamiento = 15`) complete su primer ciclo de pensamiento. La velocidad importa.

---

## El cerebro de cada monstruo

Los monstruos no comparten una lógica fija. Cada uno recibe una instancia de `BaseBrain` configurada con sus propios parámetros:

```python
cerebro_rathalos = BaseBrain()
cerebro_rathalos.velocidad_pensamiento = 25   # Decide rápido
cerebro_rathalos.agresividad = 0.5

cerebro_tigrex = BaseBrain()
cerebro_tigrex.velocidad_pensamiento = 15     # Más impulsivo, tarda más
cerebro_tigrex.agresividad = 0.8              # Prefiere ataques que gastan más stamina
```

Esta separación permite que el comportamiento en combate sea **emergente**: el Tigrex no es más lento porque "así lo dicen las reglas", sino porque su perfil mental lo hace gastar más tiempo procesando.

---

## Estado actual de implementación

### ✅ Funcionando

- Game loop en terminal con refresco fluido (sin parpadeo)
- Sistema ATB de doble barra (preparación + pensamiento) por monstruo
- Barras visuales de HP, Stamina y ATB con caracteres Unicode
- Registro de combate (historial de acciones)
- Carga de monstruos desde `monsters.json` vía `loaders.py`
- `BaseBrain` conectable con parámetros de comportamiento por instancia
- Estados de monstruo: `INACTIVO → PREPARADO → LISTO_PARA_ACTUAR`
- Detección de fin de combate y cierre limpio con `Ctrl+C`

### 🔧 Parcialmente implementado / necesita pulirse

- **`core/operator.py`**: La resolución de ataques existe pero el cálculo de daño con multiplicadores por parte del cuerpo y tipo de elemento aún no está completo
- **`ia/processor.py`**: `BaseBrain` toma decisiones básicas, pero la lógica de selección de ataque no consulta el estado real de las partes del cuerpo del objetivo
- **`entities/body_part.py`**: La estructura de partes con HP individual existe, pero los multiplicadores de resistencia elemental (fuego, corte, impacto) no están todos cableados al operador
- **`config.py`**: Archivo vacío — pendiente de definir constantes globales (velocidad del loop, multiplicadores base, etc.)

### ❌ Diseñado pero no implementado

- **`ia/memory.py`**: El sistema de aprendizaje en combate. El diseño está definido: la IA debería registrar si un ataque fue "muy_efectivo", "normal" o "poco_efectivo" por parte atacada, y usar ese conocimiento en decisiones posteriores
- **`ia/profiles/`**: Los perfiles específicos de Rathalos y Tigrex existen como archivos, pero la lógica diferenciada por especie (ej: Rathalos prioriza ataques aéreos, Tigrex hace embestidas) no está implementada sobre `BaseBrain`
- **Arquetipos de comportamiento**: El sistema de arquetipos (`AGRESIVO`, `CAUTELOSO`, `ESTRATEGICO`) con `tolerancia_riesgo` y `tasa_aprendizaje` está diseñado conceptualmente pero sin código
- **Sistema de esquive**: El operador no resuelve esquives ni probabilidades de acierto — todos los ataques impactan actualmente
- **Efectos de estado**: Veneno, fuego, aturdimiento y otros efectos secundarios no están implementados
- **Múltiples combatientes**: El engine asume exactamente 2 bestias; no está preparado para 3 o más

---

## Roadmap de desarrollo

**Prioridad 1 — Completar el combate base**
- Cableado completo de `operator.py`: acierto/fallo + daño con multiplicadores por parte y elemento
- `body_part.py`: resistencias elementales activas

**Prioridad 2 — IA con memoria**
- Implementar `ia/memory.py` con registro de efectividad por parte
- Conectar la memoria al tomador de decisiones en `BaseBrain`

**Prioridad 3 — Personalidad emergente**
- Arquetipos con `tolerancia_riesgo` y `tasa_aprendizaje`
- Perfiles de especie en `ia/profiles/` con comportamientos únicos

**Prioridad 4 — Más contenido**
- Más monstruos en `monsters.json`
- Efectos de estado (veneno, aturdimiento, fuego)
- Arena con 3+ combatientes

---

## Filosofía de diseño

El objetivo no es simular Monster Hunter con fidelidad mecánica, sino capturar la **sensación** de que cada bestia tiene una lógica propia. Que el Rathalos se comporte como un depredador aéreo calculador y el Tigrex como una máquina de destrucción impulsiva — no porque el código lo hardcodee, sino porque sus parámetros de cerebro y sus stats naturalmente generan ese comportamiento en el loop.

Gameplay emergente sin scripting manual. Esa es la meta.

---

*Proyecto personal en desarrollo activo. Python puro, sin dependencias externas.*