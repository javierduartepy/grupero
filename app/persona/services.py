from app import db
from app.models.persona import Persona


def obtener_todas():
    return Persona.query.order_by(Persona.id).all()


def registrar(nombre, apellido, horarios):
    if Persona.existe(nombre, apellido):
        raise ValueError('Esa persona ya está registrada.')

    nueva = Persona(
        nombre=nombre,
        apellido=apellido,
        horarios=','.join(horarios)
    )
    db.session.add(nueva)
    db.session.commit()
    return nueva


def eliminar(persona_id):
    persona = Persona.query.get_or_404(persona_id)
    db.session.delete(persona)
    db.session.commit()