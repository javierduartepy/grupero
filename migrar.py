from dotenv import load_dotenv
load_dotenv()

from app import create_app, db

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(db.text('ALTER TABLE grupos ADD COLUMN IF NOT EXISTS fecha_exposicion VARCHAR(20)'))
            conn.commit()
            print('OK')
        except Exception as e:
            conn.rollback()
            print(f'Error: {e}')