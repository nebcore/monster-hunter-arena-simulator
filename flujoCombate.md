graph TD
    A[Inicio del Combate] --> B[Cargar lista_combatientes];
    B --> C{"Game Loop (Se repite cada fotograma)"};
    
    subgraph "Paso 1: Fase de TICK (Actualizar Relojes)"
        C --> D[Por CADA monstruo en lista_combatientes:];
        D --> E{¿Estado == INACTIVO?};
        E -- Sí --> F[barra_preparacion += agilidad * delta_time];
        F --> G{¿barra_preparacion >= 100?};
        G -- Sí --> H[Estado = PREPARADO];
        G -- No --> C;
        
        E -- No --> I{¿Estado == PREPARADO?};
        I -- Sí --> J[barra_predecesora += vel_pensamiento * delta_time];
        J --> K{¿barra_pensamiento >= 100?};
        K -- Sí --> L[Estado = LISTO_PARA_ACTUAR];
        K -- No --> C;

        I -- No --> C;
        H --> C;
        L --> C;
    end
    
    subgraph "Paso 2: Fase de ACCIÓN (Resolver Actores Listos)"
        C --> M[Buscar monstruos con Estado == LISTO_PARA_ACTUAR];
        M -- Ninguno --> C;
        M -- Uno o más --> N[Para CADA monstruo 'Actor' listo:];
        
        N --> O[1. IA genera 'Intención de Ataque'];
        O --> P["
            <b>Intención de Ataque (Datos)</b><br/>
            - Atacante: Monstruo A<br/>
            - Ataque: Garra Venenosa<br/>
            - Naturaleza: Cortante<br/>
            - Elemento: Veneno<br/>
            - Objetivo: Monstruo B<br/>
            - Parte Objetivo: Alas
        "];
        
        P --> Q[2. El 'OPERADOR' recibe la Intención];
        Q --> R{Resuelve: Probabilidad de Éxito};
        
        R -- Fallo (Esquive) --> S[OPERADOR genera 'Suceso: FALLO'];
        R -- Acierto --> T[Resuelve: Cálculo de Daño y Efectos];
        T --> U[Aplica daño a Parte y Vida Total del Objetivo];
        U --> V[OPERADOR genera 'Suceso: GOLPE'];

        S --> W;
        V --> W;
        
        W[3. IA del 'Actor' aprende del 'Suceso'];
        W --> X[4. Log de Combate registra el 'Suceso'];
        X --> Y[5. Reiniciar al 'Actor'];
        Y --> Z[
            Estado = INACTIVO<br/>
            barra_preparacion = 0<br/>
            barra_pensamiento = 0
        ];
        Z --> C;
    end
