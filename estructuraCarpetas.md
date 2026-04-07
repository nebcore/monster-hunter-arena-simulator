MONSTER HUNTER ARENA/
│
├── main.py                 # Orquestador del Game Loop
├── core/
│   ├── engine.py           # Ciclo de Ticks (Barras Preparación/Pensamiento)
│   └── operator.py         # Resolución de Ataques (El Juez)
│
├── entities/
│   ├── monster.py          # Atributos físicos y barras
│   └── body_part.py        # Salud y resistencias de partes
│
├── ia/
│   ├── processor.py        # Toma el perfil del monstruo y ejecuta la lógica
│   ├── memory.py           # Sistema de aprendizaje
│   └── profiles/           # Aquí vive la "ciencia" de cada bestia
│       ├── rathalos.py     # Parámetros + Casos especiales
│       └── tigrex.py
│
└── data/
    └── monsters.json       # Stats base (Vida, Agilidad, etc.)