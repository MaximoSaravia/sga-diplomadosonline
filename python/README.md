# Sistema de Gestión Académica (SGA-DO)

## Descripción
Sistema de Gestión Académica desarrollado en Python para administrar alumnos, profesores, programas académicos, calificaciones y certificados.

## Funcionalidades
- Registro de alumnos y profesores.
- Asignación y registro de calificaciones.
- Evaluación de aprobación según el tipo de programa académico.
- Deshacer el último registro de nota mediante una pila (LIFO).
- Generación de certificados mediante una cola (FIFO).
- Reporte general de alumnos y profesores.
- Persistencia de datos mediante archivos de texto.

## Requisitos
- Python 3 instalado.

## Ejecución
Desde una terminal ubicada en la carpeta `python`, ejecutar:

```bash
python main.py
```

Si el comando anterior no funciona en Windows, también se puede utilizar:

```bash
py main.py
```

## Archivos del proyecto
- `main.py`: código fuente principal.
- `alumnos.txt`: información y calificaciones de alumnos.
- `profesores.txt`: información de profesores.
- `certificados_pendientes.txt`: reporte generado de certificados.
- `README.md`: documentación del proyecto.

## Uso
Al ejecutar el programa, se muestra un menú interactivo con opciones para registrar alumnos, registrar profesores, ingresar notas, deshacer el último registro, generar certificados, consultar el reporte general y salir.

## Persistencia
Los datos se guardan en archivos de texto para conservar la información entre ejecuciones del programa.
