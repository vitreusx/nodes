from .statics import db, ma

class Phrase(db.Model):
    __bind_key__ = 'vox'
    __tablename__ = 'phrase'

    phr = db.Column(db.String, primary_key = True)
    command = db.Column(db.String, nullable = False)
    payload = db.Column(db.String, nullable = True)

    def __repr__(self):
        return PhraseSchema().dumps(self)

class PhraseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Phrase
        include_fk = True
