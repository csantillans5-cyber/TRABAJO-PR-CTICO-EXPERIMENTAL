from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")


def carnets_registrados(excepto_id=None):
    """CONJUNTO con carnets registrados para evitar duplicados en O(1)."""
    return {
        r["carnet"].upper()
        for r in gestor.leer()
        if r["id"] != excepto_id
    }


def siguiente_id():
    ids = [r["id"] for r in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, "El email ingresado no es válido"

        if valores["carnet"].upper() in carnets_registrados():
            return False, f"El carnet '{valores['carnet']}' ya está registrado"

        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        gestor.guardar(registros)

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} registrado con éxito"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]


def obtener_por_id(id_estudiante):
    for est in obtener_todos():
        if est.id == id_estudiante:
            return est
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for r in gestor.leer():
        if (termino in r["nombre"].lower() or 
            termino in r["apellido"].lower() or 
            termino in r["carnet"].lower() or 
            termino in r.get("carrera", "").lower()):
            encontrados.append(Estudiante.desde_diccionario(r))
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    try:
        if "carnet" in cambios:
            if cambios["carnet"].upper() in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya pertenece a otro estudiante"

        registros = gestor.leer()
        posicion = None
        for i, r in enumerate(registros):
            if r["id"] == id_estudiante:
                posicion = i
                break

        if posicion is None:
            return False, f"No existe el estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, "Datos actualizados correctamente"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [r for r in registros if r["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe estudiante con id {id_estudiante}"

    gestor.guardar(quedan)
    return True, "Estudiante eliminado correctamente"


# ===================== NOTAS Y MATERIAS =====================

def registrar_nota(id_estudiante, materia, nota):
    try:
        if not (0 <= nota <= 20):
            return False, "La nota debe estar entre 0 y 20"

        estudiante = obtener_por_id(id_estudiante)
        if not estudiante:
            return False, "Estudiante no encontrado"

        estudiante.agregar_nota(materia, nota)

        # Actualizamos en el archivo JSON
        registros = gestor.leer()
        for r in registros:
            if r["id"] == id_estudiante:
                r["notas"] = estudiante.notas
                r["materias"] = sorted(estudiante.materias)
                break

        gestor.guardar(registros)
        return True, f"Nota {nota} asignada a {materia}"

    except Exception as error:
        return False, f"Error al registrar nota: {error}"


def materias_ofertadas():
    """Unión de todas las materias inscritas por los estudiantes usando conjuntos."""
    todas = set()
    for est in obtener_todos():
        todas |= est.materias
    return sorted(todas)