"""
Módulo de Vista (MVC).
Responsable de mostrar información al usuario y recoger sus entradas.
No contiene lógica de negocio.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

console = Console()


class MenuView:
    """
    Vista principal del gestor de gastos.
    Usa la librería 'rich' para mostrar texto con colores y tablas.
    """

    # ─── Menú principal ──────────────────────────────────────────────────────

    @staticmethod
    def mostrar_bienvenida() -> None:
        """Muestra el banner de bienvenida."""
        console.print(Panel.fit(
            "[bold cyan]💰 Gestor de Gastos Personales[/bold cyan]\n"
            "[dim]Aplicación POO con MVC en Python[/dim]",
            border_style="cyan"
        ))

    @staticmethod
    def mostrar_menu_principal() -> None:
        """Muestra las opciones del menú principal."""
        console.print("\n[bold yellow]── Menú Principal ──[/bold yellow]")
        console.print("  [cyan]1.[/cyan] Registrar movimiento (ingreso o gasto)")
        console.print("  [cyan]2.[/cyan] Ver todos los movimientos")
        console.print("  [cyan]3.[/cyan] Filtrar por categoría")
        console.print("  [cyan]4.[/cyan] Ver estadísticas y balance")
        console.print("  [cyan]5.[/cyan] Mostrar gráficos")
        console.print("  [cyan]6.[/cyan] Exportar reporte CSV")
        console.print("  [cyan]7.[/cyan] Eliminar movimiento")
        console.print("  [red]0.[/red] Salir")

    @staticmethod
    def pedir_opcion(opciones_validas: list) -> str:
        """
        Solicita una opción al usuario y valida que sea correcta.

        Args:
            opciones_validas: Lista de strings con las opciones permitidas.

        Returns:
            La opción elegida como string.
        """
        while True:
            opcion = console.input("\n[bold]Elige una opción: [/bold]").strip()
            if opcion in opciones_validas:
                return opcion
            console.print("[red]Opción inválida. Intenta de nuevo.[/red]")

    # ─── Formulario de movimiento ────────────────────────────────────────────

    @staticmethod
    def pedir_descripcion() -> str:
        """Solicita la descripción del movimiento."""
        return console.input("[bold]Descripción: [/bold]").strip()

    @staticmethod
    def pedir_monto(es_gasto: bool) -> float:
        """
        Solicita el monto y lo convierte al signo correcto.

        Args:
            es_gasto: Si True, el monto se guarda como negativo.

        Returns:
            Monto como float (negativo si es gasto).
        """
        while True:
            try:
                valor = float(console.input("[bold]Monto (sin signo): [/bold]").strip())
                if valor <= 0:
                    raise ValueError
                return -abs(valor) if es_gasto else abs(valor)
            except ValueError:
                console.print("[red]Ingresa un número mayor que cero.[/red]")

    @staticmethod
    def pedir_tipo() -> bool:
        """
        Pregunta si el movimiento es ingreso o gasto.

        Returns:
            True si es gasto, False si es ingreso.
        """
        console.print("\n  [cyan]1.[/cyan] Gasto")
        console.print("  [cyan]2.[/cyan] Ingreso")
        opcion = MenuView.pedir_opcion(["1", "2"])
        return opcion == "1"

    @staticmethod
    def pedir_categoria(categorias: list) -> str:
        """
        Muestra las categorías disponibles y pide elegir una.

        Args:
            categorias: Lista de categorías válidas.

        Returns:
            Categoría seleccionada.
        """
        console.print("\n[bold]Categorías:[/bold]")
        for i, cat in enumerate(categorias, 1):
            console.print(f"  [cyan]{i}.[/cyan] {cat}")
        while True:
            try:
                idx = int(console.input("[bold]Número de categoría: [/bold]").strip()) - 1
                if 0 <= idx < len(categorias):
                    return categorias[idx]
                raise ValueError
            except ValueError:
                console.print("[red]Número inválido.[/red]")

    # ─── Mostrar datos ───────────────────────────────────────────────────────

    @staticmethod
    def mostrar_movimientos(movimientos: list) -> None:
        """
        Muestra todos los movimientos en una tabla con rich.

        Args:
            movimientos: Lista de objetos Gasto.
        """
        if not movimientos:
            console.print("[yellow]No hay movimientos registrados.[/yellow]")
            return

        tabla = Table(title="Movimientos", box=box.ROUNDED, show_lines=True)
        tabla.add_column("#", style="dim", width=4)
        tabla.add_column("Fecha", style="cyan")
        tabla.add_column("Tipo", width=8)
        tabla.add_column("Categoría", style="magenta")
        tabla.add_column("Descripción")
        tabla.add_column("Monto", justify="right")

        for i, m in enumerate(movimientos):
            tipo = "[green]Ingreso[/green]" if m.es_ingreso() else "[red]Gasto[/red]"
            monto_str = f"[green]+${m.monto:,.2f}[/green]" if m.es_ingreso() else f"[red]-${abs(m.monto):,.2f}[/red]"
            tabla.add_row(str(i), m.fecha, tipo, m.categoria, m.descripcion, monto_str)

        console.print(tabla)

    @staticmethod
    def mostrar_estadisticas(ingresos: float, gastos: float, balance: float, resumen: dict) -> None:
        """
        Muestra un resumen estadístico del estado financiero.

        Args:
            ingresos: Total de ingresos.
            gastos: Total de gastos.
            balance: Balance actual.
            resumen: Diccionario {categoria: total}.
        """
        color_balance = "green" if balance >= 0 else "red"

        console.print(Panel(
            f"[green]Ingresos totales:[/green]  ${ingresos:>12,.2f}\n"
            f"[red]Gastos totales:[/red]    ${gastos:>12,.2f}\n"
            f"[{color_balance}]Balance actual:[/{color_balance}]    ${balance:>12,.2f}",
            title="📊 Estadísticas",
            border_style="blue"
        ))

        if resumen:
            tabla = Table(title="Gastos por Categoría", box=box.SIMPLE)
            tabla.add_column("Categoría", style="magenta")
            tabla.add_column("Total", justify="right", style="red")
            for cat, total in sorted(resumen.items(), key=lambda x: x[1], reverse=True):
                tabla.add_row(cat, f"${total:,.2f}")
            console.print(tabla)

    @staticmethod
    def mostrar_mensaje(texto: str, tipo: str = "info") -> None:
        """
        Muestra un mensaje con color según el tipo.

        Args:
            texto: Mensaje a mostrar.
            tipo: 'info', 'ok', 'error'.
        """
        colores = {"info": "cyan", "ok": "green", "error": "red"}
        color = colores.get(tipo, "white")
        console.print(f"[{color}]{texto}[/{color}]")

    @staticmethod
    def pedir_indice(mensaje: str) -> int:
        """Solicita un número entero al usuario."""
        while True:
            try:
                return int(console.input(f"[bold]{mensaje}[/bold]").strip())
            except ValueError:
                console.print("[red]Ingresa un número válido.[/red]")

    @staticmethod
    def mostrar_categorias_disponibles(categorias: list) -> str:
        """Pide al usuario elegir una categoría para filtrar."""
        console.print("\n[bold]Filtrar por categoría:[/bold]")
        for i, cat in enumerate(categorias, 1):
            console.print(f"  [cyan]{i}.[/cyan] {cat}")
        while True:
            try:
                idx = int(console.input("[bold]Número de categoría: [/bold]").strip()) - 1
                if 0 <= idx < len(categorias):
                    return categorias[idx]
                raise ValueError
            except ValueError:
                console.print("[red]Número inválido.[/red]")
