'''from sqlalchemy import Column, Integer, String
from flaskr.database import Base

class packDb(Base):
    __tablename__ = "pack"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    cards = relationship('cardDb', backref='pack', lazy=True)
    def __repr__(self):
        return '<Pack %r>' % self.id


class cardDb(db.Model):
    id = Column(Integer, primary_key=True)
    front = Column(Text)
    back = Column(Text)
    pack_id = Column(Integer, ForeignKey('pack.id'), nullable=False)
    def __repr__(self):
        return '<card %r>' % self.id'''

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from flaskr.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Pack(Base):
    __tablename__ = 'pack'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    children = relationship("Cards")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Pack %r>' % self.name

class Cards(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    front = Column(String(300) , nullable=False)
    back = Column(String(300) , nullable=False)
    pack_id = Column(Integer, ForeignKey('pack.id'))


    def __init__(self, front=None, back=None, pack_id=None):
        self.front = front
        self.back = back
        
        self.pack_id = pack_id

    def __repr__(self):
        return '<Cards %r>' % self.front

'''  pack_to_open = Pack.query.get_or_404(id)
        if request.method =='POST':

            try:
                return render_template('packView.html',  pack= pack_to_open, card = Cards.query.filter(Cards.pack_id==id).all())
            except:
                return "it was not possible to go into this pack"
        else:
            '''