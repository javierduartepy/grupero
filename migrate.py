from dotenv import load_dotenv
load_dotenv()
from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    db.session.execute(text('ALTER TABLE personas ADD COLUMN dias VARCHAR(255)'))
    db.session.execute(text("UPDATE personas SET dias = 'Sin especificar' WHERE dias IS NULL"))
    db.session.commit()
    print('Columna dias agregada OK')