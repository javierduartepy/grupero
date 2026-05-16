from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.persona import services
from app.models.persona import HORARIOS_DISPONIBLES

persona_bp = Blueprint('persona', __name__, template_folder='../templates/persona')


@persona_bp.route('/')
def index():
    personas = services.obtener_todas()
    return render_template('persona/index.html',
                           personas=personas,
                           horarios=HORARIOS_DISPONIBLES)


@persona_bp.route('/registrar', methods=['POST'])
def registrar():
    nombre   = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    horarios = request.form.getlist('horarios')

    if not nombre or not apellido or not horarios:
        flash('Completá todos los campos y seleccioná al menos un horario.', 'danger')
        return redirect(url_for('persona.index'))

    try:
        services.registrar(nombre, apellido, horarios)
        flash(f'{nombre} {apellido} registrado correctamente.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('persona.index'))


@persona_bp.route('/eliminar/<int:persona_id>', methods=['POST'])
def eliminar(persona_id):
    services.eliminar(persona_id)
    flash('Persona eliminada.', 'warning')
    return redirect(url_for('persona.index'))
