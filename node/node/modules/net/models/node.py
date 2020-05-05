from .statics import db, ma

class Node(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'node'
    addr = db.Column(db.String, primary_key=True)
    alias = db.Column(db.String, unique=True, nullable=True)

class NodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        include_fk = True
