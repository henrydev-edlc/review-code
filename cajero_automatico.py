import math


def _validar_numero(valor, nombre):
    """Valida que el valor sea un número real finito (no bool, NaN ni infinito)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"{nombre} debe ser un número.")
    if not math.isfinite(valor):
        raise ValueError(f"{nombre} debe ser un número finito.")


class CajeroAutomatico:
    def __init__(self, titular, saldo_inicial=0.0):
        _validar_numero(saldo_inicial, "El saldo inicial")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.titular = titular
        self.saldo = saldo_inicial

    def consultar(self):
        """Devuelve el saldo actual de la cuenta."""
        return f"El saldo actual de {self.titular} es: ${self.saldo:.2f}"

    def retirar(self, monto):
        """Permite retirar dinero de la cuenta."""
        _validar_numero(monto, "El monto a retirar")
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor a cero.")
        if monto > self.saldo:
            raise ValueError("Fondos insuficientes.")
        self.saldo -= monto
        return f"Retiro exitoso de ${monto:.2f}. Nuevo saldo: ${self.saldo:.2f}"

    def depositar(self, monto):
        """Permite depositar dinero en la cuenta."""
        _validar_numero(monto, "El monto a depositar")
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser mayor a cero.")
        self.saldo += monto
        return f"Depósito exitoso de ${monto:.2f}. Nuevo saldo: ${self.saldo:.2f}"

    def transferencia(self, cuenta_destino, monto):
        """Transfiere dinero a otra cuenta de destino."""
        if not isinstance(cuenta_destino, CajeroAutomatico):
            raise TypeError("La cuenta de destino no es válida.")
        if cuenta_destino is self:
            raise ValueError("No se puede transferir a la misma cuenta.")
        _validar_numero(monto, "El monto a transferir")
        if monto <= 0:
            raise ValueError("El monto a transferir debe ser mayor a cero.")
        if monto > self.saldo:
            raise ValueError("Fondos insuficientes.")
        self.saldo -= monto
        cuenta_destino.saldo += monto
        return f"Transferencia exitosa de ${monto:.2f} a {cuenta_destino.titular}. Nuevo saldo: ${self.saldo:.2f}"
