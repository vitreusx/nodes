from flask import request as req, abort, url_for
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
        cred = open(self.conf.cred, 'r').read()

        with mic as src:
            rec.adjust_for_ambient_noise(src, duration=1)

        def callback(rec, audio):
            try:
                command = rec\
                    .recognize_google_cloud(audio, credentials_json=cred)\
                    .strip()
                print(command)

                phr = self.phrases.phrase(command)
                requests.post(url_for(phr['endpoint']), json=phr['payload'])

            except:
                pass
        
        with self.enabled_cv:
            while True:
                self.enabled_cv.wait_for(self.conf.enabled)
                with mic as src:
                    audio = rec.listen(src, phrase_time_limit=5)
                    callback(rec, audio)
        
    def validate(self, required):
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

        @nx.app.route('/voice', methods=['GET'])
        def check_voice():
            return str(self.conf.enabled)

        @nx.app.route('/voice', methods=['POST'])
        def set_voice():
            self.validate(['state'])
            self.conf.enabled = req.json['state']
            self.enabled_cv.notify()
            return ''

        @nx.app.route('/voice/phrases', methods=['GET'])
        def get_phrases():
            return json.dumps(self.phrases.phrases())

        @nx.app.route('/voice/phrase', methods=['GET'])
        def get_phrase():
            phrase = self.phrases.phrase(req.json['phrase'])
            if not phrase:
                return 'No such phrase is registered', 204
            else:
                return json.dumps(phrase)

        @nx.app.route('/voice/phrase', methods=['PUT'])
        def add_phrase():
            self.validate(['phrase', 'endpoint', 'payload'])

            if self.phrases.create(req.json['phrase'], \
                req.json['endpoint'], req.json['payload']):
                return ''
            else:
                return 'Phrase already registered', 400

        @nx.app.route('/voice/phrase', methods=['DELETE'])
        def remove_phrase():
            self.validate(['phrase'])

            if self.phrases.remove(req.json['phrase']):
                return ''
            else:
                return 'No such phrase is registered', 204
