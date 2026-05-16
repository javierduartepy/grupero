from app import db

HORARIOS_DISPONIBLES = [
    'Mañana',
    'Tarde',
    'Noche',
    'Mañana y Tarde',
    'Tarde y Noche',
    'Mañana y Noche',
    'Cualquier hora',
    'Sujeto a discusión',
]
DIAS_DISPONIBLES = [
    'Domingo',
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
]

class Persona(db.Model):
    __tablename__ = 'personas'

    id       = db.Column(db.Integer, primary_key=True)
    nombre   = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    horarios = db.Column(db.String(255), nullable=False)
    dias     = db.Column(db.String(255), nullable=False)

    def horarios_lista(self):
        return self.horarios.split(',')
    
    def dias_lista(self):
        return self.dias.split(',')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'horarios': self.horarios_lista(),
            'dias': self.dias_lista()
        }

    @staticmethod
    def existe(nombre, apellido):
        return Persona.query.filter(
            db.func.lower(Persona.nombre) == nombre.lower(),
            db.func.lower(Persona.apellido) == apellido.lower()
        ).first() is not None

    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'