from .models import db, ma, Phrase
from .router import Router
from flask import request as req
import speech_recognition as sr
from multiprocessing import Process
from os.path import join
import requests


def install(app, conf):
    path = join(app.root, conf.get('db') or 'db/vox.db')
    app.ensure_fs(path)

    db_uri = f'sqlite:///{path}'
    app.flask.config['SQLALCHEMY_BINDS']['vox'] = db_uri

    db.init_app(app.flask)
    ma.init_app(app.flask)
    with app.flask.app_context():
        db.create_all(bind='vox')
    
    router = Router(db, conf)
    app.flask.register_blueprint(router.router, url_prefix='/net')

    cred_path = join(app.root, conf.get('cloud') or 'auth.json')
    cred = open(cred_path, 'r').read()

    def cb(rec, audio):
        try:
            phrase = rec.recognize_google_cloud(audio, credentials_json=cred).strip()            
            instr = Phrase.query.filter_by(phr = phrase).first()

            if instr:
                requests.post(f'http://{req.host}{instr.command}', instr.payload)

        except:
            pass

    def voice_thread_fn():
        rec = sr.Recognizer()
        mic = sr.Microphone()

        with mic as src:
            rec.adjust_for_ambient_noise(src, duration=1)

        while True:
            with mic as src:
                audio = rec.listen(src, phrase_time_limit=5)
                cb(rec, audio)

    voice_thr = Process(target=voice_thread_fn)
    voice_thr.start()
