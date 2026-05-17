from app import db

grupo_persona = db.Table('grupo_persona',
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id'), primary_key=True),
    db.Column('persona_id', db.Integer, db.ForeignKey('personas.id'), primary_key=True)
)


class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    tema = db.Column(db.String(200), nullable=True)
    archivo = db.Column(db.String(200), nullable=True)
    observacion = db.Column(db.Text, nullable=True)
    personas = db.relationship('Persona', secondary='grupo_persona', lazy='subquery')
    fecha_exposicion = db.Column(db.String(20), nullable=True)

    def cantidad(self):
        return len(self.personas)