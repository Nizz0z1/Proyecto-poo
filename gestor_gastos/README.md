#  Gestor de Gastos Personales

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

| evidencia |
|---|
|<img width="893" height="640" alt="{94DFA129-6B6D-4EE4-8DF3-314DD577EB3F}" src="https://github.com/user-attachments/assets/b21af30f-bd53-47c6-a5a5-aacdd0e76c0a" />|
|<img width="588" height="234" alt="{5F048F98-AB22-450F-B8C7-CB5926908A84}" src="https://github.com/user-attachments/assets/ee25ba78-1984-499a-8e55-8b0c5b91f012" />|
|<img width="831" height="428" alt="{A5E32C46-5F78-45E4-A0AA-C91AD3F33423}" src="https://github.com/user-attachments/assets/e9640cba-c6c2-46f2-85d6-df31f553f235" />|

## Integrantes

- *Nicolas Castillo*

## Licencia

MIT License — libre uso educativo.
