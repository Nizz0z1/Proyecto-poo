"""
Controlador para la interfaz gráfica (MVC).
Conecta GUIView con GestorFinanciero.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

from app.models.gasto import Gasto
from app.models.gestor_financiero import GestorFinanciero
from app.views.gui_view import GUIView


class GestorControllerGUI:
    """
    Controlador que usa la vista gráfica tkinter.
    Inyecta los callbacks en la vista y refresca los datos tras cada acción.
    """

    def __init__(self):
        self._modelo = GestorFinanciero()
        self._vista  = GUIView()

        # Inyectar callbacks
        self._vista.on_agregar  = self._agregar
        self._vista.on_eliminar = self._eliminar
        self._vista.on_exportar = self._exportar
        self._vista.on_grafico  = self._grafico

        self._refrescar()

    def ejecutar(self):
        """Inicia el loop principal de tkinter."""
        self._vista.mainloop()

    # ── Acciones ─────────────────────────────────────────────────────────────

    def _agregar(self, tipo: str, descripcion: str, monto_str: str, categoria: str):
        """Valida y registra un nuevo movimiento."""
        try:
            monto = float(monto_str.replace(",", "."))
            if monto <= 0:
                raise ValueError("El monto debe ser mayor que cero.")
            if tipo == "Gasto":
                monto = -monto

            nuevo = Gasto(descripcion, monto, categoria)
            self._modelo.agregar_movimiento(nuevo)
            self._vista.limpiar_formulario()
            self._refrescar()
        except ValueError as e:
            self._vista.mostrar_error(str(e))

    def _eliminar(self, indice: int):
        """Elimina el movimiento en la posición indicada."""
        eliminado = self._modelo.eliminar_movimiento(indice)
        if eliminado:
            self._refrescar()
        else:
            self._vista.mostrar_error("No se pudo eliminar el movimiento.")

    def _exportar(self):
        """Pide ruta y exporta CSV."""
        ruta = self._vista.pedir_ruta_csv()
        if ruta:
            self._modelo.exportar_a_csv(ruta)
            self._vista.mostrar_info(f"Reporte guardado en:\n{ruta}")

    def _grafico(self):
        """Genera gráfico y lo guarda, luego lo muestra en una ventana."""
        resumen = self._modelo.resumen_por_categoria()
        if not resumen:
            self._vista.mostrar_info("No hay gastos registrados para graficar.")
            return

        os.makedirs("docs/capturas", exist_ok=True)
        fig, axes = plt.subplots(1, 2, figsize=(11, 5))
        fig.suptitle("Distribución de Gastos", fontsize=14, fontweight="bold")

        categorias = list(resumen.keys())
        valores    = list(resumen.values())

        axes[0].pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90)
        axes[0].set_title("Por categoría")

        colores = plt.cm.Set2.colors[:len(categorias)]
        bars = axes[1].bar(categorias, valores, color=colores, edgecolor="white", linewidth=1.2)
        axes[1].set_title("Montos por categoría")
        axes[1].set_ylabel("Monto ($)")
        axes[1].tick_params(axis="x", rotation=30)
        for bar, val in zip(bars, valores):
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(valores)*0.01,
                         f"${val:,.0f}", ha="center", va="bottom", fontsize=8)

        plt.tight_layout()
        ruta = "docs/capturas/grafico_gastos.png"
        plt.savefig(ruta, dpi=120)
        plt.close()

        # Mostrar en ventana tkinter
        import tkinter as tk
        from PIL import Image, ImageTk
        try:
            ventana = tk.Toplevel(self._vista)
            ventana.title("Gráfico de gastos")
            img = Image.open(ruta)
            img = img.resize((820, 380), Image.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            lbl = tk.Label(ventana, image=foto)
            lbl.image = foto
            lbl.pack(padx=10, pady=10)
        except Exception:
            self._vista.mostrar_info(f"Gráfico guardado en:\n{ruta}")

    # ── Refresco de UI ───────────────────────────────────────────────────────

    def _refrescar(self):
        """Actualiza tabla y estadísticas con los datos actuales del modelo."""
        movimientos = self._modelo.obtener_movimientos()
        self._vista.actualizar_tabla(movimientos)
        self._vista.actualizar_estadisticas(
            ingresos=self._modelo.total_ingresos(),
            gastos=self._modelo.total_gastos(),
            balance=self._modelo.balance(),
            resumen=self._modelo.resumen_por_categoria(),
        )
