from flask import Blueprint, request as req
from .models import Phrase
import json

class Router:
    def __init__(self, db, conf):
        self.router = Blueprint('vox', __name__)

        @self.router.route('/list')
        def list_coms():
            return json.dumps(Phrase.query.all())

        @self.router.route('/add')
        def add_com():
            payload = req.json or {}
            phrase = Phrase(**payload)

            db.session.add(phrase)
            db.session.commit()
            return ''

        @self.router.route('/remove')
        def remove_com():
            payload = req.json or {}
            phrase = Phrase.query.filter_by(payload.get('phrase')).first()

            db.session.delete(phrase)
            db.session.commit()
            return ''
