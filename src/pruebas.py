"""Pruebas integradas del TAD, recorridos y sistema de riego.

Ejecutar desde esta carpeta con ``python pruebas.py``.
"""
import math
import unittest

from aplicacion import SistemaRiego
from datos import cargar_red
from grafo import Grafo


class PruebasRedRiego(unittest.TestCase):
    """Cada caso parte de una instancia nueva de la red oficial."""

    def setUp(self) -> None:
        self.grafo = cargar_red()
        self.sistema = SistemaRiego(self.grafo)

    def test_datos_direccion_pesos_y_representaciones_manuales(self) -> None:
        """Contrasta lista y matriz con los datos del enunciado."""
        lista_esperada = {
            "I1": [("I2", 120)],
            "I2": [("I3", 100), ("I10", 50)],
            "I3": [("I4", 70), ("I7", 60)],
            "I4": [("I5", 35), ("I6", 35)],
            "I5": [],
            "I6": [],
            "I7": [("I8", 30), ("I9", 25)],
            "I8": [],
            "I9": [],
            "I10": [("I7", 40)],
        }
        codigos = [f"I{i}" for i in range(1, 11)]
        # Matriz de referencia construida manualmente desde la tabla del PDF.
        matriz_esperada = [
            [0, 120, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 100, 0, 0, 0, 0, 0, 0, 50],
            [0, 0, 0, 70, 0, 0, 60, 0, 0, 0],
            [0, 0, 0, 0, 35, 35, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 30, 25, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 40, 0, 0, 0],
        ]

        self.assertEqual(self.grafo.codigos(), codigos)
        self.assertEqual(self.grafo.a_lista_adyacencia(), lista_esperada)
        self.assertEqual(self.grafo.a_matriz_adyacencia(), matriz_esperada)
        self.assertTrue(self.grafo.existe_arista("I1", "I2"))
        self.assertEqual(dict(self.grafo.vecinos("I1"))["I2"], 120)
        self.assertFalse(self.grafo.existe_arista("I2", "I1"))

    def test_representaciones_son_copias(self) -> None:
        lista = self.grafo.a_lista_adyacencia()
        matriz = self.grafo.a_matriz_adyacencia()
        lista["I1"].clear()
        matriz[0][1] = 999
        self.assertEqual(self.grafo.vecinos("I1"), [("I2", 120)])
        self.assertEqual(self.grafo.a_matriz_adyacencia()[0][1], 120)

    def test_bfs_y_ruta_con_menos_enlaces(self) -> None:
        self.assertEqual(
            self.grafo.bfs("I1"),
            ["I1", "I2", "I3", "I10", "I4", "I7", "I5", "I6", "I8", "I9"],
        )
        self.assertEqual(
            self.grafo.ruta_bfs("I1", "I9"),
            ["I1", "I2", "I3", "I7", "I9"],
        )
        self.assertEqual(self.grafo.ruta_bfs("I1", "I1"), ["I1"])

    def test_bfs_inalcanzable_devuelve_none(self) -> None:
        grafo = Grafo()
        grafo.agregar_vertice("A", "Origen")
        grafo.agregar_vertice("B", "Destino")
        self.assertIsNone(grafo.ruta_bfs("A", "B"))

    def test_traza_bfs_muestra_iteraciones_reales(self) -> None:
        pasos = self.grafo.traza_bfs("I1")
        self.assertGreaterEqual(len(pasos), 3)
        self.assertEqual((pasos[0].actual, pasos[0].descubiertos, pasos[0].cola),
                         ("I1", ["I2"], ["I2"]))
        self.assertEqual((pasos[1].actual, pasos[1].descubiertos, pasos[1].cola),
                         ("I2", ["I3", "I10"], ["I3", "I10"]))
        self.assertEqual((pasos[2].actual, pasos[2].descubiertos, pasos[2].cola),
                         ("I3", ["I4", "I7"], ["I10", "I4", "I7"]))

    def test_dfs_usa_orden_ascendente_y_es_dirigido(self) -> None:
        self.assertEqual(
            self.grafo.dfs("I1"),
            ["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"],
        )
        self.assertEqual(self.grafo.alcanzables_desde("I1"), set(self.grafo.codigos()))
        self.assertEqual(self.grafo.alcanzables_desde("I2"),
                         {"I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10"})
        self.assertNotIn("I1", self.grafo.alcanzables_desde("I2"))

    def test_traza_dfs_muestra_estados_reales_de_pila(self) -> None:
        pasos = self.grafo.traza_dfs("I1")
        self.assertGreaterEqual(len(pasos), 3)
        self.assertEqual((pasos[0].actual, pasos[0].descubiertos, pasos[0].pila),
                         ("I1", ["I2"], ["I2"]))
        self.assertEqual((pasos[1].actual, pasos[1].descubiertos, pasos[1].pila),
                         ("I2", ["I10", "I3"], ["I10", "I3"]))
        self.assertEqual((pasos[2].actual, pasos[2].descubiertos, pasos[2].pila),
                         ("I3", ["I7", "I4"], ["I10", "I7", "I4"]))

    def test_experimento_de_cierres_sucesivos(self) -> None:
        ruta_original = self.grafo.ruta_bfs("I1", "I9")
        self.assertEqual(self.sistema.parcelas_alcanzables("I1"),
                         ["I5", "I6", "I8", "I9"])
        self.assertEqual(ruta_original, ["I1", "I2", "I3", "I7", "I9"])
        self.assertEqual(self.sistema.cuello_botella_de_ruta(ruta_original), 25)

        self.assertTrue(self.sistema.cerrar_valvula("I3", "I7"))
        ruta_tras_primer_cierre = self.grafo.ruta_bfs("I1", "I9")
        self.assertEqual(ruta_tras_primer_cierre,
                         ["I1", "I2", "I10", "I7", "I9"])
        self.assertEqual(self.sistema.cuello_botella_de_ruta(ruta_tras_primer_cierre), 25)

        self.assertTrue(self.sistema.cerrar_valvula("I2", "I10"))
        self.assertIsNone(self.grafo.ruta_bfs("I1", "I9"))
        self.assertEqual(self.sistema.parcelas_alcanzables("I1"), ["I5", "I6"])

    def test_cierre_ausente_no_modifica_el_grafo(self) -> None:
        self.assertFalse(self.sistema.cerrar_valvula("I3", "I1"))
        self.assertEqual(self.grafo.ruta_bfs("I1", "I9"),
                         ["I1", "I2", "I3", "I7", "I9"])

    def test_cuello_de_botella_valida_ruta_y_tramos(self) -> None:
        self.assertEqual(self.sistema.cuello_botella_de_ruta(["I1", "I2"]), 120)
        with self.assertRaises(ValueError):
            self.sistema.cuello_botella_de_ruta([])
        with self.assertRaises(ValueError):
            self.sistema.cuello_botella_de_ruta(["I1"])
        with self.assertRaises(ValueError):
            self.sistema.cuello_botella_de_ruta(["I1", "I4"])
        with self.assertRaises(KeyError):
            self.sistema.cuello_botella_de_ruta(["I1", "I99"])

    def test_codigos_inexistentes_generan_key_error(self) -> None:
        for consulta in (
            lambda: self.grafo.vecinos("I99"),
            lambda: self.grafo.bfs("I99"),
            lambda: self.grafo.alcanzables_desde("I99"),
            lambda: self.grafo.ruta_bfs("I1", "I99"),
            lambda: self.grafo.existe_arista("I1", "I99"),
        ):
            with self.subTest(consulta=consulta):
                with self.assertRaises(KeyError):
                    consulta()

    def test_duplicados_y_pesos_invalidos_no_alteran_el_grafo(self) -> None:
        with self.assertRaises(ValueError):
            self.grafo.agregar_vertice("I1", "Duplicado")
        with self.assertRaises(ValueError):
            self.grafo.agregar_arista("I1", "I2", 1)
        self.assertEqual(self.grafo.vecinos("I1"), [("I2", 120)])

        for peso in (0, -1, math.inf, -math.inf, math.nan):
            with self.subTest(peso=peso):
                with self.assertRaises(ValueError):
                    self.grafo.agregar_arista("I1", "I5", peso)
                self.assertFalse(self.grafo.existe_arista("I1", "I5"))
        with self.assertRaises(TypeError):
            self.grafo.agregar_arista("I1", "I5", "120")


if __name__ == "__main__":
    unittest.main(verbosity=2)
