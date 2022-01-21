from db import db

from models.spafinal import *
from models.sparaw import *


class SPARFModel(db.Model):
    __tablename__ = 'sparf'
    id1 = db.Column(db.Integer, primary_key=True)
    finalP_ID = db.Column(db.String, db.ForeignKey('spafinallist.id'))
    rawP_ID = db.Column(db.String, db.ForeignKey('sparawlist.id'))
    SQuantity = db.Column(db.Integer)
    SPrice = db.Column(db.Float)
    # SName = db.Column(db.String(256), unique=True)
    SName = db.Column(db.String(256))
    SDescription = db.Column(
        db.String(1024))
    SWeight = db.Column(db.String(128))
    rawProd = db.relationship(
        'SPARawModel', backref=db.backref('rawMaterials'))
    finalProd = db.relationship(
        'SPAFinalModel', backref=db.backref('FinalProducts'))

    def __init__(self, SQuantity, SPrice, SName, SDescription, SWeight):
        self.id = id
        self.SQuantity = SQuantity
        self.SPrice = SPrice
        self.SName = SName
        self.SDescription = SDescription
        self.SWeight = SWeight

    @classmethod
    def getAllFP(cls):
        return cls.query.all()

    @classmethod
    def getIdFP(cls, _id):
        return cls.query.filter_by(finalP_ID=_id).first()

    @classmethod
    def getIdRP(cls, _id):
        return cls.query.filter_by(rawP_ID=_id).first()

    def saveFP(self):
        db.session.add(self)
        db.session.commit()
        print('Asso Table Added')

    def updateFP(self):
        db.session.commit()
        print('Asso Table Updated!')

    def deleteFPR(self):
        db.session.delete(self)
        db.session.commit()
        print('Final Product Deleted is Deleting')
