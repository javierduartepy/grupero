import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'personas.json')

HORARIOS_DISPONIBLES = [
    'Mañana',
    'Tarde',
    'Noche',
    'Mañana y Tarde',
    'Tarde y Noche',
    'Mañana y Noche',
    'Todo el día'
]


class Persona:
    def __init__(self, id, nombre, apellido, horarios):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.horarios = horarios

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'horarios': self.horarios
        }

    @staticmethod
    def from_dict(data):
        return Persona(
            id=data['id'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            horarios=data['horarios']
        )

    @staticmethod
    def cargar_todas():
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [Persona.from_dict(p) for p in data]

    @staticmethod
    def guardar_todas(personas):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in personas], f, ensure_ascii=False, indent=2)

    @staticmethod
    def existe(nombre, apellido):
        personas = Persona.cargar_todas()
        return any(
            p.nombre.lower() == nombre.lower() and
            p.apellido.lower() == apellido.lower()
            for p in personas
        )

    @staticmethod
    def siguiente_id():
        personas = Persona.cargar_todas()
        if not personas:
            return 1
        return max(p.id for p in personas) + 1
