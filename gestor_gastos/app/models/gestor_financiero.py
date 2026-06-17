"""
Módulo que define la clase GestorFinanciero.
Contiene la lógica principal del sistema: registrar, eliminar,
filtrar movimientos y generar estadísticas.
"""

import json
import os
from typing import List, Optional
import pandas as pd

from app.models.gasto import Gasto


class GestorFinanciero:
    """
    Gestiona una lista de movimientos financieros.
    Se encarga de guardar/cargar datos y generar estadísticas.
    """

    def __init__(self, archivo_datos: str = "datos/movimientos.json"):
        """
        Inicializa el gestor cargando movimientos desde el archivo JSON.

        Args:
            archivo_datos: Ruta al archivo JSON donde se persisten los datos.
        """
        self._archivo = archivo_datos
        self._movimientos: List[Gasto] = []
        self._cargar_datos()

    # ─── Operaciones CRUD ────────────────────────────────────────────────────

    def agregar_movimiento(self, gasto: Gasto) -> None:
        """Agrega un nuevo movimiento a la lista y guarda los datos."""
        self._movimientos.append(gasto)
        self._guardar_datos()

    def eliminar_movimiento(self, indice: int) -> Optional[Gasto]:
        """
        Elimina un movimiento por índice.

        Args:
            indice: Posición del movimiento en la lista (0-based).

        Returns:
            El Gasto eliminado, o None si el índice es inválido.
        """
        if 0 <= indice < len(self._movimientos):
            eliminado = self._movimientos.pop(indice)
            self._guardar_datos()
            return eliminado
        return None

    def obtener_movimientos(self) -> List[Gasto]:
        """Retorna todos los movimientos registrados."""
        return list(self._movimientos)

    # ─── Filtros ─────────────────────────────────────────────────────────────

    def filtrar_por_categoria(self, categoria: str) -> List[Gasto]:
        """Retorna los movimientos que pertenecen a la categoría indicada."""
        return [m for m in self._movimientos if m.categoria == categoria]

    def filtrar_por_tipo(self, solo_ingresos: bool) -> List[Gasto]:
        """
        Filtra movimientos por tipo.

        Args:
            solo_ingresos: True para ingresos, False para gastos.
        """
        if solo_ingresos:
            return [m for m in self._movimientos if m.es_ingreso()]
        return [m for m in self._movimientos if m.es_gasto()]

    # ─── Estadísticas ────────────────────────────────────────────────────────

    def total_ingresos(self) -> float:
        """Suma todos los ingresos registrados."""
        return round(sum(m.monto for m in self._movimientos if m.es_ingreso()), 2)

    def total_gastos(self) -> float:
        """Suma el valor absoluto de todos los gastos registrados."""
        return round(sum(abs(m.monto) for m in self._movimientos if m.es_gasto()), 2)

    def balance(self) -> float:
        """Calcula el balance actual (ingresos - gastos)."""
        return round(sum(m.monto for m in self._movimientos), 2)

    def resumen_por_categoria(self) -> dict:
        """
        Genera un resumen de gastos agrupados por categoría.

        Returns:
            Diccionario {categoria: total_gastado}.
        """
        resumen = {}
        for m in self._movimientos:
            if m.es_gasto():
                cat = m.categoria
                resumen[cat] = resumen.get(cat, 0) + abs(m.monto)
        # Redondear valores
        return {k: round(v, 2) for k, v in resumen.items()}

    def exportar_a_csv(self, ruta: str = "datos/reporte.csv") -> str:
        """
        Exporta todos los movimientos a un archivo CSV usando pandas.

        Args:
            ruta: Ruta del archivo CSV de salida.

        Returns:
            Ruta del archivo generado.
        """
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        datos = [m.to_dict() for m in self._movimientos]
        df = pd.DataFrame(datos)
        df.to_csv(ruta, index=False, encoding="utf-8-sig")
        return ruta

    def obtener_dataframe(self) -> pd.DataFrame:
        """Retorna los movimientos como un DataFrame de pandas."""
        datos = [m.to_dict() for m in self._movimientos]
        return pd.DataFrame(datos) if datos else pd.DataFrame(
            columns=["descripcion", "monto", "categoria", "fecha"]
        )

    # ─── Persistencia ────────────────────────────────────────────────────────

    def _guardar_datos(self) -> None:
        """Guarda los movimientos en el archivo JSON."""
        os.makedirs(os.path.dirname(self._archivo), exist_ok=True)
        with open(self._archivo, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self._movimientos], f, ensure_ascii=False, indent=2)

    def _cargar_datos(self) -> None:
        """Carga los movimientos desde el archivo JSON si existe."""
        if os.path.exists(self._archivo):
            with open(self._archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self._movimientos = [Gasto.from_dict(d) for d in datos]
