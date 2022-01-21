from db import db
import datetime

from models.sparf import *
from models.sparaw import *


class SPAProcessModel(db.Model):
    __tablename__ = 'spaprocesslist'

    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)
    PPName = db.Column(db.String(256), unique=True)
    PPDescription = db.Column(db.String(1024))
    PProduct = db.Column(db.Text())
    PPrice = db.Column(db.Float())
    PPDeleted = db.Column(db.Boolean(), default=False)
    PPFDeleted = db.Column(db.Boolean(), default=False)
    PPCreatedD = db.Column(db.Date(), default=datetime.date.today())
    PPCreated = db.Column(db.DateTime(), default=datetime.datetime.now())

    def __init__(self, id, PPName, PPDescription, PProduct, PPrice):
        self.id = id
        self.PPName = PPName
        self.PPDescription = PPDescription
        self.PProduct = PProduct
        self.PPrice = PPrice

    @classmethod
    def getAllPP(cls):
        return cls.query.all()

    @classmethod
    def getidPP(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def getnamePP(cls, _name):
        return cls.query.filter_by(PPName=_name).first()

    def savePP(self):
        db.session.add(self)
        db.session.commit()
        print('Process Product Added')

    def deletePP(self):
        db.session.delete(self)
        db.session.commit()
        print('Process Product Deleted')

    def updatePP(self):
        db.session.commit()
        print('Process Product Updated!')
