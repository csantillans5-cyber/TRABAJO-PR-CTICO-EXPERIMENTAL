import json

CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet", "carrera")


# ===================== CLASE BASE (PADRE) =====================
class Persona:
    """Clase base que encapsula los atributos generales."""

    def __init__(self, id_persona, nombre, apellido, email):
        self.id = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
        }


# ===================== CLASE DERIVADA (HIJA) =====================
class Estudiante(Persona):
    """Clase que hereda de Persona e incluye atributos y métodos específicos."""

    def __init__(self, id_persona, nombre, apellido, email, carnet, carrera, notas=None, materias=None):
        # Invocamos al constructor de la clase Padre (Persona)
        super().__init__(id_persona, nombre, apellido, email)
        self.carnet = carnet
        self.carrera = carrera
        # DICCIONARIO de listas: {"Matemática": [18, 19]}
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito sin duplicados
        self.materias = set(materias) if materias else set()

    def inscribir_materia(self, materia):
        self.materias.add(materia)

    def agregar_nota(self, materia, nota):
        self.inscribir_materia(materia)
        self.notas.setdefault(materia, []).append(nota)

    def obtener_promedio(self):
        todas = [n for lista in self.notas.values() for n in lista]
        return round(sum(todas) / len(todas), 2) if todas else 0.0

    def materias_en_comun(self, otro_estudiante):
        # Intersección de conjuntos
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        # Reutilizamos el diccionario del padre y agregamos los datos del estudiante
        datos = super().a_diccionario()
        datos.update({
            "carnet": self.carnet,
            "carrera": self.carrera,
            "notas": self.notas,
            "materias": sorted(self.materias),  # Convertimos el set a list para JSON
        })
        return datos

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            datos.get("carrera", "Sin Carrera"),
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Carrera: {self.carrera} | Promedio: {self.obtener_promedio()}"