"""
Pruebas con pytest para el gestor de gastos personales.
Incluye pruebas válidas e inválidas según lo requerido por el trabajo.
"""

import pytest
import os
import json
from app.models.gasto import Gasto
from app.models.gestor_financiero import GestorFinanciero


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def gestor_temporal(tmp_path):
    """Crea un GestorFinanciero con un archivo JSON temporal para las pruebas."""
    archivo = str(tmp_path / "test_movimientos.json")
    return GestorFinanciero(archivo_datos=archivo)


# ─── Pruebas válidas ──────────────────────────────────────────────────────────

def test_crear_gasto_valido():
    """Prueba 1 (válida): Se puede crear un gasto con datos correctos."""
    gasto = Gasto("Almuerzo", -15000, "Alimentación", "2024-06-01")
    assert gasto.descripcion == "Almuerzo"
    assert gasto.monto == -15000
    assert gasto.categoria == "Alimentación"
    assert gasto.es_gasto() is True
    assert gasto.es_ingreso() is False


def test_crear_ingreso_valido():
    """Prueba 2 (válida): Se puede registrar un ingreso correctamente."""
    ingreso = Gasto("Salario", 3000000, "Ingreso", "2024-06-01")
    assert ingreso.monto == 3000000
    assert ingreso.es_ingreso() is True
    assert ingreso.es_gasto() is False


def test_balance_correcto(gestor_temporal):
    """Prueba 3 (válida): El balance refleja ingresos menos gastos."""
    gestor_temporal.agregar_movimiento(Gasto("Salario", 2000000, "Ingreso"))
    gestor_temporal.agregar_movimiento(Gasto("Arriendo", -800000, "Servicios"))
    gestor_temporal.agregar_movimiento(Gasto("Comida", -150000, "Alimentación"))

    assert gestor_temporal.total_ingresos() == 2000000
    assert gestor_temporal.total_gastos() == 950000
    assert gestor_temporal.balance() == 1050000


def test_persistencia_json(gestor_temporal):
    """Prueba 4 (válida): Los movimientos se guardan y cargan correctamente del JSON."""
    gestor_temporal.agregar_movimiento(Gasto("Bus", -3500, "Transporte"))

    # Crear un nuevo gestor con el mismo archivo; debe cargar el movimiento guardado
    gestor2 = GestorFinanciero(archivo_datos=gestor_temporal._archivo)
    movimientos = gestor2.obtener_movimientos()

    assert len(movimientos) == 1
    assert movimientos[0].descripcion == "Bus"


def test_filtrar_por_categoria(gestor_temporal):
    """Prueba 5 (válida): El filtro por categoría retorna solo los movimientos correctos."""
    gestor_temporal.agregar_movimiento(Gasto("Taxi", -10000, "Transporte"))
    gestor_temporal.agregar_movimiento(Gasto("Pizza", -25000, "Alimentación"))
    gestor_temporal.agregar_movimiento(Gasto("Metro", -3500, "Transporte"))

    transporte = gestor_temporal.filtrar_por_categoria("Transporte")
    assert len(transporte) == 2
    assert all(m.categoria == "Transporte" for m in transporte)


def test_eliminar_movimiento(gestor_temporal):
    """Prueba 6 (válida): Eliminar un movimiento lo quita de la lista."""
    gestor_temporal.agregar_movimiento(Gasto("Cine", -20000, "Entretenimiento"))
    gestor_temporal.agregar_movimiento(Gasto("Libro", -35000, "Educación"))

    eliminado = gestor_temporal.eliminar_movimiento(0)
    assert eliminado.descripcion == "Cine"
    assert len(gestor_temporal.obtener_movimientos()) == 1


def test_exportar_csv(gestor_temporal, tmp_path):
    """Prueba 7 (válida): La exportación CSV genera el archivo correctamente."""
    gestor_temporal.agregar_movimiento(Gasto("Mercado", -120000, "Alimentación"))
    ruta_csv = str(tmp_path / "reporte.csv")
    resultado = gestor_temporal.exportar_a_csv(ruta_csv)
    assert os.path.exists(resultado)


# ─── Pruebas inválidas (casos de error) ──────────────────────────────────────

def test_gasto_descripcion_vacia():
    """Prueba inválida 1: Crear un gasto con descripción vacía debe lanzar ValueError."""
    with pytest.raises(ValueError, match="descripción"):
        Gasto("", -5000, "Alimentación")


def test_gasto_monto_cero():
    """Prueba inválida 2: Crear un gasto con monto 0 debe lanzar ValueError."""
    with pytest.raises(ValueError, match="cero"):
        Gasto("Algo", 0, "Otros")


def test_categoria_invalida():
    """Prueba inválida 3: Crear un gasto con categoría inexistente debe lanzar ValueError."""
    with pytest.raises(ValueError, match="Categoría inválida"):
        Gasto("Videojuego", -80000, "Juegos")


def test_eliminar_indice_invalido(gestor_temporal):
    """Prueba inválida 4: Eliminar con índice fuera de rango retorna None."""
    gestor_temporal.agregar_movimiento(Gasto("Café", -5000, "Alimentación"))
    resultado = gestor_temporal.eliminar_movimiento(99)
    assert resultado is None
