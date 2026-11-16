# librerías ---------------------------------------------------------------------------------------------------
import os
import shutil # para copiar archivos (opción 6)
import datetime # para mostrar la fecha de modificación (opción 9)

# Funciones de gestión de archivos ----------------------------------------------------------------------------

def crear_directorio(nombre):
    ruta_final = nombre
    contador = 1 # para verificar si el nombre ya existe y crear uno nuevo con un número al final

    #Busca un nombre libre: "carpeta (1)", "carpeta (2)", etc, para que no haya error por repetir nombres.
    while os.path.exists(ruta_final):
        ruta_final = f"{nombre} ({contador})"
        contador += 1

    # Crea el directorio con el nombre libre encontrado
    os.makedirs(ruta_final)

    # Mensaje final
    return "se ha creado el directorio: " + ruta_final



def crear_archivo_txt(nombre):
    # Nos aseguramos de que el archivo tenga la extensión ".txt" al final
    if not nombre.endswith(".txt"):
        # Sino la tiene la pegamos al final
        nombre += ".txt"

    # Separamos el nombre del archivo por si debemos modificar el nombre para que no se repita
    base, extension = os.path.splitext(nombre)
    ruta_final = nombre
    contador = 1

    # Busca un nombre libre: "nombre (1).txt", "nombre (2).txt", etc.
    while os.path.exists(ruta_final):
        ruta_final = f"{base} ({contador}){extension}"
        contador += 1

    # descriptor de archivo: es un número entero que representa un archivo abierto en el sistema operativo.
    descriptor = os.open(ruta_final, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    # os.O_CREAT Activa la creación. Le ordena al sistema operativo que, si el archivo indicado en ruta_final no existe en el disco, lo cree desde cero.
    # os.O_EXCL garantiza que no se sobrescriba si algo se creó en ese mismo instante
    # os.O_WRONLY indica que el archivo se abrirá en modo de escritura, es obligatorio incluir este modo para poder crear un archivo nuevo.
    
    os.close(descriptor) # Cerramos el descriptor de archivo para liberar recursos

    return "se ha creado el archivo: " + ruta_final

def escribir_archivo(nombre):
    # Verificamos si al nombre le falta el ".txt" para agregárselo y que coincida con cómo se crean en la opción 2
    if not nombre.endswith(".txt"):
        nombre += ".txt"

    # Validamos que el archivo exista y que sea un archivo (no una carpeta) antes de intentar escribir
    if not os.path.isfile(nombre):
        return "Error: el archivo " + nombre + " no existe"

    #Si existe, pedimos el texto al usuario
    contenido= input("Ingrese la información a escribir: ")
    
    try:
        # Abrimos el archivo usando su descriptor en el sistema operativo.
        # os.O_WRONLY abre el archivo únicamente en modo de escritura.
        # os.O_APPEND mueve el puntero al final del archivo en cada escritura, para agregar la nueva información sin borrar lo que ya tenía antes.
        descriptor = os.open(nombre, os.O_WRONLY | os.O_APPEND)

        # Usamos codificación UTF-8 para evitar problemas con caracteres especiales, además separamos con un salto de linea.
        datos_bytes = (contenido + "\n").encode("utf-8")

        # Pedimosal sistema operativo escribir esos bytes en el archivo asociado al descriptor
        os.write(descriptor, datos_bytes)

        # Cerramos el descriptor para que los cambios se guarden en disco y liberar el recurso
        os.close(descriptor)
        
    except OSError as error:
        return "Error al escribir en el archivo: " + str(error)

    return "se ha agregado la información al archivo: " + nombre



def leer_archivo(nombre):
    # Igual que en las funciones anteriores, aseguramos la extensión ".txt" si el usuario no la puso
    if not nombre.endswith(".txt"):
        nombre += ".txt"

    # Validamos que el archivo exista y no sea un directorio antes de leerlo
    if not os.path.isfile(nombre):
        return "Error: el archivo " + nombre + " no existe"

    try:
        # os.O_RDONLY le indica al sistema operativo que solo vamos a abrir el archivo en modo lectura (read-only)
        descriptor = os.open(nombre, os.O_RDONLY)

        # Consultamos el tamaño total del archivo en bytes para saber cuánto debemos leer con os.read
        tamano = os.path.getsize(nombre)

        # os.read recibe el descriptor y la cantidad de bytes que queremos traer de memoria
        bytes_leidos = os.read(descriptor, tamano)

        # Cerramos el descriptor apenas terminamos de leer para liberar recursos del sistema
        os.close(descriptor)

        # Convertimos los bytes leídos de vuelta a texto normal (string) usando decodificación UTF-8
        contenido = bytes_leidos.decode("utf-8")

        # Si el archivo recién se creó y no tiene nada escrito todavía, avisamos que está vacío
        if contenido == "":
            return "El archivo " + nombre + " está vacío"

        return "\n--- Contenido de " + nombre + " ---\n" + contenido.rstrip("\n") + "\n-------------------------------"
    except OSError as error:
        return "Error al leer el archivo: " + str(error)

def renombrar_archivo(nombre_actual, nombre_nuevo):
    # Validamos que el archivo que se quiere renombrar exista y sea un archivo (no una carpeta)
    if not os.path.isfile(nombre_actual):
        return "Error: el archivo " + nombre_actual + " no existe"

    # Si el nuevo nombre ya está ocupado no renombramos, para no reemplazar otro archivo sin querer
    if os.path.exists(nombre_nuevo):
        return "Error: ya existe un archivo con el nombre " + nombre_nuevo

    try:
        # os.rename le pide al sistema operativo cambiar la entrada del archivo en el directorio.
        # El contenido no se mueve ni se copia, solo cambia el nombre con el que se encuentra.
        os.rename(nombre_actual, nombre_nuevo)
    except OSError as error:
        # Por ejemplo: el archivo está abierto en otro programa o no hay permisos
        return "Error al renombrar: " + str(error)

    return "se ha renombrado " + nombre_actual + " a " + nombre_nuevo

def copiar_archivo(nombre_origen, nombre_copia):
    # Validamos que el archivo original exista y sea un archivo
    if not os.path.isfile(nombre_origen):
        return "Error: el archivo " + nombre_origen + " no existe"

    # Igual que al crear archivos: si el nombre de la copia ya existe buscamos uno libre
    # "copia (1).txt", "copia (2).txt", etc, para no sobrescribir nada
    base, extension = os.path.splitext(nombre_copia)
    ruta_final = nombre_copia
    contador = 1
    while os.path.exists(ruta_final):
        ruta_final = f"{base} ({contador}){extension}"
        contador += 1

    try:
        # shutil.copy2 crea un archivo nuevo con el mismo contenido
        # y además conserva los metadatos, como la fecha de modificación
        shutil.copy2(nombre_origen, ruta_final)
    except OSError as error:
        return "Error al copiar: " + str(error)

    return "se ha creado la copia: " + ruta_final

def elminar_archivo(nombre):    
    if os.path.exists(nombre):
        if os.path.isfile(nombre):
            confirmar = input("Esta seguro que desea eliminar el archivo (s/n): ")
            if confirmar.lower() == "s":
                os.remove(nombre)  
                print("Se ha eliminado el archivo exitosamente.")
            else:
                print("Se ha cancelado la eliminación del archivo")
        else:
            print("La ruta corresponde a un directorio, no a un archivo")
    else:
        print("El archivo no existe")  

def listar_archivos(nombre_directorio):
    if os.path.exists(nombre_directorio):
        if os.path.isdir(nombre_directorio):
            elementos = os.listdir(nombre_directorio)
            print("\nContenido del directorio:")
            for elemento in elementos:
                ruta = os.path.join(nombre_directorio, elemento)
                if os.path.isfile(ruta):
                    print("[ARCHIVO]", elemento)
                elif os.path.isdir(ruta):
                    print("[CARPETA]", elemento)
        else:
            print("La ruta no corresponde a un directorio")
    else:
        print("El directorio no existe")

def consultar_informacion(nombre):
    if not os.path.exists(nombre):
        return "La ruta especificada no existe."
    
    try:
        tamano = os.path.getsize(nombre)
        # Obtenemos el timestamp y lo convertimos a fecha legible con datetime
        timestamp_mod = os.path.getmtime(nombre)
        fecha_mod = datetime.datetime.fromtimestamp(timestamp_mod).strftime('%Y-%m-%d %H:%M:%S')
        
        resultado = (
            f"\n--- Información del elemento ---\n"
            f"Nombre: {nombre}\n"
            f"Tamaño: {tamano} bytes\n"
            f"Última fecha de modificación: {fecha_mod}\n"
            f"----------------------------------"
        )
        return resultado
    except OSError as error:
        return f"Error al consultar la información: {str(error)}"

# Programa principal -------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Aseguramos que el programa se ejecute si existe la carpeta de trabajo "GESTOR_SO" y nos ubicamos en ella.
    os.makedirs("GESTOR_SO", exist_ok=True)
    os.chdir("GESTOR_SO")
     
    while True:
        print("\nBienvenido al Gestor de Archivos")
        print("Seleccione una opción válida:\n")
        print("1. Crear un directorio")
        print("2. Crear un archivo de texto")
        print("3. Escribir información en un archivo")
        print("4. Leer el contenido de un archivo")
        print("5. Renombrar un archivo")
        print("6. Copiar un archivo")
        print("7. Eliminar un archivo")
        print("8. Listar archivos de un directorio")
        print("9. Consultar información de un archivo")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")

        # Menú de opciones --------------------------------------------------------------

        if opcion == "1":
            input_nombre = input("\nIngrese el nombre del directorio a crear: ")
            print(crear_directorio(input_nombre))
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            input_nombre = input("\nIngrese el nombre del archivo a crear: ")
            print(crear_archivo_txt(input_nombre))
            input("\nPresione Enter para continuar...")
        
        elif opcion == "3":
            input_nombre = input("\nIngrese el nombre del archivo en el que desea escribir: ")
            print(escribir_archivo(input_nombre))
            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            input_nombre = input("\nIngrese el nombre del archivo a leer: ")
            print(leer_archivo(input_nombre))
            input("\nPresione Enter para continuar...")

        elif opcion == "5":
            input_actual = input("\nIngrese el nombre del archivo a renombrar: ")
            input_nuevo = input("Ingrese el nuevo nombre: ")
            print(renombrar_archivo(input_actual, input_nuevo))
            input("\nPresione Enter para continuar...")

        elif opcion == "6":
            input_origen = input("\nIngrese el nombre del archivo a copiar: ")
            input_copia = input("Ingrese el nombre de la copia: ")
            print(copiar_archivo(input_origen, input_copia))
            input("\nPresione Enter para continuar...")

        elif opcion == "7":
            input_nombre = input("\nIngrese el nombre del archivo a eliminar: ")
            elminar_archivo(input_nombre)
            input("\nPresione Enter para continuar...")

        elif opcion == "8":
            input_nombre = input("\nIngrese el directorio que desea listar: ")
            listar_archivos(input_nombre)
            input("\nPresione Enter para continuar...")

        elif opcion == "9":
            input_nombre = input("\nIngrese el nombre del archivo o directorio a consultar: ")
            print(consultar_informacion(input_nombre))
            input("\nPresione Enter para continuar...")

        elif opcion == "0": # Salida
            break

        else: # Opción no válida
            print("\nOpción no válida. Por favor, seleccione una opción del 0 al 9\n")
            input("\nPresione Enter para continuar...")