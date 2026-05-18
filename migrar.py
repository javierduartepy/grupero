from dotenv import load_dotenv
load_dotenv()

from app import create_app, db

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(db.text('ALTER TABLE grupos ADD COLUMN IF NOT EXISTS tema VARCHAR(200)'))
        except Exception as e:
            print(f'tema: {e}')
        try:
            conn.execute(db.text('ALTER TABLE grupos ADD COLUMN IF NOT EXISTS archivo VARCHAR(200)'))
        except Exception as e:
            print(f'archivo: {e}')
        try:
            conn.execute(db.text('ALTER TABLE grupos ADD COLUMN IF NOT EXISTS observacion TEXT'))
        except Exception as e:
            print(f'observacion: {e}')
        try:
            conn.execute(db.text('ALTER TABLE grupos ADD COLUMN IF NOT EXISTS fecha_exposicion VARCHAR(20)'))
        except Exception as e:
            print(f'fecha_exposicion: {e}')
        conn.commit()
    print('Migración completada.')