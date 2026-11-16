================================================================================
DOCUMENTACIÓN: GESTOR DE ARCHIVOS EN PYTHON

Hecho por: Nicolas David Zambrano Murcia, Daniel Alberto Zapata Castaño,  Miguel Ángel Quiceno hincapié, Cristhian Camilo Mesias Rodriguez, Carlos Augusto Villalobos Cubas.

================================================================================

1. DESCRIPCIÓN GENERAL
--------------------------------------------------------------------------------
Este programa es una aplicación de consola desarrollada en Python que permite
administrar archivos y directorios básicos mediante llamadas directas al 
sistema operativo (uso de descriptores de archivo, gestión de rutas y metadatos).

Al ejecutarse, el script crea automáticamente una carpeta de trabajo llamada 
"GESTOR_SO" (si no existe) y sitúa la ejecución dentro de ella para mantener
organizados todos los archivos generados.


2. LIBRERÍAS UTILIZADAS
--------------------------------------------------------------------------------
- os: Módulo principal para interactuar con el sistema operativo (crear carpetas,
  leer/escribir a bajo nivel mediante descriptores, renombrar, eliminar y
  obtener metadatos).
- shutil: Utilizada para realizar copias exactas de archivos conservando sus
  metadatos originales.
- datetime: Utilizada para convertir las marcas de tiempo (timestamps) del 
  sistema en fechas y horas legibles para el usuario.


3. DETALLE DE LAS 9 FUNCIONALIDADES
--------------------------------------------------------------------------------

[Opción 1] crear_directorio(nombre)
- Propósito: Crea una nueva carpeta con el nombre indicado.
- Funcionamiento: Verifica si ya existe una carpeta con ese nombre. Si existe,
  añade un contador numérico incremental (ej. "carpeta (1)", "carpeta (2)")
  hasta encontrar un nombre disponible y crea el directorio con os.makedirs().

[Opción 2] crear_archivo_txt(nombre)
- Propósito: Crea un archivo de texto plano vacío (.txt).
- Funcionamiento: Asegura que el nombre termine en ".txt". Si el nombre ya
  está en uso, agrega un contador incremental. Utiliza os.open() con las
  banderas O_CREAT, O_EXCL y O_WRONLY para crear el archivo a bajo nivel y 
  cierra inmediatamente su descriptor con os.close().

[Opción 3] escribir_archivo(nombre)
- Propósito: Añade texto al final de un archivo existente sin borrar su
  contenido previo.
- Funcionamiento: Valida que el archivo exista. Solicita el texto por consola,
  lo codifica en UTF-8 con un salto de línea y lo escribe usando un descriptor
  en modo escritura y adición (O_WRONLY | O_APPEND).

[Opción 4] leer_archivo(nombre)
- Propósito: Muestra en pantalla el contenido de un archivo de texto.
- Funcionamiento: Comprueba que el archivo exista, obtiene su tamaño en bytes
  con os.path.getsize(), abre el descriptor en modo solo lectura (O_RDONLY),
  lee los bytes correspondientes y los decodifica a texto legible (UTF-8).

[Opción 5] renombrar_archivo(nombre_actual, nombre_nuevo)
- Propósito: Cambia el nombre de un archivo existente.
- Funcionamiento: Verifica que el archivo original exista y que el nuevo
  nombre no esté ocupado para evitar sobrescrituras accidentales. Ejecuta el
  cambio mediante os.rename().

[Opción 6] copiar_archivo(nombre_origen, nombre_copia)
- Propósito: Crea un duplicado exacto de un archivo.
- Funcionamiento: Valida el archivo de origen. Si el nombre de destino ya
  existe, genera un nombre libre con un contador. Utiliza shutil.copy2() para
  duplicar tanto el contenido como los metadatos (fechas, permisos).

[Opción 7] elminar_archivo(nombre)
- Propósito: Borra un archivo de forma permanente.
- Funcionamiento: Verifica que la ruta exista y corresponda a un archivo (no a
  una carpeta). Solicita confirmación explícita al usuario ("s/n") antes de
  ejecutar os.remove().

[Opción 8] listar_archivos(nombre_directorio)
- Propósito: Muestra el contenido de una carpeta específica.
- Funcionamiento: Comprueba que la ruta sea un directorio válido y recorre sus
  elementos con os.listdir(), diferenciando visualmente entre [ARCHIVO] y
  [CARPETA].

[Opción 9] consultar_informacion(nombre)
- Propósito: Muestra los metadatos básicos de un archivo o carpeta.
- Funcionamiento: Verifica la existencia del elemento y extrae su tamaño en
  bytes (os.path.getsize) y su última fecha de modificación (os.path.getmtime),
  formateando esta última a "AAAA-MM-DD HH:MM:SS" mediante datetime.


4. FLUJO DEL PROGRAMA PRINCIPAL
--------------------------------------------------------------------------------
El bloque principal (__main__) ejecuta un bucle infinito (while True) que
despliega el menú numérico del 0 al 9. Captura la selección del usuario,
solicita los parámetros necesarios por consola, invoca la función
correspondiente y pausa la ejecución hasta que se presione Enter. La opción 0
rompe el bucle y finaliza el programa.
================================================================================
