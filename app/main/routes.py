from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.persona import Persona
from app.models.grupo import Grupo

main_bp = Blueprint('main', __name__, template_folder='../templates')


@main_bp.route('/')
def index():
    total_personas = Persona.query.count()
    total_grupos = Grupo.query.count()
    return render_template('main/index.html', total_personas=total_personas, total_grupos=total_grupos)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    modal = None
    persona_data = None

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()

        if nombre and apellido:
            persona = Persona.query.filter(
                Persona.nombre == nombre,
                Persona.apellido == apellido
            ).first()

            if not persona:
                modal = 'no_registrado'
            else:
                session['usuario'] = {'id': persona.id, 'nombre': persona.nombre, 'apellido': persona.apellido}
                grupo = Grupo.query.filter(Grupo.personas.any(id=persona.id)).first()
                if not grupo:
                    modal = 'sin_grupo'
                    persona_data = {'nombre': nombre, 'apellido': apellido}
                else:
                    modal = 'con_grupo'
                    companieros = [p for p in grupo.personas if p.id != persona.id]
                    persona_data = {
                        'nombre': nombre,
                        'apellido': apellido,
                        'companieros': companieros,
                        'grupo_id': grupo.id
                    }

    return render_template('login.html',
        modal=modal,
        persona_data=persona_data)


@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))