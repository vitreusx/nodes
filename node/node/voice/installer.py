from flask import request as req, abort, url_for
from flask_restful import Resource
import json
import speech_recognition as sr
import requests
from threading import Thread, Condition
from ..nexus import Nexus
from .config import Config
from .phrases import Phrases

class Installer:
    def voice_thread(self):
        rec = sr.Recognizer()
        mic = sr.Microphone()
        try:
            cred = open(self.conf.cred, 'r').read()
        except:
            cred = ''

        with mic as src:
            rec.adjust_for_ambient_noise(src, duration=1)

        def callback(rec, audio):
            try:
                command = rec\
                    .recognize_google_cloud(audio, credentials_json=cred)\
                    .strip()
                print(f'[Voice] Phrase: {command}')

                phr = self.phrases.phrase(command)
                other_node_name = nx.conf['net']['name']
                requests.post(req.url_root + phr['endpoint'], json=phr['payload'], **nx.auth.get_requests_auth(other_node_name))

            except:
                pass
        
        while True:
            with self.enabled_cv:
                self.enabled_cv.wait_for(lambda: self.conf.enabled)
            with mic as src:
                audio = rec.listen(src, phrase_time_limit=5)
                callback(rec, audio)
    
    @staticmethod
    def validate(required):
        if not req.json \
            or any(param not in req.json \
                    for param in required):
            abort(404)
    
    def __init__(self, nx: Nexus):
        self.nx = nx
        self.conf = Config(nx.conf.get('voice') or {})
        self.phrases = Phrases(self.conf)
        self.enabled_cv = Condition()
        self.thr = Thread(target=self.voice_thread)
        self.thr.start()
        inst = self

        class Voice(Resource):
            @nx.httpauth.login_required
            def get(self):
                return inst.conf.enabled
            
            @nx.httpauth.login_required
            def post(self):
                inst.conf.enabled = req.json['state']
                with inst.enabled_cv:
                    inst.enabled_cv.notify()
        
        nx.api.add_resource(Voice, '/voice')

        class PhraseList(Resource):
            @nx.httpauth.login_required
            def get(self):
                return inst.phrases.phrases()
        
        nx.api.add_resource(PhraseList, '/voice/phrases')

        class Phrase(Resource):
            @nx.httpauth.login_required
            def get(self, phrase):
                return inst.phrases.phrase(phrase)
            
            @nx.httpauth.login_required
            def put(self, phrase):
                inst.phrases.db[phrase] = {
                    'endpoint': req.json['endpoint'],
                    'payload': req.json['payload']
                }

            @nx.httpauth.login_required
            def post(self, phrase):
                phr = inst.phrases.phrase(phrase)
                other_node_name = nx.conf['net']['name']
                requests.post(req.url_root + phr['endpoint'], json=phr['payload'], **nx.auth.get_requests_auth(other_node_name))
            
            @nx.httpauth.login_required
            def delete(self, phrase):
                inst.phrases.remove(phrase)

        nx.api.add_resource(Phrase, '/voice/p/<phrase>')
