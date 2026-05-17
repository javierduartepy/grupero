from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Registrar Blueprints
    from app.main.routes import main_bp
    from app.persona.routes import persona_bp
    from app.grupo.routes import grupo_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(persona_bp, url_prefix='/persona')
    app.register_blueprint(grupo_bp, url_prefix='/grupo')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.template_filter('fecha_formato')
    def fecha_formato(fecha):
        if not fecha:
            return '—'
        try:
            from datetime import datetime
            return datetime.strptime(fecha, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            return fecha

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app