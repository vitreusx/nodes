from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Groups(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'groups'
    name = db.Column(db.String(80), primary_key=True)
    members = db.relationship('Node', secondary='group_members')

class Node(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'node'
    addr = db.Column(db.String(320), primary_key=True)
    alias = db.Column(db.String(80), unique=True)

class Members(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'members'
    id = db.Column(db.Integer(), primary_key=True)
    group = db.Column(db.String(80), db.ForeignKey('groups.name', ondelete='CASCADE'))
    node = db.Column(db.String(320), db.ForeignKey('node.addr', ondelete='CASCADE'))
