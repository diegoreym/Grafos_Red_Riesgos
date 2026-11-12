"""Recorrido en profundidad y traza de pila para grafos dirigidos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grafo import Grafo


@dataclass
class PasoDFS:
    """Estado de la pila tras atender un vértice.

    ``pila`` muestra el tope en el extremo derecho. ``descubiertos`` está en
    orden de inserción, por lo que el último elemento es el próximo en atender.
    """

    actual: str
    descubiertos: list[str]
    pila: list[str]


def _recorrer(
    grafo: Grafo, origen: str, pasos: list[PasoDFS] | None = None
) -> list[str]:
    """Ejecuta DFS iterativo y visita primero el vecino de menor código."""
    grafo.nombre(origen)  # valida incluso cuando el grafo no tiene vértices
    pila = [origen]
    visitados: set[str] = set()
    orden: list[str] = []

    while pila:
        actual = pila.pop()
        if actual in visitados:
            continue

        visitados.add(actual)
        orden.append(actual)
        descubiertos: list[str] = []
        # La pila es LIFO: se insertan al revés para visitar el menor primero.
        for destino, _ in reversed(grafo.vecinos(actual)):
            if destino not in visitados:
                pila.append(destino)
                descubiertos.append(destino)

        if pasos is not None:
            pasos.append(PasoDFS(actual, descubiertos, list(pila)))

    return orden


def dfs(grafo: Grafo, origen: str) -> list[str]:
    """Devuelve el orden de visita en profundidad desde ``origen``."""
    return _recorrer(grafo, origen)


def alcanzables_desde(grafo: Grafo, origen: str) -> set[str]:
    """Devuelve los vértices alcanzables, incluyendo el origen."""
    return set(_recorrer(grafo, origen))


def traza_dfs(grafo: Grafo, origen: str) -> list[PasoDFS]:
    """Devuelve los estados reales de la pila del recorrido DFS."""
    pasos: list[PasoDFS] = []
    _recorrer(grafo, origen, pasos)
    return pasos
