import random
from itertools import combinations
from app.models.persona import Persona


def _horarios_en_comun(grupo):
    if not grupo:
        return []
    comun = set(grupo[0].horarios)
    for p in grupo[1:]:
        comun &= set(p.horarios)
    return sorted(comun)


def _score_compatibilidad(combo):
    score = 0
    for i in range(len(combo)):
        for j in range(i + 1, len(combo)):
            score += len(set(combo[i].horarios) & set(combo[j].horarios))
    return score


def formar_al_azar(tamano):
    personas = Persona.cargar_todas()
    if len(personas) < tamano:
        raise ValueError(f'Se necesitan al menos {tamano} personas registradas.')
    grupo = random.sample(personas, tamano)
    return grupo, _horarios_en_comun(grupo)


def formar_por_compatibilidad(tamano):
    personas = Persona.cargar_todas()
    if len(personas) < tamano:
        raise ValueError(f'Se necesitan al menos {tamano} personas registradas.')

    mejor_score = -1
    mejor_combo = None
    for combo in combinations(personas, tamano):
        score = _score_compatibilidad(combo)
        if score > mejor_score:
            mejor_score = score
            mejor_combo = list(combo)

    return mejor_combo, _horarios_en_comun(mejor_combo)


def formar_manual(ids):
    personas = Persona.cargar_todas()
    grupo = [p for p in personas if p.id in ids]
    if len(grupo) != len(ids):
        raise ValueError('Una o más personas seleccionadas no existen.')
    return grupo, _horarios_en_comun(grupo)
