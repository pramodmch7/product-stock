from db import db
import datetime

from models.sparf import *
from models.sparaw import *


class SPAFinalModel(db.Model):
    __tablename__ = 'spafinallist'

    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)
    FPName = db.Column(db.String(256), unique=True)
    FPDescription = db.Column(db.String(1024))
    FPDeleted = db.Column(db.Boolean(), default=False)
    FPFDeleted = db.Column(db.Boolean(), default=False)
    FPCreatedD = db.Column(db.Date(), default=datetime.date.today())
    FPCreated = db.Column(db.DateTime(), default=datetime.datetime.now())
    RawMats = db.relationship('SPARFModel', backref=db.backref(
        'FinalProducts'))

    def __init__(self, id, FPName, FPDescription):
        self.id = id
        self.FPName = FPName
        self.FPDescription = FPDescription

    @classmethod
    # Get All List of Final Product
    def getAllFP(cls):
        return cls.query.all()

    @classmethod
    # Get Specific Final Product with ID
    def getidFP(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    # Get Specific Final Product with Name
    def getnameFP(cls, _name):
        return cls.query.filter_by(FPName=_name).first()

    def saveFP(self):
        db.session.add(self)
        db.session.commit()
        print('Final Product Added')

    def deleteFP(self):
        db.session.delete(self)
        db.session.commit()
        print('Final Product Deleted')

    def updateFP(self):
        db.session.commit()
        print('Final Product Updated!')
