from .statics import db, ma

class Member(db.Model):
    __bind_key__ = 'net'
    __tablename__ = 'member'
    id = db.Column(db.Integer(), primary_key=True)
    group = db.Column(db.String, db.ForeignKey('group.name', ondelete='CASCADE'))
    node = db.Column(db.String, db.ForeignKey('node.addr', ondelete='CASCADE'))

    def __repr__(self):
        return MemberSchema().dumps(self)

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Member
        include_fk = True