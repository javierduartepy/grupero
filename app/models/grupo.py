from app import db

grupo_persona = db.Table('grupo_persona',
    db.Column('grupo_id', db.Integer, db.ForeignKey('grupos.id'), primary_key=True),
    db.Column('persona_id', db.Integer, db.ForeignKey('personas.id'), primary_key=True)
)


class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    personas = db.relationship('Persona', secondary='grupo_persona', lazy='subquery')

    def cantidad(self):
        return len(self.personas)