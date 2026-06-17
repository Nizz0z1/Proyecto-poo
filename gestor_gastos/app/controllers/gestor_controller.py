"""
Módulo del Controlador (MVC).
Conecta la Vista con el Modelo: recibe acciones del usuario,
llama al modelo y envía los resultados a la vista.
"""

import matplotlib.pyplot as plt
import matplotlib
import os

from app.models.gasto import Gasto
from app.models.gestor_financiero import GestorFinanciero
from app.views.menu_view import MenuView

# Usar backend sin interfaz gráfica para evitar errores en entornos sin pantalla
matplotlib.use("Agg")


class GestorController:
    """
    Controlador principal del gestor de gastos.
    Orquesta el flujo entre la Vista y el Modelo.
    """

    def __init__(self):
        """Inicializa el controlador creando el modelo y la vista."""
        self._modelo = GestorFinanciero()
        self._vista = MenuView()

    def ejecutar(self) -> None:
        """Inicia el ciclo principal de la aplicación."""
        self._vista.mostrar_bienvenida()

        opciones = {"0", "1", "2", "3", "4", "5", "6", "7"}
        acciones = {
            "1": self._registrar_movimiento,
            "2": self._ver_movimientos,
            "3": self._filtrar_por_categoria,
            "4": self._ver_estadisticas,
            "5": self._mostrar_graficos,
            "6": self._exportar_csv,
            "7": self._eliminar_movimiento,
        }

        while True:
            self._vista.mostrar_menu_principal()
            opcion = self._vista.pedir_opcion(opciones)

            if opcion == "0":
                self._vista.mostrar_mensaje("👋 ¡Hasta luego!", "info")
                break

            accion = acciones.get(opcion)
            if accion:
                accion()

    # ─── Acciones ────────────────────────────────────────────────────────────

    def _registrar_movimiento(self) -> None:
        """Flujo para registrar un nuevo ingreso o gasto."""
        self._vista.mostrar_mensaje("\n── Registrar movimiento ──", "info")

        es_gasto = self._vista.pedir_tipo()
        descripcion = self._vista.pedir_descripcion()
        monto = self._vista.pedir_monto(es_gasto)

        # Mostrar categorías según tipo
        categorias = [c for c in Gasto.CATEGORIAS_VALIDAS if c != "Ingreso"] if es_gasto \
            else ["Ingreso"]
        categoria = self._vista.pedir_categoria(categorias) if len(categorias) > 1 \
            else categorias[0]

        try:
            nuevo = Gasto(descripcion, monto, categoria)
            self._modelo.agregar_movimiento(nuevo)
            self._vista.mostrar_mensaje("✅ Movimiento registrado correctamente.", "ok")
        except ValueError as e:
            self._vista.mostrar_mensaje(f"❌ Error: {e}", "error")

    def _ver_movimientos(self) -> None:
        """Muestra la lista completa de movimientos."""
        movimientos = self._modelo.obtener_movimientos()
        self._vista.mostrar_movimientos(movimientos)

    def _filtrar_por_categoria(self) -> None:
        """Filtra y muestra movimientos de una categoría específica."""
        categoria = self._vista.mostrar_categorias_disponibles(Gasto.CATEGORIAS_VALIDAS)
        filtrados = self._modelo.filtrar_por_categoria(categoria)
        self._vista.mostrar_mensaje(f"\n── Movimientos en '{categoria}' ──", "info")
        self._vista.mostrar_movimientos(filtrados)

    def _ver_estadisticas(self) -> None:
        """Muestra el resumen estadístico financiero."""
        self._vista.mostrar_estadisticas(
            ingresos=self._modelo.total_ingresos(),
            gastos=self._modelo.total_gastos(),
            balance=self._modelo.balance(),
            resumen=self._modelo.resumen_por_categoria(),
        )

    def _mostrar_graficos(self) -> None:
        """
        Genera y guarda gráficos de gastos usando matplotlib.
        Guarda los archivos en docs/capturas/.
        """
        resumen = self._modelo.resumen_por_categoria()

        if not resumen:
            self._vista.mostrar_mensaje("No hay gastos para graficar.", "info")
            return

        os.makedirs("docs/capturas", exist_ok=True)

        # Gráfico de pastel por categoría
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle("Resumen Financiero", fontsize=14, fontweight="bold")

        categorias = list(resumen.keys())
        valores = list(resumen.values())

        # Pastel
        axes[0].pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90)
        axes[0].set_title("Distribución de Gastos")

        # Barras
        axes[1].bar(categorias, valores, color="salmon", edgecolor="black")
        axes[1].set_title("Gastos por Categoría")
        axes[1].set_ylabel("Monto ($)")
        axes[1].tick_params(axis="x", rotation=30)

        plt.tight_layout()
        ruta = "docs/capturas/grafico_gastos.png"
        plt.savefig(ruta, dpi=120)
        plt.close()

        self._vista.mostrar_mensaje(f"✅ Gráfico guardado en '{ruta}'.", "ok")

    def _exportar_csv(self) -> None:
        """Exporta los movimientos a un archivo CSV."""
        ruta = self._modelo.exportar_a_csv()
        self._vista.mostrar_mensaje(f"✅ Reporte exportado a '{ruta}'.", "ok")

    def _eliminar_movimiento(self) -> None:
        """Muestra los movimientos y elimina el indicado por el usuario."""
        movimientos = self._modelo.obtener_movimientos()
        self._vista.mostrar_movimientos(movimientos)

        if not movimientos:
            return

        indice = self._vista.pedir_indice("Número del movimiento a eliminar: ")
        eliminado = self._modelo.eliminar_movimiento(indice)

        if eliminado:
            self._vista.mostrar_mensaje(f"✅ Eliminado: {eliminado}", "ok")
        else:
            self._vista.mostrar_mensaje("❌ Índice inválido.", "error")
