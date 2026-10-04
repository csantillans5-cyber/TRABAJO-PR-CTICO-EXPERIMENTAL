from models import Cliente, CAMPOS_CLIENTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/clientes.json")

# TUPLAS de configuración
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """CONJUNTO con emails registrados para prevenir duplicados."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_cliente(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_CLIENTE}

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        cliente = Cliente(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(cliente.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Cliente {cliente.obtener_nombre_completo()} creado con id {cliente.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Cliente.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_cliente):
    for cliente in obtener_todos():
        if cliente.id == id_cliente:
            return cliente
    return None


# ===================== S · SEARCH =====================

def buscar_clientes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Cliente.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_cliente(id_cliente, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_CLIENTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_cliente):
                return False, "Ese email ya lo usa otro cliente"

        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_cliente:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un cliente con id {id_cliente}"

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return True, f"Cliente {id_cliente} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_cliente(id_cliente):
    registros = gestor.leer()
    quedan = [registro for registro in registros if registro["id"] != id_cliente]

    if len(quedan) == len(registros):
        return False, f"No existe un cliente con id {id_cliente}"

    gestor.guardar(quedan)
    return True, f"Cliente {id_cliente} eliminado"


# ===================== EXTRA · ESTADÍSTICAS & AGRUPACIONES =====================

def estadisticas():
    registros = gestor.leer()
    ciudades = {r.get("ciudad", "").title() for r in registros if r.get("ciudad")}
    dominios = {r["email"].split("@")[1].lower() for r in registros if "@" in r["email"]}
    sin_telefono = [r["nombre"] for r in registros if not r.get("telefono")]

    return {
        "total": len(registros),
        "ciudades": sorted(ciudades),
        "dominios": sorted(dominios),
        "sin_telefono": sin_telefono,
    }


def clientes_por_ciudad():
    """Agrupa clientes por ciudad usando setdefault."""
    agrupados = {}
    for registro in gestor.leer():
        ciudad = registro.get("ciudad", "").title() or "Sin ciudad"
        agrupados.setdefault(ciudad, []).append(registro["nombre"])
    return agrupados