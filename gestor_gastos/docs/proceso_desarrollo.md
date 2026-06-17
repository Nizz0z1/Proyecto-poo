# Proceso de desarrollo

## 1. Idea inicial

Desarrollar una aplicación de consola para registrar y analizar ingresos y gastos personales, permitiendo al usuario llevar un control financiero básico con estadísticas y gráficos.

## 2. Análisis del problema

**Usuario objetivo:** Cualquier persona que quiera llevar un control simple de sus finanzas personales sin necesidad de una hoja de cálculo compleja.

**Necesidades identificadas:**
- Registrar movimientos (ingresos y gastos) con descripción, monto y categoría.
- Consultar el balance en cualquier momento.
- Filtrar movimientos por categoría.
- Ver gráficos visuales del gasto por categoría.
- Exportar datos a CSV para análisis externo.

## 3. Diseño de la solución

### Clases principales
- **`Gasto`**: Entidad que representa un movimiento financiero. Contiene las validaciones básicas.
- **`GestorFinanciero`**: Lógica de negocio: agregar, eliminar, filtrar y calcular estadísticas. Persiste en JSON.
- **`MenuView`**: Interfaz de usuario en consola usando `rich`.
- **`GestorController`**: Orquesta el flujo entre vista y modelo.

### Arquitectura MVC
- **Modelo:** `Gasto` y `GestorFinanciero` (datos y lógica)
- **Vista:** `MenuView` (interacción con el usuario)
- **Controlador:** `GestorController` (conecta modelo y vista)

## 4. Implementación

1. Se definió primero el modelo `Gasto` con sus validaciones.
2. Se construyó `GestorFinanciero` con la lógica de CRUD y persistencia JSON.
3. Se diseñó `MenuView` con `rich` para tablas y paneles con colores.
4. Se implementó `GestorController` uniendo todo.
5. Se escribieron las pruebas con pytest.
6. Se generó el README y documentación.

## 5. Pruebas

Se implementaron 11 pruebas con pytest:
- 7 pruebas válidas: creación de gastos/ingresos, balance, persistencia, filtros, eliminación y exportación CSV.
- 4 pruebas inválidas: descripción vacía, monto cero, categoría inválida, índice fuera de rango.

Todas las pruebas pasaron correctamente.

## 6. Dificultades encontradas

- Configurar `matplotlib` en modo sin interfaz gráfica (`Agg`) para evitar errores en terminales sin display.
- Gestionar los imports correctamente con la arquitectura MVC en carpetas separadas.
- Asegurar que los datos JSON se guarden con codificación UTF-8 para soportar tildes y caracteres especiales.

## 7. Mejoras futuras

- Agregar interfaz gráfica con `tkinter` o `customtkinter`.
- Soporte para múltiples usuarios con autenticación.
- Alertas cuando se supere un presupuesto mensual por categoría.
- Integración con APIs bancarias para importar movimientos automáticamente.
- Soporte para múltiples monedas con conversión automática.
