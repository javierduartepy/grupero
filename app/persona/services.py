from app import db
from app.models.persona import Persona


def obtener_todas():
    return Persona.query.order_by(Persona.id).all()


def obtener_por_id(persona_id):
    return Persona.query.get_or_404(persona_id)


def registrar(nombre, apellido, dias, horarios):
    if Persona.existe(nombre, apellido):
        raise ValueError('Esa persona ya está registrada.')

    nueva = Persona(
        nombre=nombre,
        apellido=apellido,
        dias=','.join(dias),
        horarios=','.join(horarios)
    )
    db.session.add(nueva)
    db.session.commit()
    return nueva


def actualizar(persona_id, nombre, apellido, dias, horarios):
    persona = Persona.query.get_or_404(persona_id)
    persona.nombre   = nombre
    persona.apellido = apellido
    persona.dias     = ','.join(dias)
    persona.horarios = ','.join(horarios)
    db.session.commit()
    return persona


def eliminar(persona_id):
    persona = Persona.query.get_or_404(persona_id)
    db.session.delete(persona)
    db.session.commit()