
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/test.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import flaskr.models
    Base.metadata.create_all(bind=engine)

'''from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flaskr.__init__ import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class packDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cards = db.relationship('cardDb', backref='pack', lazy=True)
    def __repr__(self):
        return '<Pack %r>' % self.id


class cardDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.Text)
    back = db.Column(db.Text)
    pack_id = db.Column(db.Integer, db.ForeignKey('pack.id'), nullable=False)
    def __repr__(self):
        return '<card %r>' % self.id
'''