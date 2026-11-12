
"""
Genera la lista y matriz de adyacencia de un grafo
dirigido y ponderado, conservando los pesos en L/min.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grafo import Grafo


def a_lista_adyacencia(
    grafo: Grafo
) -> dict[str, list[tuple[str, float]]]:  # sourcery skip: dict-comprehension

    lista: dict[str, list[tuple[str, float]]] = {}

    for codigo in grafo.codigos():
        lista[codigo] = grafo.vecinos(codigo)

    return lista


def a_matriz_adyacencia(grafo: Grafo) -> list[list[float]]:
    codigos = grafo.codigos()
    n = len(codigos)

    # Crear matriz cuadrada inicializada en cero
    matriz = [[0.0 for _ in range(n)] for _ in range(n)]

    # Asociar cada código con su posición
    indices = {
        codigo: i for i, codigo in enumerate(codigos)
    }

    # Registrar los pesos de las conexiones dirigidas
    for origen in codigos:
        i = indices[origen]

        for destino, peso in grafo.vecinos(origen):
            j = indices[destino]
            matriz[i][j] = peso

    return matriz

