from flask import Blueprint, request, jsonify

import uuid0 as ID

from models.sparaw import SPARawModel

RawProduct = Blueprint('RawProduct', __name__)


@RawProduct.route('/garp', methods=['GET'])
def getRawProduct():
    RawProducts = SPARawModel.getAllRP()
    data = []
    for a in RawProducts:
        if not a.RPDeleted:
            DataC = {}
            DataC['id'] = a.id
            DataC['RPN'] = a.RPName
            DataC['RPD'] = a.RPDescription
            DataC['RPQ'] = a.RPQuantity
            DataC['RPP'] = a.RPPrice
            DataC['RPW'] = a.RPWeight
            DataC['RPCost'] = a.RPQuantity * a.RPPrice
            data.append(DataC)
    return {'message': data, 'status': 200}


@RawProduct.route('/anrp', methods=['POST'])
def addRawProduct():
    dataRawProduct = request.get_json()

    Id = str(ID.generate())
    FindRawProduct = SPARawModel.getRP(dataRawProduct['RPN'])
    if FindRawProduct:
        if FindRawProduct.RPDeleted:

            return {'message': f'Raw Product {FindRawProduct.RPName} Was Deleted. Click Ok To Recover', 'ststus': 295, 'code': f'Recover|{FindRawProduct.id}'}

        return {'message': f'Raw Product {FindRawProduct.RPName} is already exists!'}

    NewRawProduct = SPARawModel(id=Id, RPName=dataRawProduct['RPN'], RPDescription=dataRawProduct['RPD'],
                                RPQuantity=dataRawProduct['RPQ'], RPPrice=dataRawProduct['RPP'], RPWeight=dataRawProduct['RPW'])
    SPARawModel.saveRP(NewRawProduct, dataRawProduct['RPN'])

    return{'status': 200, 'message': 'Raw Product Saved', 'code': f'Created'}


@RawProduct.route('/drp/<id>', methods=['PUT'])
def deleteRawProduct(id):
    RawProductDelete = SPARawModel.getidRP(id)
    RawProductDelete.RPDeleted = True
    SPARawModel.updateRP(RawProductDelete)
    return {'message': 'Raw Product Successfuly deleted', 'status': 200}


@RawProduct.route('/rrp/<id>', methods=['PUT'])
def recoverRawProduct(id):
    RawProductDelete = SPARawModel.getidRP(id)
    RawProductDelete.RPDeleted = False
    SPARawModel.updateRP(RawProductDelete)
    return {'message': 'Raw Product Successfuly Recovered', 'status': 200}


@RawProduct.route('/urp/<id>', methods=['PUT'])
def updateRawProduct(id):
    dataRawProduct = request.get_json()

    RawProductUpdate = SPARawModel.getidRP(id)

    RawProductUpdate.RPName = dataRawProduct['RPN']
    RawProductUpdate.RPDescription = dataRawProduct['RPD']
    RawProductUpdate.RPQuantity = dataRawProduct['RPQ']
    RawProductUpdate.RPPrice = dataRawProduct['RPP']
    RawProductUpdate.RPWeight = dataRawProduct['RPW']

    SPARawModel.updateRP(SPARawModel)
    return {'message': 'Raw Product Successfuly Updated', 'status': 200}
