import json

# TUPLA con los campos obligatorios del Cliente
CAMPOS_CLIENTE = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")


class Cliente:
    """MODELO: representa a un cliente."""

    def __init__(self, id_cliente, nombre, apellido, email, telefono, ciudad, direccion):
        self.id = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.direccion = direccion

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["telefono"],
            datos.get("ciudad", ""),
            datos.get("direccion", ""),
        )

    def a_json(self):
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    def __str__(self):
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"


class Estudiante:
    """MODELO: representa a un estudiante. Utiliza las 4 colecciones."""

    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito sin repetidos
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas = []
        for lista_notas in self.notas.values():
            todas.extend(lista_notas)
        if not todas:
            return 0
        return round(sum(todas) / len(todas), 2)

    def materias_en_comun(self, otro_estudiante):
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            "materias": sorted(self.materias), # Se convierte el set a list para JSON
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"