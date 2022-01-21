import json
import string
from flask import Blueprint, request, jsonify

import uuid0 as ID

from models.spaprocess import SPAProcessModel

ProcessProduct = Blueprint('ProcessProduct', __name__)


@ProcessProduct.route('/gapp', methods=['GET'])
def getProcessProduct():
    ProcessProducts = SPAProcessModel.getAllPP()

    data = []
    for a in ProcessProducts:
        if not a.PPDeleted:
            cData = []
            convert = a.PProduct.split('~')
            for cda in convert:
                cData.append(json.loads(cda))
            DataC = {}
            DataC['id'] = a.id
            DataC['PPN'] = a.PPName
            DataC['PPD'] = a.PPDescription
            DataC['PPP'] = a.PPrice
            DataC['PPL'] = cData
            data.append(DataC)

    return {'message': data, 'status': 200}


@ProcessProduct.route('/anpp', methods=['POST'])
def addProcessProduct():
    dataProcessProduct = request.get_json()

    checkExisting = SPAProcessModel.getnamePP(dataProcessProduct['PPN'])
    if checkExisting:

        return{'status': 200, 'message': 'Already submitted for Process', 'code': f'Exe'}
    newPRM = dataProcessProduct['PRM']

    Id = str(ID.generate())
    NewProcessProduct = SPAProcessModel(
        id=Id, PPName=dataProcessProduct['PPN'], PPDescription=dataProcessProduct['PPD'], PProduct=newPRM, PPrice=float(dataProcessProduct['PPP']))
    SPAProcessModel.savePP(NewProcessProduct)

    return{'status': 200, 'message': 'Process Product Saved', 'code': f'Created'}
