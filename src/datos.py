
"""
Construye un grafo dirigido y ponderado con los
10 vértices y 10 aristas del enunciado.
"""

from grafo import Grafo


# Vértices de la red de riego: (código, nombre)
VERTICES = (
    ("I1", "Reservorio"),
    ("I2", "Filtro"),
    ("I3", "Bomba"),
    ("I4", "Válvula Norte"),
    ("I5", "Parcela A"),
    ("I6", "Parcela B"),
    ("I7", "Válvula Sur"),
    ("I8", "Parcela C"),
    ("I9", "Parcela D"),
    ("I10", "Cisterna Alterna"),
)


# Aristas dirigidas: (origen, destino, capacidad en L/min)
ARISTAS = (
    ("I1", "I2", 120),
    ("I2", "I3", 100),
    ("I3", "I4", 70),
    ("I3", "I7", 60),
    ("I4", "I5", 35),
    ("I4", "I6", 35),
    ("I7", "I8", 30),
    ("I7", "I9", 25),
    ("I10", "I7", 40),
    ("I2", "I10", 50),
)


def cargar_red() -> Grafo:
    grafo = Grafo()

    # Registrar los vértices
    for codigo, nombre in VERTICES:
        grafo.agregar_vertice(codigo, nombre)

    # Registrar las conexiones dirigidas y sus pesos
    for origen, destino, peso in ARISTAS:
        grafo.agregar_arista(origen, destino, peso)

    return grafo

