import math
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


NAN = float("nan")
INF = float("inf")


class TestSaldoInicialInvalido(unittest.TestCase):
    def test_saldo_inicial_string_numerico(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", "100")

    def test_saldo_inicial_string_no_numerico(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", "abc")

    def test_saldo_inicial_none(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", None)

    def test_saldo_inicial_lista(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", [100])

    def test_saldo_inicial_bool(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", True)

    def test_saldo_inicial_nan(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", NAN)

    def test_saldo_inicial_inf(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", INF)

    def test_saldo_inicial_menos_inf(self):
        with self.assertRaises((ValueError, TypeError)):
            CajeroAutomatico("Ana", -INF)


class TestNaNInfOperaciones(unittest.TestCase):
    def setUp(self):
        self.a = CajeroAutomatico("Ana", 100)
        self.b = CajeroAutomatico("Luis", 0)

    def test_depositar_nan(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.depositar(NAN)
        self.assertEqual(self.a.saldo, 100)

    def test_depositar_inf(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.depositar(INF)
        self.assertEqual(self.a.saldo, 100)

    def test_retirar_nan(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.retirar(NAN)
        self.assertEqual(self.a.saldo, 100)

    def test_retirar_inf(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.retirar(INF)
        self.assertEqual(self.a.saldo, 100)

    def test_transferencia_nan(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.transferencia(self.b, NAN)
        self.assertEqual(self.a.saldo, 100)
        self.assertEqual(self.b.saldo, 0)

    def test_transferencia_inf(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.transferencia(self.b, INF)
        self.assertEqual(self.a.saldo, 100)
        self.assertEqual(self.b.saldo, 0)

    def test_transferencia_monto_no_numerico(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.transferencia(self.b, "10")
        self.assertEqual(self.a.saldo, 100)
        self.assertEqual(self.b.saldo, 0)

    def test_transferencia_monto_none(self):
        with self.assertRaises((ValueError, TypeError)):
            self.a.transferencia(self.b, None)

    def test_saldo_nunca_nan_tras_operaciones(self):
        for op in (lambda: self.a.depositar(NAN),
                   lambda: self.a.retirar(NAN),
                   lambda: self.a.transferencia(self.b, NAN)):
            try:
                op()
            except (ValueError, TypeError):
                pass
        self.assertFalse(math.isnan(self.a.saldo))
        self.assertFalse(math.isnan(self.b.saldo))


class TestFormatoMensajes(unittest.TestCase):
    def test_depositar_mensaje(self):
        c = CajeroAutomatico("Ana", 100)
        self.assertEqual(c.depositar(50),
                         "Depósito exitoso de $50.00. Nuevo saldo: $150.00")

    def test_depositar_mensaje_decimales(self):
        c = CajeroAutomatico("Ana", 0.5)
        self.assertEqual(c.depositar(1.25),
                         "Depósito exitoso de $1.25. Nuevo saldo: $1.75")

    def test_retirar_mensaje(self):
        c = CajeroAutomatico("Ana", 100)
        self.assertEqual(c.retirar(40),
                         "Retiro exitoso de $40.00. Nuevo saldo: $60.00")

    def test_retirar_mensaje_saldo_cero(self):
        c = CajeroAutomatico("Ana", 100)
        self.assertEqual(c.retirar(100),
                         "Retiro exitoso de $100.00. Nuevo saldo: $0.00")

    def test_transferencia_mensaje(self):
        a = CajeroAutomatico("Ana", 100)
        b = CajeroAutomatico("Luis")
        self.assertEqual(
            a.transferencia(b, 30),
            "Transferencia exitosa de $30.00 a Luis. Nuevo saldo: $70.00")

    def test_mensajes_son_str(self):
        a = CajeroAutomatico("Ana", 100)
        b = CajeroAutomatico("Luis")
        self.assertIsInstance(a.depositar(1), str)
        self.assertIsInstance(a.retirar(1), str)
        self.assertIsInstance(a.transferencia(b, 1), str)

    def test_consultar_tras_operaciones(self):
        a = CajeroAutomatico("Ana", 100)
        b = CajeroAutomatico("Luis")
        a.transferencia(b, 30)
        self.assertEqual(b.consultar(), "El saldo actual de Luis es: $30.00")


if __name__ == "__main__":
    unittest.main()
