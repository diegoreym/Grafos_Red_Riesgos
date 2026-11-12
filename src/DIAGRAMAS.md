# Diagramas de la red de riego

Los diagramas se basan en el dataset de `datos.py`. Las etiquetas de las aristas son capacidades nominales en L/min. En los estados modificados, las flechas rojas discontinuas identifican las conexiones que se cerraron; no forman parte de las rutas disponibles.

## Red original

```mermaid
flowchart LR
    I1["I1 · Reservorio"] -->|120| I2["I2 · Filtro"]
    I2 -->|100| I3["I3 · Bomba"]
    I2 -->|50| I10["I10 · Cisterna Alterna"]
    I3 -->|70| I4["I4 · Válvula Norte"]
    I3 -->|60| I7["I7 · Válvula Sur"]
    I4 -->|35| I5["I5 · Parcela A"]
    I4 -->|35| I6["I6 · Parcela B"]
    I7 -->|30| I8["I8 · Parcela C"]
    I7 -->|25| I9["I9 · Parcela D"]
    I10 -->|40| I7
```

## Después de cerrar I3 → I7

La ruta a I9 usa el desvío por I10.

```mermaid
flowchart LR
    I1["I1 · Reservorio"] -->|120| I2["I2 · Filtro"]
    I2 -->|100| I3["I3 · Bomba"]
    I2 -->|50| I10["I10 · Cisterna Alterna"]
    I3 -->|70| I4["I4 · Válvula Norte"]
    I3 -. "cerrada · 60" .-> I7["I7 · Válvula Sur"]
    I4 -->|35| I5["I5 · Parcela A"]
    I4 -->|35| I6["I6 · Parcela B"]
    I7 -->|30| I8["I8 · Parcela C"]
    I7 -->|25| I9["I9 · Parcela D"]
    I10 -->|40| I7
    linkStyle 4 stroke:#b42318,stroke-dasharray:5 5
```

## Después de cerrar también I2 → I10

I9 permanece en la red, pero ya no es alcanzable desde I1. Las parcelas I5 e I6 siguen conectadas.

```mermaid
flowchart LR
    I1["I1 · Reservorio"] -->|120| I2["I2 · Filtro"]
    I2 -->|100| I3["I3 · Bomba"]
    I2 -. "cerrada · 50" .-> I10["I10 · Cisterna Alterna"]
    I3 -->|70| I4["I4 · Válvula Norte"]
    I3 -. "cerrada · 60" .-> I7["I7 · Válvula Sur"]
    I4 -->|35| I5["I5 · Parcela A"]
    I4 -->|35| I6["I6 · Parcela B"]
    I7 -->|30| I8["I8 · Parcela C"]
    I7 -->|25| I9["I9 · Parcela D"]
    I10 -->|40| I7
    linkStyle 2,4 stroke:#b42318,stroke-dasharray:5 5
```

## UML de clases y colaboración

`SistemaRiego` recibe la instancia de `Grafo` y opera sobre ella sin hacer una copia. Las eliminaciones de aristas quedan visibles de inmediato en BFS, DFS y las representaciones que consultan esa misma instancia.

```mermaid
classDiagram
    class Nodo {
        +str codigo
        +str nombre
        +dict salidas
    }
    class Grafo {
        -dict nodos
        +agregar_vertice(codigo, nombre)
        +agregar_arista(origen, destino, peso)
        +eliminar_arista(origen, destino) bool
        +existe_arista(origen, destino) bool
        +vecinos(codigo) list
        +codigos() list
        +bfs(origen) list
        +ruta_bfs(origen, destino) list | None
        +traza_bfs(origen) list
        +dfs(origen) list
        +traza_dfs(origen) list
        +alcanzables_desde(origen) set
        +a_lista_adyacencia() dict
        +a_matriz_adyacencia() list
    }
    class SistemaRiego {
        -Grafo grafo
        +parcelas_alcanzables(origen) list
        +cerrar_valvula(origen, destino) bool
        +cuello_botella_de_ruta(ruta) float
    }
    class BFS {
        +bfs(grafo, origen) list
        +ruta_bfs(grafo, origen, destino) list | None
        +traza_bfs(grafo, origen) list
    }
    class DFS {
        +dfs(grafo, origen) list
        +alcanzables_desde(grafo, origen) set
        +traza_dfs(grafo, origen) list
    }
    class Representaciones {
        +a_lista_adyacencia(grafo) dict
        +a_matriz_adyacencia(grafo) list
    }

    Grafo "1" *-- "0..*" Nodo : encapsula
    SistemaRiego --> Grafo : comparte la instancia
    Grafo ..> BFS : delega recorridos
    Grafo ..> DFS : delega recorridos
    Grafo ..> Representaciones : delega conversiones
```

## Una celda y su entrada correspondiente

En la matriz original, la fila `I2` y columna `I10` contiene `50`. La misma conexión aparece en la lista de `I2` como `("I10", 50)`. El valor cero en esa celda tras cerrar la conexión indica que dejó de existir; `I10` continúa en la lista como vértice, aunque ya no figure como vecino de `I2`.
