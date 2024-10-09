# tests/test_gestor_ventas.py
#unittest es un módulo de Python que se utiliza para escribir y ejecutar pruebas unitarias, lo que permite verificar que las partes individuales de tu código (generalmente funciones o métodos) se comporten como se espera
import unittest
from gestor_ventas.gestor_ventas import GestorVentas
from gestor_ventas.exceptions import ImpuestoInvalidoError, DescuentoInvalidoError

class TestGestorVentas(unittest.TestCase):

    def test_calculo_precio_final(self):
        gestor = GestorVentas(100.0, 0.05, 0.10)  # 5% de impuesto, 10% de descuento
        self.assertEqual(gestor.calcular_precio_final(), 95.0)

    def test_impuesto_invalido(self):
        with self.assertRaises(ImpuestoInvalidoError):
            GestorVentas(100.0, 1.5, 0.10)  # Impuesto mayor a 1

    def test_descuento_invalido(self):
        with self.assertRaises(DescuentoInvalidoError):
            GestorVentas(100.0, 0.05, 1.5)  # Descuento mayor a 1

if __name__ == "__main__":
    unittest.main()
