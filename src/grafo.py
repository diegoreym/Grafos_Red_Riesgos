"""Grafo dirigido y ponderado de la red de riego."""
from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
import re
import bfs as recorrido
import dfs as profundidad


@dataclass
class Nodo:
    """Vértice con sus conexiones salientes y capacidades nominales."""
    codigo: str
    nombre: str
    salidas: dict[str, float] = field(default_factory=dict)


def _orden(codigo: str) -> tuple[str, int, str]:
    """Ordena por prefijo y sufijo numérico, por ejemplo I2 antes de I10."""
    partes = re.fullmatch(r"(.*?)([0-9]+)", codigo)
    if partes:
        return partes[1], int(partes[2]), codigo
    return codigo, -1, codigo


class Grafo:
    """Almacena un nodo por código y una conexión por destino."""

    def __init__(self) -> None:
        self.__nodos: dict[str, Nodo] = {}

    def agregar_vertice(self, codigo: str, nombre: str) -> None:
        """Registra un vértice con código único."""
        if codigo in self.__nodos:
            raise ValueError(f"Vértice repetido: {codigo}")
        self.__nodos[codigo] = Nodo(codigo, nombre)

    def codigos(self) -> list[str]:
        """Devuelve los códigos en el orden común de la red."""
        return sorted(self.__nodos, key=_orden)

    def nombre(self, codigo: str) -> str:
        """Consulta el nombre del nodo. Un código inexistente genera KeyError."""
        return self.__nodos[codigo].nombre

    def agregar_arista(self, origen: str, destino: str, peso: float = 1) -> None:
        """Agrega una conexión dirigida de capacidad positiva."""
        if self.existe_arista(origen, destino):
            raise ValueError(f"Arista repetida: {origen} -> {destino}")
        if isinstance(peso, bool) or not isinstance(peso, (int, float)):
            raise TypeError("El peso debe ser numérico")
        if peso <= 0 or (isinstance(peso, float) and not isfinite(peso)):
            raise ValueError("El peso debe ser positivo y finito")
        self.__nodos[origen].salidas[destino] = peso

    def existe_arista(self, origen: str, destino: str) -> bool:
        """Comprueba la conexión entre dos vértices registrados."""
        nodo = self.__nodos[origen]
        if destino not in self.__nodos:
            raise KeyError(destino)
        return destino in nodo.salidas

    def eliminar_arista(self, origen: str, destino: str) -> bool:
        """Devuelve True si retiró la conexión indicada."""
        if not self.existe_arista(origen, destino):
            return False
        del self.__nodos[origen].salidas[destino]
        return True

    def vecinos(self, codigo: str) -> list[tuple[str, float]]:
        """Devuelve pares (destino, peso) en orden ascendente."""
        salidas = self.__nodos[codigo].salidas
        return [(v, salidas[v]) for v in sorted(salidas, key=_orden)]

    def bfs(self, origen: str) -> list[str]:
        """Recorre por amplitud desde el origen."""
        return recorrido.bfs(self, origen)

    def ruta_bfs(self, origen: str, destino: str) -> list[str] | None:
        """Devuelve una ruta con el mínimo número de enlaces."""
        return recorrido.ruta_bfs(self, origen, destino)

    def traza_bfs(self, origen: str) -> list[recorrido.PasoBFS]:
        """Muestra el estado de la cola después de atender cada nodo."""
        return recorrido.traza_bfs(self, origen)

    def dfs(self, origen: str) -> list[str]:
        """Delega el recorrido en profundidad."""
        return profundidad.dfs(self, origen)

    def traza_dfs(self, origen: str) -> list[profundidad.PasoDFS]:
        """Devuelve los estados de la pila generados por el DFS."""
        return profundidad.traza_dfs(self, origen)

    def alcanzables_desde(self, origen: str) -> set[str]:
        """Devuelve los vértices alcanzables en el sentido de las aristas."""
        return profundidad.alcanzables_desde(self, origen)

    def a_lista_adyacencia(self) -> dict[str, list[tuple[str, float]]]:
        """Devuelve una copia de la lista de adyacencia ponderada."""
        from representaciones import a_lista_adyacencia
        return a_lista_adyacencia(self)

    def a_matriz_adyacencia(self) -> list[list[float]]:
        """Devuelve la matriz cuyas filas y columnas siguen codigos()."""
        from representaciones import a_matriz_adyacencia
        return a_matriz_adyacencia(self)
