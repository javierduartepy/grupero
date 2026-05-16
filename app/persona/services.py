from app.models.persona import Persona


def obtener_todas():
    return Persona.cargar_todas()


def registrar(nombre, apellido, horarios):
    if Persona.existe(nombre, apellido):
        raise ValueError('Esa persona ya está registrada.')

    nueva = Persona(
        id=Persona.siguiente_id(),
        nombre=nombre,
        apellido=apellido,
        horarios=horarios
    )
    personas = Persona.cargar_todas()
    personas.append(nueva)
    Persona.guardar_todas(personas)
    return nueva


def eliminar(persona_id):
    personas = Persona.cargar_todas()
    personas = [p for p in personas if p.id != persona_id]
    # Re-numerar
    for i, p in enumerate(personas):
        p.id = i + 1
    Persona.guardar_todas(personas)
