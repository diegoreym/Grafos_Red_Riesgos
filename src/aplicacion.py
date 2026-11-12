"""Servicios de consulta y operación de la red de riego."""
from __future__ import annotations

from collections.abc import Sequence

from grafo import Grafo


class SistemaRiego:
    """Agrupa las consultas de riego sobre una instancia compartida de Grafo."""

    _PARCELAS = ("I5", "I6", "I8", "I9")

    def __init__(self, grafo: Grafo) -> None:
        """Crea el sistema sobre el grafo recibido, sin copiarlo."""
        self.__grafo = grafo

    @property
    def grafo(self) -> Grafo:
        """Expone la instancia compartida para consultas y representaciones."""
        return self.__grafo

    def parcelas_alcanzables(self, origen: str) -> list[str]:
        """Filtra las parcelas alcanzables y las devuelve en orden de código."""
        alcanzables = self.__grafo.alcanzables_desde(origen)
        codigos = set(self.__grafo.codigos())
        return [
            parcela
            for parcela in self._PARCELAS
            if parcela in codigos and parcela in alcanzables
        ]

    def cerrar_valvula(self, origen: str, destino: str) -> bool:
        """Elimina del grafo compartido la arista dirigida indicada."""
        return self.__grafo.eliminar_arista(origen, destino)

    def cuello_botella_de_ruta(self, ruta: Sequence[str]) -> float:
        """Devuelve el menor peso de una ruta válida que contenga una arista.

        Este valor describe el menor peso nominal del recorrido; no representa
        una simulación del caudal hidráulico de la red.
        """
        if ruta is None or len(ruta) < 2:
            raise ValueError("La ruta debe contener al menos un tramo")

        pesos: list[float] = []
        for origen, destino in zip(ruta, ruta[1:]):
            # Los códigos inválidos conservan el contrato KeyError del grafo.
            self.__grafo.nombre(origen)
            self.__grafo.nombre(destino)
            conexiones = dict(self.__grafo.vecinos(origen))
            if destino not in conexiones:
                raise ValueError(f"El tramo {origen} -> {destino} no existe")
            pesos.append(conexiones[destino])

        return min(pesos)
