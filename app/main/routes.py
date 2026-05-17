from flask import Blueprint, render_template
from app.models.persona import Persona
from app.models.grupo import Grupo

main_bp = Blueprint('main', __name__, template_folder='../templates/main')


@main_bp.route('/')
def index():
    total_personas = Persona.query.count()
    total_grupos = Grupo.query.count()
    return render_template('main/index.html', total_personas=total_personas, total_grupos=total_grupos)