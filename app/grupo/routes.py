from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.grupo import services
from app.models.persona import Persona

grupo_bp = Blueprint('grupo', __name__, template_folder='../templates/grupo')


@grupo_bp.route('/')
def index():
    grupos = services.obtener_todos()
    return render_template('grupo/index.html', grupos=grupos)


@grupo_bp.route('/formar')
def formar():
    personas = Persona.query.all()
    return render_template('grupo/crear.html', personas=personas)


@grupo_bp.route('/crear', methods=['POST'])
def crear():
    tamano = int(request.form.get('tamano', 3))
    metodo = request.form.get('metodo', 'azar')

    try:
        if metodo == 'azar':
            grupo = services.formar_al_azar(tamano)
        elif metodo == 'compatibilidad':
            grupo = services.formar_por_compatibilidad(tamano)
        elif metodo == 'manual':
            ids = [int(i) for i in request.form.getlist('manual_ids')]
            if len(ids) != tamano:
                flash(f'Seleccioná exactamente {tamano} personas.', 'danger')
                return redirect(url_for('grupo.formar'))
            grupo = services.formar_manual(ids)

        flash('Grupo formado correctamente.', 'success')
        return redirect(url_for('grupo.visualizar', grupo_id=grupo.id))

    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('grupo.crear'))


@grupo_bp.route('/visualizar/<int:grupo_id>')
def visualizar(grupo_id):
    grupo = services.obtener_por_id(grupo_id)
    return render_template('grupo/visualizar.html', grupo=grupo)


@grupo_bp.route('/eliminar/<int:grupo_id>', methods=['POST'])
def eliminar(grupo_id):
    services.eliminar(grupo_id)
    flash('Grupo eliminado.', 'warning')
    return redirect(url_for('grupo.index'))