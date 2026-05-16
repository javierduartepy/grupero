from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.persona import services
from app.models.persona import HORARIOS_DISPONIBLES, DIAS_DISPONIBLES

persona_bp = Blueprint('persona', __name__, template_folder='../templates/persona')


@persona_bp.route('/')
def index():
    personas = services.obtener_todas()
    return render_template('persona/index.html', personas=personas)


@persona_bp.route('/nueva')
def nueva():
    return render_template('persona/crear.html',
                           dias=DIAS_DISPONIBLES,
                           horarios=HORARIOS_DISPONIBLES)


@persona_bp.route('/registrar', methods=['POST'])
def registrar():
    nombre   = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    horarios = request.form.getlist('horarios')
    dias     = request.form.getlist('dias')

    if not nombre or not apellido or not horarios or not dias:
        flash('Completá todos los campos y seleccioná al menos un horario y día.', 'danger')
        return redirect(url_for('persona.nueva'))

    try:
        services.registrar(nombre, apellido, dias, horarios)
        flash(f'{nombre} {apellido} registrado correctamente.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('persona.nueva'))

    return redirect(url_for('persona.index'))


@persona_bp.route('/visualizar/<int:persona_id>')
def visualizar(persona_id):
    persona = services.obtener_por_id(persona_id)
    return render_template('persona/visualizar.html', persona=persona)


@persona_bp.route('/modificar/<int:persona_id>')
def modificar(persona_id):
    persona = services.obtener_por_id(persona_id)
    return render_template('persona/modificar.html',
                           persona=persona,
                           dias=DIAS_DISPONIBLES,
                           horarios=HORARIOS_DISPONIBLES)


@persona_bp.route('/actualizar/<int:persona_id>', methods=['POST'])
def actualizar(persona_id):
    nombre   = request.form.get('nombre', '').strip()
    apellido = request.form.get('apellido', '').strip()
    horarios = request.form.getlist('horarios')
    dias     = request.form.getlist('dias')

    if not nombre or not apellido or not horarios or not dias:
        flash('Completá todos los campos.', 'danger')
        return redirect(url_for('persona.modificar', persona_id=persona_id))

    try:
        services.actualizar(persona_id, nombre, apellido, dias, horarios)
        flash('Persona actualizada correctamente.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('persona.modificar', persona_id=persona_id))

    return redirect(url_for('persona.index'))


@persona_bp.route('/eliminar/<int:persona_id>', methods=['POST'])
def eliminar(persona_id):
    services.eliminar(persona_id)
    flash('Persona eliminada.', 'warning')
    return redirect(url_for('persona.index'))