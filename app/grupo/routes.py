from flask import Blueprint, render_template, request, flash
from app.grupo import services
from app.models.persona import Persona

grupo_bp = Blueprint('grupo', __name__, template_folder='../templates/grupo')


@grupo_bp.route('/')
def index():
    personas = Persona.cargar_todas()
    return render_template('grupo/index.html', personas=personas)


@grupo_bp.route('/formar', methods=['POST'])
def formar():
    personas = Persona.cargar_todas()
    tamano = int(request.form.get('tamano', 3))
    metodo = request.form.get('metodo', 'azar')

    grupo = []
    horarios_comun = []

    try:
        if metodo == 'azar':
            grupo, horarios_comun = services.formar_al_azar(tamano)

        elif metodo == 'compatibilidad':
            grupo, horarios_comun = services.formar_por_compatibilidad(tamano)

        elif metodo == 'manual':
            ids = [int(i) for i in request.form.getlist('manual_ids')]
            if len(ids) != tamano:
                flash(f'Seleccioná exactamente {tamano} personas.', 'danger')
                return render_template('grupo/index.html', personas=personas)
            grupo, horarios_comun = services.formar_manual(ids)

    except ValueError as e:
        flash(str(e), 'danger')
        return render_template('grupo/index.html', personas=personas)

    return render_template('grupo/index.html',
                           personas=personas,
                           grupo=grupo,
                           horarios_comun=horarios_comun,
                           metodo=metodo,
                           tamano=tamano)
