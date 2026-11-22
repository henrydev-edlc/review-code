import unittest

from cajero_automatico import CajeroAutomatico


class TestConsultar(unittest.TestCase):
    def test_consultar_formato(self):
        self.assertEqual(CajeroAutomatico("Ana", 100).consultar(),
                         "El saldo actual de Ana es: $100.00")

    def test_saldo_inicial_por_defecto_cero(self):
        self.assertEqual(CajeroAutomatico("Luis").saldo, 0)

    def test_saldo_inicial_negativo_rechazado(self):
        with self.assertRaises(ValueError):
            CajeroAutomatico("Ana", -50)


class TestDepositar(unittest.TestCase):
    def test_deposito_valido(self):
        c = CajeroAutomatico("Ana", 100)
        c.depositar(50)
        self.assertEqual(c.saldo, 150)

    def test_deposito_cero(self):
        with self.assertRaises(ValueError):
            CajeroAutomatico("Ana", 100).depositar(0)

    def test_deposito_negativo(self):
        with self.assertRaises(ValueError):
            CajeroAutomatico("Ana", 100).depositar(-10)

    def test_deposito_no_numerico(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", 100).depositar("10")


class TestRetirar(unittest.TestCase):
    def test_retiro_valido(self):
        c = CajeroAutomatico("Ana", 100)
        c.retirar(40)
        self.assertEqual(c.saldo, 60)

    def test_retiro_saldo_exacto(self):
        c = CajeroAutomatico("Ana", 100)
        c.retirar(100)
        self.assertEqual(c.saldo, 0)

    def test_retiro_mayor_al_saldo(self):
        c = CajeroAutomatico("Ana", 100)
        with self.assertRaises(ValueError):
            c.retirar(150)
        self.assertEqual(c.saldo, 100)

    def test_retiro_cero(self):
        c = CajeroAutomatico("Ana", 100)
        with self.assertRaises(ValueError):
            c.retirar(0)

    def test_retiro_negativo_no_aumenta_saldo(self):
        c = CajeroAutomatico("Ana", 100)
        with self.assertRaises(ValueError):
            c.retirar(-50)
        self.assertEqual(c.saldo, 100)

    def test_retiro_sin_fondos_cuenta_vacia(self):
        c = CajeroAutomatico("Luis")
        with self.assertRaises(ValueError):
            c.retirar(1)
        self.assertGreaterEqual(c.saldo, 0)

    def test_retiro_no_numerico(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", 100).retirar("10")


class TestTransferencia(unittest.TestCase):
    def setUp(self):
        self.a = CajeroAutomatico("Ana", 100)
        self.b = CajeroAutomatico("Luis", 0)

    def test_transferencia_valida_acredita_destino(self):
        self.a.transferencia(self.b, 30)
        self.assertEqual(self.a.saldo, 70)
        self.assertEqual(self.b.saldo, 30)

    def test_transferencia_conserva_dinero_total(self):
        self.a.transferencia(self.b, 30)
        self.assertEqual(self.a.saldo + self.b.saldo, 100)

    def test_transferencia_saldo_exacto(self):
        self.a.transferencia(self.b, 100)
        self.assertEqual((self.a.saldo, self.b.saldo), (0, 100))

    def test_transferencia_fondos_insuficientes(self):
        with self.assertRaises(ValueError):
            self.a.transferencia(self.b, 500)
        self.assertEqual(self.a.saldo, 100)
        self.assertEqual(self.b.saldo, 0)

    def test_transferencia_monto_negativo(self):
        with self.assertRaises(ValueError):
            self.a.transferencia(self.b, -20)
        self.assertEqual(self.a.saldo, 100)
        self.assertEqual(self.b.saldo, 0)

    def test_transferencia_monto_cero(self):
        with self.assertRaises(ValueError):
            self.a.transferencia(self.b, 0)

    def test_transferencia_a_si_mismo(self):
        with self.assertRaises(ValueError):
            self.a.transferencia(self.a, 10)
        self.assertEqual(self.a.saldo, 100)

    def test_transferencia_destino_invalido(self):
        with self.assertRaises((ValueError, TypeError, AttributeError)):
            self.a.transferencia(None, 10)
        self.assertEqual(self.a.saldo, 100)

    def test_transferencia_destino_invalido_no_descuenta(self):
        try:
            self.a.transferencia(None, 10)
        except Exception:
            pass
        self.assertEqual(self.a.saldo, 100)


if __name__ == "__main__":
    unittest.main()
