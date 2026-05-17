import random
from itertools import combinations
from app import db
from app.models.persona import Persona
from app.models.grupo import Grupo


def obtener_todos():
    return Grupo.query.order_by(Grupo.id).all()


def obtener_por_id(grupo_id):
    return Grupo.query.get_or_404(grupo_id)


def _horarios_en_comun(personas):
    if not personas:
        return []
    comun = set(personas[0].horarios_lista())
    for p in personas[1:]:
        comun &= set(p.horarios_lista())
    return sorted(comun)


def _score_compatibilidad(combo):
    score = 0
    for i in range(len(combo)):
        for j in range(i + 1, len(combo)):
            score += len(set(combo[i].horarios_lista()) & set(combo[j].horarios_lista()))
    return score


def formar_al_azar(tamano):
    personas = Persona.query.all()
    if len(personas) < tamano:
        raise ValueError(f'Se necesitan al menos {tamano} personas registradas.')
    seleccionadas = random.sample(personas, tamano)
    return _guardar_grupo(seleccionadas)


def formar_por_compatibilidad(tamano):
    personas = Persona.query.all()
    if len(personas) < tamano:
        raise ValueError(f'Se necesitan al menos {tamano} personas registradas.')
    mejor_score = -1
    mejor_combo = None
    for combo in combinations(personas, tamano):
        score = _score_compatibilidad(combo)
        if score > mejor_score:
            mejor_score = score
            mejor_combo = list(combo)
    return _guardar_grupo(mejor_combo)


def formar_manual(ids):
    personas = Persona.query.filter(Persona.id.in_(ids)).all()
    if len(personas) != len(ids):
        raise ValueError('Una o más personas seleccionadas no existen.')
    return _guardar_grupo(personas)


def _guardar_grupo(personas):
    grupo = Grupo()
    grupo.personas = personas
    db.session.add(grupo)
    db.session.commit()
    return grupo


def eliminar(grupo_id):
    grupo = Grupo.query.get_or_404(grupo_id)
    db.session.delete(grupo)
    db.session.commit()