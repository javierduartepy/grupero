from flask import Flask
from config import config
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Crear carpeta de datos si no existe
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Registrar Blueprints
    from app.main.routes import main_bp
    from app.persona.routes import persona_bp
    from app.grupo.routes import grupo_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(persona_bp, url_prefix='/persona')
    app.register_blueprint(grupo_bp, url_prefix='/grupo')

    return app
