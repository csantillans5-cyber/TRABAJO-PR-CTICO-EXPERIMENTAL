from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, registrar_nota, materias_ofertadas
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'CARNET':<12}{'NOMBRE COMPLETO':<28}{'CARRERA':<20}{'PROMEDIO':<10}")
    print("-" * 75)
    for est in estudiantes:
        print(f"{est.id:<5}{est.carnet:<12}{est.obtener_nombre_completo():<28}{est.carrera:<20}{est.obtener_promedio():<10}")
    print("-" * 75)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("REGISTRAR ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTADO DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("No hay estudiantes registrados.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Ingrese nombre, apellido, carnet o carrera: ")
    encontrados = buscar_estudiantes(termino)
    if not encontrados:
        imprimir_info(f"No se encontraron coincidencias para '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("REGISTRAR NOTA DE ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
        materia = input("Nombre de la materia: ").strip()
        nota = float(input("Nota (0 a 20): "))
    except ValueError:
        imprimir_error("ID y nota deben ser números válidos")
        return pausa()

    exito, mensaje = registrar_nota(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser entero")
        return pausa()

    estudiante = obtener_por_id(id_est)
    if not estudiante:
        imprimir_error("Estudiante no encontrado")
        return pausa()

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("ID del estudiante: "))
    except ValueError:
        imprimir_error("ID no válido")
        return pausa()

    estudiante = obtener_por_id(id_est)
    if not estudiante:
        imprimir_error("Estudiante no encontrado")
        return pausa()

    if confirmar(f"¿Desea eliminar a {estudiante.obtener_nombre_completo()}?"):
        exito, mensaje = eliminar_estudiante(id_est)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    pausa()


def opcion_materias():
    imprimir_titulo("MATERIAS REGISTRADAS EN EL SISTEMA")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("No hay materias asignadas a estudiantes todavía.")
    else:
        for m in materias:
            print(f"  • {m}")
    pausa()


def salir():
    imprimir_info("Saliendo del sistema...")
    return "salir"


OPCIONES = {
    "1": ("Registrar Estudiante", opcion_crear),
    "2": ("Ver Todos los Estudiantes", opcion_ver_todos),
    "3": ("Buscar Estudiante", opcion_buscar),
    "4": ("Registrar Nota / Materia", opcion_agregar_nota),
    "5": ("Actualizar Estudiante", opcion_actualizar),
    "6": ("Eliminar Estudiante", opcion_eliminar),
    "7": ("Ver Materias Globales", opcion_materias),
    "0": ("Salir", salir),
}


def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO (HERENCIA + MVC)")
        for tecla, (texto, _) in OPCIONES.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Seleccione una opción: ").strip()
        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")