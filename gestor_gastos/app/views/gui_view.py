"""
Vista gráfica (MVC) usando tkinter.
Reemplaza la vista de consola manteniendo la misma arquitectura.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, List
from app.models.gasto import Gasto


class GUIView(tk.Tk):
    """
    Ventana principal de la aplicación.
    Muestra tabs para: movimientos, estadísticas y gráficos.
    No contiene lógica de negocio.
    """

    # ── Paleta de colores ────────────────────────────────────────────────────
    BG       = "#F5F6FA"
    SIDEBAR  = "#2C3E50"
    ACCENT   = "#27AE60"
    DANGER   = "#E74C3C"
    TEXT_W   = "#FFFFFF"
    TEXT_D   = "#2C3E50"
    CARD     = "#FFFFFF"
    INCOME   = "#27AE60"
    EXPENSE  = "#E74C3C"
    BORDER   = "#DFE3E8"

    def __init__(self):
        super().__init__()
        self.title("💰 Gestor de Gastos Personales")
        self.geometry("900x620")
        self.minsize(800, 560)
        self.configure(bg=self.BG)
        self.resizable(True, True)

        # Callbacks que el controlador inyecta
        self.on_agregar:   Callable = None
        self.on_eliminar:  Callable = None
        self.on_exportar:  Callable = None
        self.on_grafico:   Callable = None

        self._build_ui()

    # ── Construcción de la UI ────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        contenedor = tk.Frame(self, bg=self.BG)
        contenedor.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        self._build_form(contenedor)
        self._build_table(contenedor)
        self._build_stats(contenedor)
        self._build_footer()

    def _build_header(self):
        header = tk.Frame(self, bg=self.SIDEBAR, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="💰  Gestor de Gastos Personales",
            bg=self.SIDEBAR, fg=self.TEXT_W,
            font=("Helvetica", 16, "bold")
        ).pack(side="left", padx=20, pady=12)

    def _build_form(self, parent):
        """Panel izquierdo: formulario de registro."""
        frame = tk.LabelFrame(
            parent, text=" ➕ Nuevo movimiento ",
            bg=self.CARD, fg=self.TEXT_D,
            font=("Helvetica", 10, "bold"),
            relief="flat", bd=1,
            highlightbackground=self.BORDER, highlightthickness=1
        )
        frame.pack(side="left", fill="y", padx=(0, 12), pady=8, ipadx=10, ipady=8)

        # Tipo
        tk.Label(frame, text="Tipo", bg=self.CARD, fg=self.TEXT_D,
                 font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", padx=8, pady=(10,2))
        self.tipo_var = tk.StringVar(value="Gasto")
        tipo_frame = tk.Frame(frame, bg=self.CARD)
        tipo_frame.grid(row=1, column=0, sticky="w", padx=8)
        for val, color in [("Gasto", self.EXPENSE), ("Ingreso", self.INCOME)]:
            tk.Radiobutton(
                tipo_frame, text=val, variable=self.tipo_var, value=val,
                bg=self.CARD, fg=color, selectcolor=self.CARD,
                activebackground=self.CARD, font=("Helvetica", 10, "bold"),
                command=self._on_tipo_change
            ).pack(side="left", padx=4)

        # Descripción
        tk.Label(frame, text="Descripción", bg=self.CARD, fg=self.TEXT_D,
                 font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w", padx=8, pady=(10,2))
        self.desc_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.desc_var, width=24,
                 font=("Helvetica", 10), relief="solid", bd=1
                 ).grid(row=3, column=0, padx=8, sticky="ew")

        # Monto
        tk.Label(frame, text="Monto ($)", bg=self.CARD, fg=self.TEXT_D,
                 font=("Helvetica", 9, "bold")).grid(row=4, column=0, sticky="w", padx=8, pady=(10,2))
        self.monto_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.monto_var, width=24,
                 font=("Helvetica", 10), relief="solid", bd=1
                 ).grid(row=5, column=0, padx=8, sticky="ew")

        # Categoría
        tk.Label(frame, text="Categoría", bg=self.CARD, fg=self.TEXT_D,
                 font=("Helvetica", 9, "bold")).grid(row=6, column=0, sticky="w", padx=8, pady=(10,2))
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(
            frame, textvariable=self.cat_var, width=22,
            font=("Helvetica", 10), state="readonly"
        )
        self.cat_combo.grid(row=7, column=0, padx=8, sticky="ew")
        self._on_tipo_change()  # Carga categorías iniciales

        # Botón agregar
        tk.Button(
            frame, text="  Registrar  ", command=self._click_agregar,
            bg=self.ACCENT, fg=self.TEXT_W, relief="flat",
            font=("Helvetica", 10, "bold"), cursor="hand2",
            activebackground="#219A52", activeforeground=self.TEXT_W, pady=6
        ).grid(row=8, column=0, padx=8, pady=16, sticky="ew")

        # Botones secundarios
        tk.Button(
            frame, text="📊 Ver gráfico", command=lambda: self.on_grafico and self.on_grafico(),
            bg=self.SIDEBAR, fg=self.TEXT_W, relief="flat",
            font=("Helvetica", 9), cursor="hand2", pady=4
        ).grid(row=9, column=0, padx=8, pady=2, sticky="ew")

        tk.Button(
            frame, text="📥 Exportar CSV", command=lambda: self.on_exportar and self.on_exportar(),
            bg="#7F8C8D", fg=self.TEXT_W, relief="flat",
            font=("Helvetica", 9), cursor="hand2", pady=4
        ).grid(row=10, column=0, padx=8, pady=2, sticky="ew")

    def _build_table(self, parent):
        """Panel central: tabla de movimientos."""
        frame = tk.LabelFrame(
            parent, text=" 📋 Movimientos ",
            bg=self.CARD, fg=self.TEXT_D,
            font=("Helvetica", 10, "bold"),
            relief="flat", bd=1,
            highlightbackground=self.BORDER, highlightthickness=1
        )
        frame.pack(side="left", fill="both", expand=True, pady=8)

        # Toolbar de tabla
        toolbar = tk.Frame(frame, bg=self.CARD)
        toolbar.pack(fill="x", padx=8, pady=(6, 0))

        tk.Label(toolbar, text="Filtrar:", bg=self.CARD,
                 font=("Helvetica", 9)).pack(side="left")
        self.filtro_var = tk.StringVar(value="Todos")
        filtro_vals = ["Todos", "Solo ingresos", "Solo gastos"] + Gasto.CATEGORIAS_VALIDAS
        ttk.Combobox(
            toolbar, textvariable=self.filtro_var,
            values=filtro_vals, width=18, state="readonly",
            font=("Helvetica", 9)
        ).pack(side="left", padx=6)
        self.filtro_var.trace_add("write", lambda *_: self._aplicar_filtro())

        tk.Button(
            toolbar, text="🗑 Eliminar seleccionado",
            command=self._click_eliminar,
            bg=self.DANGER, fg=self.TEXT_W, relief="flat",
            font=("Helvetica", 9), cursor="hand2", pady=2
        ).pack(side="right", padx=4)

        # Treeview
        cols = ("Fecha", "Tipo", "Categoría", "Descripción", "Monto")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=18)

        anchos = {"Fecha": 90, "Tipo": 70, "Categoría": 110, "Descripción": 200, "Monto": 110}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=anchos[col],
                             anchor="e" if col == "Monto" else "w")

        # Tags de color
        self.tree.tag_configure("ingreso", foreground=self.INCOME)
        self.tree.tag_configure("gasto",   foreground=self.EXPENSE)

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)
        sb.pack(side="left", fill="y", pady=8, padx=(0,4))

        # Estilo treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=26, font=("Helvetica", 9))
        style.configure("Treeview.Heading", font=("Helvetica", 9, "bold"))

        # Cache de todos los movimientos para filtrar localmente
        self._todos_los_items: list = []

    def _build_stats(self, parent):
        """Panel derecho: tarjetas de estadísticas."""
        frame = tk.LabelFrame(
            parent, text=" 📊 Resumen ",
            bg=self.CARD, fg=self.TEXT_D,
            font=("Helvetica", 10, "bold"),
            relief="flat", bd=1,
            highlightbackground=self.BORDER, highlightthickness=1
        )
        frame.pack(side="left", fill="y", padx=(12, 0), pady=8, ipadx=8, ipady=8)

        def tarjeta(parent, titulo, var, color):
            f = tk.Frame(parent, bg=color, padx=12, pady=8)
            f.pack(fill="x", padx=6, pady=5)
            tk.Label(f, text=titulo, bg=color, fg=self.TEXT_W,
                     font=("Helvetica", 8)).pack(anchor="w")
            tk.Label(f, textvariable=var, bg=color, fg=self.TEXT_W,
                     font=("Helvetica", 13, "bold")).pack(anchor="w")

        self.v_ingresos = tk.StringVar(value="$0")
        self.v_gastos   = tk.StringVar(value="$0")
        self.v_balance  = tk.StringVar(value="$0")

        tarjeta(frame, "💚 Ingresos totales", self.v_ingresos, "#27AE60")
        tarjeta(frame, "❤️  Gastos totales",   self.v_gastos,   "#E74C3C")
        tarjeta(frame, "💙 Balance actual",    self.v_balance,  "#2980B9")

        # Mini-tabla categorías
        tk.Label(frame, text="Por categoría", bg=self.CARD, fg=self.TEXT_D,
                 font=("Helvetica", 9, "bold")).pack(anchor="w", padx=6, pady=(14,2))

        self.cat_tree = ttk.Treeview(frame, columns=("cat","total"), show="headings", height=8)
        self.cat_tree.heading("cat",   text="Categoría")
        self.cat_tree.heading("total", text="Total")
        self.cat_tree.column("cat",   width=100)
        self.cat_tree.column("total", width=80, anchor="e")
        self.cat_tree.pack(fill="x", padx=6)

    def _build_footer(self):
        footer = tk.Frame(self, bg=self.SIDEBAR, height=28)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer, text="Gestor de Gastos Personales · POO con MVC · Python",
            bg=self.SIDEBAR, fg="#BDC3C7", font=("Helvetica", 8)
        ).pack(side="left", padx=12, pady=4)

    # ── Helpers internos ─────────────────────────────────────────────────────

    def _on_tipo_change(self):
        """Actualiza las categorías del combobox según el tipo seleccionado."""
        cats = [c for c in Gasto.CATEGORIAS_VALIDAS if c != "Ingreso"] \
               if self.tipo_var.get() == "Gasto" else ["Ingreso"]
        self.cat_combo["values"] = cats
        self.cat_var.set(cats[0])

    def _click_agregar(self):
        if self.on_agregar:
            self.on_agregar(
                tipo=self.tipo_var.get(),
                descripcion=self.desc_var.get(),
                monto_str=self.monto_var.get(),
                categoria=self.cat_var.get(),
            )

    def _click_eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Sin selección", "Selecciona un movimiento de la tabla.")
            return
        item = seleccion[0]
        indice = self.tree.index(item)
        # Calcular índice real según filtro aplicado
        indice_real = self._indice_real(indice)
        if self.on_eliminar and indice_real is not None:
            self.on_eliminar(indice_real)

    def _indice_real(self, indice_visible: int):
        """Devuelve el índice real en la lista completa del ítem visible nº indice_visible."""
        items_visibles = self.tree.get_children()
        if indice_visible >= len(items_visibles):
            return None
        iid = items_visibles[indice_visible]
        # El iid almacena el índice real como texto
        return int(self.tree.item(iid, "values")[5])  # columna oculta

    def _aplicar_filtro(self):
        """Filtra los items visibles en la tabla sin releer el modelo."""
        filtro = self.filtro_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in self._todos_los_items:
            tipo = row[1]   # "Ingreso" o "Gasto"
            cat  = row[2]
            if filtro == "Todos":
                mostrar = True
            elif filtro == "Solo ingresos":
                mostrar = tipo == "Ingreso"
            elif filtro == "Solo gastos":
                mostrar = tipo == "Gasto"
            else:
                mostrar = cat == filtro

            if mostrar:
                tag = "ingreso" if tipo == "Ingreso" else "gasto"
                # Mostramos solo las 5 primeras columnas; la 6ª (índice real) está oculta
                self.tree.insert("", "end", iid=row[5], values=row[:5], tags=(tag,))

    # ── API pública (llamada por el controlador) ──────────────────────────────

    def actualizar_tabla(self, movimientos: list):
        """
        Recibe la lista de Gasto y actualiza la tabla y el filtro.
        Columna oculta [5] = índice real en la lista del modelo.
        """
        self._todos_los_items = []
        for i, m in enumerate(movimientos):
            tipo   = "Ingreso" if m.es_ingreso() else "Gasto"
            monto  = f"+${m.monto:,.2f}" if m.es_ingreso() else f"-${abs(m.monto):,.2f}"
            self._todos_los_items.append(
                (m.fecha, tipo, m.categoria, m.descripcion, monto, str(i))
            )
        self._aplicar_filtro()

    def actualizar_estadisticas(self, ingresos: float, gastos: float,
                                balance: float, resumen: dict):
        """Actualiza las tarjetas de estadísticas y la mini-tabla."""
        self.v_ingresos.set(f"${ingresos:,.2f}")
        self.v_gastos.set(f"${gastos:,.2f}")
        color_balance = "#2980B9" if balance >= 0 else self.EXPENSE
        self.v_balance.set(f"${balance:,.2f}")

        for item in self.cat_tree.get_children():
            self.cat_tree.delete(item)
        for cat, total in sorted(resumen.items(), key=lambda x: x[1], reverse=True):
            self.cat_tree.insert("", "end", values=(cat, f"${total:,.2f}"))

    def limpiar_formulario(self):
        self.desc_var.set("")
        self.monto_var.set("")
        self._on_tipo_change()

    def mostrar_error(self, mensaje: str):
        messagebox.showerror("Error", mensaje)

    def mostrar_info(self, mensaje: str):
        messagebox.showinfo("Información", mensaje)

    def pedir_ruta_csv(self) -> str:
        return filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Guardar reporte CSV",
            initialfile="reporte_gastos.csv"
        )
