"""Menú interactivo y demostración de la red de riego."""
from __future__ import annotations

from aplicacion import SistemaRiego
from datos import cargar_red
from dfs import PasoDFS
from bfs import PasoBFS


def _ruta_como_texto(sistema: SistemaRiego, ruta: list[str]) -> str:
    """Presenta códigos y nombres en una ruta."""
    return " -> ".join(
        f"{codigo} ({sistema.grafo.nombre(codigo)})" for codigo in ruta
    )


def _capacidades(sistema: SistemaRiego, ruta: list[str]) -> list[float]:
    """Obtiene los pesos de los tramos de una ruta existente."""
    capacidades: list[float] = []
    for origen, destino in zip(ruta, ruta[1:]):
        capacidades.append(dict(sistema.grafo.vecinos(origen))[destino])
    return capacidades


def mostrar_consulta_principal(sistema: SistemaRiego) -> None:
    """Muestra accesibilidad, ruta mínima en enlaces y parcelas desde I1."""
    origen, destino = "I1", "I9"
    alcanzables = sistema.grafo.alcanzables_desde(origen)
    ruta = sistema.grafo.ruta_bfs(origen, destino)

    print(f"\n¿{destino} es alcanzable desde {origen}?: {'Sí' if destino in alcanzables else 'No'}")
    print("Parcelas alcanzables:", ", ".join(sistema.parcelas_alcanzables(origen)) or "ninguna")
    if ruta is None:
        print(f"No existe ruta de {origen} a {destino}.")
        return

    capacidades = _capacidades(sistema, ruta)
    print("Ruta BFS:", _ruta_como_texto(sistema, ruta))
    print("Número de enlaces:", len(ruta) - 1)
    print("Capacidades nominales (L/min):", capacidades)
    print(
        "Menor capacidad nominal de la ruta:",
        f"{sistema.cuello_botella_de_ruta(ruta)} L/min",
    )


def mostrar_recorridos(sistema: SistemaRiego) -> None:
    """Imprime BFS y DFS junto con sus trazas de cola y pila."""
    grafo = sistema.grafo
    origen = "I1"
    print("\nBFS desde I1:", " -> ".join(grafo.bfs(origen)))
    print("Traza BFS (cola al final de cada paso):")
    for numero, paso in enumerate(grafo.traza_bfs(origen), start=1):
        assert isinstance(paso, PasoBFS)
        print(
            f"  {numero}. atiende {paso.actual}; "
            f"descubre {paso.descubiertos or 'ninguno'}; cola={paso.cola}"
        )

    print("\nDFS desde I1:", " -> ".join(grafo.dfs(origen)))
    print("Traza DFS (tope de la pila a la derecha):")
    for numero, paso in enumerate(grafo.traza_dfs(origen), start=1):
        assert isinstance(paso, PasoDFS)
        print(
            f"  {numero}. atiende {paso.actual}; "
            f"inserta {paso.descubiertos or 'ninguno'}; pila={paso.pila}"
        )


def mostrar_representaciones(sistema: SistemaRiego) -> None:
    """Muestra lista y matriz ponderadas sobre la instancia actual."""
    grafo = sistema.grafo
    print("\nLista de adyacencia (destino, capacidad L/min):")
    for codigo, vecinos in grafo.a_lista_adyacencia().items():
        print(f"  {codigo} ({grafo.nombre(codigo)}): {vecinos}")

    codigos = grafo.codigos()
    matriz = grafo.a_matriz_adyacencia()
    ancho = 6
    print("\nMatriz de adyacencia ponderada (0 = sin arista):")
    print("".ljust(ancho) + "".join(codigo.rjust(ancho) for codigo in codigos))
    for codigo, fila in zip(codigos, matriz):
        valores = "".join(str(peso).rjust(ancho) for peso in fila)
        print(f"{codigo:<{ancho}}{valores}")


def mostrar_estado_experimento(sistema: SistemaRiego, etiqueta: str) -> None:
    """Informa los resultados calculados para el estado actual del grafo."""
    origen, destino = "I1", "I9"
    alcanzables = sistema.grafo.alcanzables_desde(origen)
    ruta = sistema.grafo.ruta_bfs(origen, destino)
    print(f"\n{etiqueta}")
    print(f"  I9 alcanzable desde I1: {'Sí' if destino in alcanzables else 'No'}")
    print("  Parcelas alcanzables:", sistema.parcelas_alcanzables(origen) or "ninguna")
    if ruta is None:
        print("  Ruta: no existe; ruta_bfs devuelve None.")
        print("  Número de enlaces: no aplica.")
        print("  Capacidades: no hay tramos que evaluar.")
        return

    capacidades = _capacidades(sistema, ruta)
    print("  Ruta:", " -> ".join(ruta))
    print(f"  Número de enlaces: {len(ruta) - 1}")
    print(f"  Capacidades (L/min): {capacidades}")
    print(
        "  Mínimo nominal de la ruta:",
        f"{sistema.cuello_botella_de_ruta(ruta)} L/min",
    )


def ejecutar_experimento() -> SistemaRiego:
    """Reinicia la red y reproduce los dos cierres sucesivos del enunciado."""
    sistema = SistemaRiego(cargar_red())
    mostrar_estado_experimento(sistema, "1. Red original")

    sistema.cerrar_valvula("I3", "I7")
    mostrar_estado_experimento(sistema, "2. Después de cerrar I3 -> I7")

    sistema.cerrar_valvula("I2", "I10")
    mostrar_estado_experimento(sistema, "3. Después de cerrar I2 -> I10")
    print(
        "\nEl mínimo nominal describe los pesos de una ruta; el prototipo no calcula "
        "el comportamiento hidráulico de la red."
    )
    return sistema


def _cerrar_conexion(sistema: SistemaRiego) -> None:
    """Cierra una conexión elegida e informa si existía."""
    origen = input("Código de origen: ").strip().upper()
    destino = input("Código de destino: ").strip().upper()
    try:
        eliminada = sistema.cerrar_valvula(origen, destino)
    except KeyError as error:
        print(f"Código inexistente: {error.args[0]}")
        return
    print(
        f"Conexión {origen} -> {destino} "
        f"{'cerrada' if eliminada else 'no existía; el grafo no cambió'}."
    )


def main() -> None:
    """Ejecuta el menú; todas las consultas comparten el grafo actual."""
    sistema = SistemaRiego(cargar_red())
    while True:
        print(
            "\n=== Sistema de riego ===\n"
            "1. Consultar accesibilidad, ruta y parcelas desde I1\n"
            "2. Mostrar recorridos BFS/DFS y trazas\n"
            "3. Mostrar lista y matriz de adyacencia\n"
            "4. Ejecutar experimento completo de cierres\n"
            "5. Cerrar una conexión manualmente\n"
            "0. Salir"
        )
        try:
            opcion = input("Opción: ").strip()
        except EOFError:
            print("\nFin de la entrada.")
            return

        if opcion == "1":
            mostrar_consulta_principal(sistema)
        elif opcion == "2":
            mostrar_recorridos(sistema)
        elif opcion == "3":
            mostrar_representaciones(sistema)
        elif opcion == "4":
            # El experimento siempre inicia con una red nueva y deja esa misma
            # instancia como la red activa para las consultas siguientes.
            sistema = ejecutar_experimento()
        elif opcion == "5":
            _cerrar_conexion(sistema)
        elif opcion == "0":
            print("Fin del sistema de riego.")
            return
        else:
            print("Opción no válida; elige una de las opciones del menú.")


if __name__ == "__main__":
    main()
