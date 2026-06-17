"""
Módulo que define la clase Gasto.
Representa un movimiento financiero (ingreso o gasto) del usuario.
"""

from datetime import datetime


class Gasto:
    """
    Representa un movimiento financiero registrado por el usuario.
    Puede ser un ingreso (positivo) o un gasto (negativo).
    """

    CATEGORIAS_VALIDAS = [
        "Alimentación",
        "Transporte",
        "Entretenimiento",
        "Salud",
        "Educación",
        "Ropa",
        "Servicios",
        "Ingreso",
        "Otros",
    ]

    def __init__(self, descripcion: str, monto: float, categoria: str, fecha: str = None):
        """
        Inicializa un nuevo movimiento financiero.

        Args:
            descripcion: Texto que describe el movimiento.
            monto: Valor del movimiento. Negativo = gasto, Positivo = ingreso.
            categoria: Categoría del movimiento (debe estar en CATEGORIAS_VALIDAS).
            fecha: Fecha en formato 'YYYY-MM-DD'. Si no se pasa, usa la fecha actual.

        Raises:
            ValueError: Si la descripción está vacía, el monto es 0, o la categoría no es válida.
        """
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía.")

        if monto == 0:
            raise ValueError("El monto no puede ser cero.")

        if categoria not in self.CATEGORIAS_VALIDAS:
            raise ValueError(
                f"Categoría inválida. Opciones: {', '.join(self.CATEGORIAS_VALIDAS)}"
            )

        self.descripcion = descripcion.strip()
        self.monto = round(float(monto), 2)
        self.categoria = categoria
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d")

    def es_ingreso(self) -> bool:
        """Retorna True si el movimiento es un ingreso (monto positivo)."""
        return self.monto > 0

    def es_gasto(self) -> bool:
        """Retorna True si el movimiento es un gasto (monto negativo)."""
        return self.monto < 0

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario para serialización."""
        return {
            "descripcion": self.descripcion,
            "monto": self.monto,
            "categoria": self.categoria,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Gasto":
        """Crea un objeto Gasto a partir de un diccionario."""
        return cls(
            descripcion=data["descripcion"],
            monto=data["monto"],
            categoria=data["categoria"],
            fecha=data["fecha"],
        )

    def __str__(self) -> str:
        tipo = "Ingreso" if self.es_ingreso() else "Gasto"
        return f"[{self.fecha}] {tipo} | {self.categoria} | {self.descripcion}: ${self.monto:,.2f}"
