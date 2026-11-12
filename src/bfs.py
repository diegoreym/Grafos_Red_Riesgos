"""Recorrido por amplitud, rutas y traza para la red de riego."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grafo import Grafo


@dataclass
class PasoBFS:
    """Estado al terminar de explorar los vecinos de un nodo."""
    actual: str
    descubiertos: list[str]
    cola: list[str]


def _recorrer(grafo: Grafo, origen: str, pasos: list[PasoBFS] | None = None
              ) -> tuple[list[str], dict[str, str]]:
    """Marca al encolar y conserva el primer predecesor de cada vértice."""
    cola = deque([origen])
    visitados = {origen}
    orden: list[str] = []
    predecesor: dict[str, str] = {}
    while cola:
        actual = cola.popleft()
        orden.append(actual)
        nuevos: list[str] = []
        for vecino, _ in grafo.vecinos(actual):
            if vecino in visitados:
                continue
            visitados.add(vecino)
            predecesor[vecino] = actual
            cola.append(vecino)
            if pasos is not None:
                nuevos.append(vecino)
        if pasos is not None:
            pasos.append(PasoBFS(actual, nuevos, list(cola)))
    return orden, predecesor


def bfs(grafo: Grafo, origen: str) -> list[str]:
    """Devuelve el orden de visita desde origen."""
    orden, _ = _recorrer(grafo, origen)
    return orden


def ruta_bfs(grafo: Grafo, origen: str, destino: str) -> list[str] | None:
    """Distingue destino inexistente (KeyError) de inalcanzable (None)."""
    grafo.nombre(destino)
    _, predecesor = _recorrer(grafo, origen)
    if destino != origen and destino not in predecesor:
        return None
    ruta = [destino]
    while ruta[-1] != origen:
        ruta.append(predecesor[ruta[-1]])
    ruta.reverse()
    return ruta


def traza_bfs(grafo: Grafo, origen: str) -> list[PasoBFS]:
    """Devuelve los pasos del mismo algoritmo utilizado por bfs y ruta_bfs."""
    pasos: list[PasoBFS] = []
    _recorrer(grafo, origen, pasos)
    return pasos
