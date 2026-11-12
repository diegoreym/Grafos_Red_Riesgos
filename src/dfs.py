def dfs(grafo, origen: str) -> list[str]:
    pila = [origen]
    visitados = set()
    recorrido = []
    
    while pila:
        actual = pila.pop()
 
        if actual not in visitados:
            visitados.add(actual)
            recorrido.append(actual)
            
            for destino, peso in reversed(grafo.vecinos(actual)):
                if destino not in visitados:
                    pila.append(destino)
                    
    return recorrido


def alcanzables_desde(grafo, origen: str) -> set[str]:
    return set(dfs(grafo, origen))
