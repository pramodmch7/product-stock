from db import db
import datetime

from models.spafinal import *
from models.sparf import *


class SPARawModel(db.Model):
    __tablename__ = 'sparawlist'
    id1 = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String, unique=True)
    RPName = db.Column(db.String(256), unique=True)
    RPDescription = db.Column(
        db.String(1024))
    RPQuantity = db.Column(db.Integer)
    RPPrice = db.Column(db.Float)
    RPWeight = db.Column(db.String(128))
    RPDeleted = db.Column(db.Boolean(), default=False)
    RPFDeleted = db.Column(db.Boolean(), default=False)
    RPCreatedD = db.Column(db.Date(), default=datetime.date.today())
    RPCreated = db.Column(db.DateTime(), default=datetime.datetime.now())
    FinalProd = db.relationship('SPARFModel', backref=db.backref(
        'RawMaterials'))

    def __init__(self, id, RPName, RPDescription, RPQuantity, RPPrice, RPWeight):
        self.id = id
        self.RPName = RPName
        self.RPDescription = RPDescription
        self.RPQuantity = RPQuantity
        self.RPPrice = RPPrice
        self.RPWeight = RPWeight

    @classmethod
    # Get All List of Raw Product
    def getAllRP(cls):
        return cls.query.all()

    @classmethod
    # Get Specific Raw Product
    def getRP(cls, name):
        return cls.query.filter_by(RPName=name).first()

    @classmethod
    # Get Specific Raw Product with id
    def getidRP(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def saveRP(self, name):
        db.session.add(self)
        db.session.commit()
        print(f'{name} Added')

    def deleteRP(self):
        db.session.delete(self)
        db.session.commit()
        print(self)
        print('Raw Product Deleted!')

    def updateRP(self):
        db.session.commit()
