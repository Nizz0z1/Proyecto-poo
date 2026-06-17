# 💰 Gestor de Gastos Personales

## Descripción

Aplicación de consola desarrollada en Python que permite registrar, clasificar y analizar ingresos y gastos personales. Genera estadísticas, gráficos y reportes CSV para tener control total de las finanzas personales.

## Objetivo

Desarrollar un software funcional aplicando Programación Orientada a Objetos y el patrón de arquitectura MVC, usando librerías externas de Python para una experiencia de usuario enriquecida.

## Características principales

- Registrar ingresos y gastos con descripción, categoría y fecha
- Ver todos los movimientos en una tabla con colores (usando `rich`)
- Filtrar movimientos por categoría
- Ver estadísticas: total ingresos, gastos y balance actual
- Generar gráficos de distribución de gastos con `matplotlib`
- Exportar todos los movimientos a un archivo CSV con `pandas`
- Eliminar movimientos existentes
- Persistencia automática en archivo JSON

## Tecnologías utilizadas

- Python 3.10+
- `rich` — Interfaz de consola con colores, tablas y paneles
- `pandas` — Exportación a CSV y manejo de datos
- `matplotlib` — Generación de gráficos
- `pytest` — Pruebas automatizadas
- GitHub — Control de versiones

## Arquitectura del proyecto (MVC)

```
gestor_gastos/
│
├── app/
│   ├── models/
│   │   ├── gasto.py              ← Modelo: entidad Gasto con validaciones
│   │   └── gestor_financiero.py  ← Modelo: lógica de negocio y persistencia
│   │
│   ├── views/
│   │   └── menu_view.py          ← Vista: interfaz de consola con rich
│   │
│   ├── controllers/
│   │   └── gestor_controller.py  ← Controlador: conecta modelo y vista
│   │
│   └── main.py                   ← Punto de entrada
│
├── tests/
│   ├── conftest.py
│   └── test_gestor.py            ← Pruebas con pytest
│
├── docs/
│   ├── diagrama_clases.md        ← Diagrama de clases en Mermaid
│   ├── proceso_desarrollo.md
│   └── capturas/
│
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

- **Modelo:** `Gasto` representa un movimiento financiero. `GestorFinanciero` contiene la lógica de negocio, cálculos y persistencia.
- **Vista:** `MenuView` muestra menús, tablas y mensajes al usuario usando `rich`. No contiene lógica de negocio.
- **Controlador:** `GestorController` recibe la acción del usuario, llama al modelo y envía el resultado a la vista.

## Diagrama de clases

Ver archivo [`docs/diagrama_clases.md`](docs/diagrama_clases.md) con el diagrama completo en formato Mermaid.

## Instalación

```bash
git clone https://github.com/TU_USUARIO/gestor-gastos-personales.git
cd gestor-gastos-personales
pip install -r requirements.txt
```

## Ejecución

```bash
python -m app.main
```

> Ejecutar desde la carpeta raíz del proyecto.

## Pruebas

```bash
pytest
```

Para ver más detalles:

```bash
pytest -v
```

## Capturas de pantalla

*(Agrega aquí las capturas tomadas del programa funcionando)*

| Menú principal | Estadísticas | Gráfico |
|---|---|---|
| ![menu](docs/capturas/captura_menu.png) | ![stats](docs/capturas/captura_estadisticas.png) | ![grafico](docs/capturas/grafico_gastos.png) |

## Integrantes

- *(Nombre del estudiante 1)*
- *(Nombre del estudiante 2)*
- *(Nombre del estudiante 3)*

## Licencia

MIT License — libre uso educativo.
