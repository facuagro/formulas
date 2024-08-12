# Gestión de Fórmulas

## Descripción
Esta aplicación permite gestionar fórmulas para productos químicos. Los administradores pueden cargar fórmulas desde archivos Excel y los operadores pueden modificar la cantidad utilizada.

## Estructura de Directorios
- `2_4D/`, `FLOABLES/`, `HM/`, `LSE/`, `CLIENTES/`: Directorios que contienen fórmulas en formato Excel organizadas por categoría y cliente.

## Requisitos
- Python 3.x
- PyQt5
- pandas

## Instalación
1. Clonar el repositorio: `git clone <url-del-repositorio>`
2. Instalar las dependencias: `pip install -r requirements.txt`

## Uso
1. Ejecutar la aplicación: `python main.py`
2. Cargar fórmulas desde el botón "Cargar Fórmulas"
3. Modificar las cantidades utilizadas en la tabla y guardar los cambios con el botón "Guardar Cantidades"
