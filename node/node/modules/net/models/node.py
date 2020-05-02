from .statics import db, ma

class Node(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'node'
    addr = db.Column(db.String(320), primary_key=True)
    alias = db.Column(db.String(80), unique=True, nullable=True)

    def __repr__(self):
        return NodeSchema().dumps(self)

class NodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        include_fk = True