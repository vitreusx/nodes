from .statics import db, ma
from .node import Node
from .member import Member

class Group(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'group'
    name = db.Column(db.String, primary_key=True)
    members = db.relationship('Node', secondary='member')

class GroupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        include_fk = True
