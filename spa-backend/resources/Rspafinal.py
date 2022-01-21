from cmath import log
from typing_extensions import Final
from flask import Blueprint, jsonify, request
import uuid0 as ID
from sqlalchemy import func

from models.spafinal import SPAFinalModel
from models.sparaw import SPARawModel
from models.sparf import SPARFModel


FinalProduct = Blueprint('FinalProduct', __name__)


@FinalProduct.route('/gafp', methods=['GET'])
def getFinalProduct():
    FinalProducts = SPAFinalModel.getAllFP()

    data = []

    for fp in FinalProducts:
        if not fp.FPDeleted:

            Data = {}
            Data['id'] = fp.id
            Data['FPN'] = fp.FPName
            Data['FPD'] = fp.FPDescription
            Ndata = []

            for rp in fp.RawMats:
                ndata = {}

                ndata['RPQ'] = rp.SQuantity
                ndata['RPP'] = rp.rawProd.RPPrice
                ndata['RPN'] = rp.SName
                ndata['RPD'] = rp.SDescription
                ndata['RPW'] = rp.SWeight
                ndata['NRPQ'] = rp.SQuantity
                ndata['id'] = rp.rawP_ID
                ndata['RPC'] = rp.SQuantity * rp.rawProd.RPPrice

                Ndata.append(ndata)

            Data['SRDetails'] = Ndata
            data.append(Data)

        FCostPrice = 0
        for s in Data['SRDetails']:
            FCostPrice += s['RPC']

        Data['FPP'] = FCostPrice

    return{'message': data, 'status': 200}


@FinalProduct.route('/gsfp/<id>', methods=['GET'])
def getSelectedFinalProduct(id):

    FinalProducts = SPAFinalModel.getidFP(id)

    data = []

    fp = FinalProducts
    if not fp.FPDeleted:
        Data = {}
        Data['id'] = fp.id
        Data['FPN'] = fp.FPName
        Data['FPD'] = fp.FPDescription
        Ndata = []
        RSModelData = []
        RModelData = SPARawModel.getAllRP()
        for rp in fp.RawMats:

            RSModelData.append(SPARawModel.getidRP(rp.rawP_ID))
            ndata = {}
            ndata['RPQ'] = rp.rawProd.RPQuantity
            ndata['RPP'] = rp.rawProd.RPPrice
            ndata['RPN'] = rp.SName
            ndata['RPD'] = rp.SDescription
            ndata['RPW'] = rp.SWeight
            ndata['NRPQ'] = rp.SQuantity
            ndata['id'] = rp.rawP_ID
            ndata['RPCost'] = rp.SQuantity * rp.rawProd.RPPrice
            ndata['NewAdd'] = 'False'

            Ndata.append(ndata)

        Data['SRDetails'] = Ndata
        data.append(Data)

        _RProducts = []
        for a in RModelData:
            if a not in RSModelData:
                _RProducts.append(a)
        for b in RSModelData:
            if b not in RModelData:
                _RProducts.append(b)

        Datar = []

        for _RPData in _RProducts:
            if not _RPData.RPDeleted:
                DataR = {}
                DataR['id'] = _RPData.id
                DataR['RPN'] = _RPData.RPName
                DataR['RPD'] = _RPData.RPDescription
                DataR['RPQ'] = _RPData.RPQuantity
                DataR['RPP'] = _RPData.RPPrice
                DataR['RPW'] = _RPData.RPWeight
                DataR['RPCost'] = _RPData.RPQuantity * _RPData.RPPrice
                DataR['NewAdd'] = 'True'
                Datar.append(DataR)

    FCostPrice = 0
    for s in Data['SRDetails']:
        FCostPrice += s['RPCost']

    Data['FPP'] = FCostPrice
    Data['RRP'] = Datar

    return{'message': data, 'status': 200}


@FinalProduct.route('/anfp', methods=['POST'])
def addFileProduct():
    datas = request.get_json()

    Id = str(ID.generate())
    FindProduct = SPAFinalModel.getnameFP(datas['FPN'])
    if FindProduct:
        if FindProduct.FPDeleted:

            return {'message': f'Final Product {FindProduct.FPName} Was Deleted. Click Ok To Recover', 'ststus': 295, 'code': f'Recover|{FindProduct.id}'}

        return {'message': f'Final Product {FindProduct.FPName} is already exists!'}
    NewFinalProduct = SPAFinalModel(
        id=Id, FPName=datas['FPN'], FPDescription=datas['FPD'])
    SPAFinalModel.saveFP(NewFinalProduct)

    for data in datas['FRM']:

        check = SPARawModel.getRP(data['RPN'])

        if check:
            NewAso = SPARFModel(SQuantity=data['NRPQ'], SPrice=data['RPP'],
                                SName=data['RPN'], SDescription=data['RPD'], SWeight=data['RPW'])

            NewAso.rawP_ID = data['id']
            SPARFModel.saveFP(NewAso)

            check.RPQuantity = int(check.RPQuantity) - int(data['NRPQ'])

            SPARawModel.updateRP(SPARawModel)

            NewFinalProduct.RawMats.append(NewAso)
            SPARFModel.updateFP(NewFinalProduct)

    return{'status': 200, 'message': 'Add Final Product Triggred', 'code': f'Created'}


@ FinalProduct.route('/ufp/<id>', methods=['PUT'])
def UpdateFinalProduct(id):

    datas = request.get_json()

    newCheck = SPAFinalModel.getidFP(id)

    newCheck.FPName = datas['FPN']
    newCheck.FPDescription = datas['FPD']

    SPAFinalModel.updateFP(newCheck)

    for oData in datas['ORM']:

        if oData['NewAdd'] == 'False' and oData['Check'] == 'OldProduct':
            check = SPARawModel.getRP(oData['RPN'])
            if check:

                check.RPQuantity = int(check.RPQuantity) + int(oData['NRPQ'])
                SPARawModel.updateRP(SPARawModel)
                _deleteCheck = SPARFModel.getIdRP(oData['id'])
                if _deleteCheck:
                    SPARFModel.deleteFPR(_deleteCheck)
                    SPARFModel.updateFP(SPARFModel)

    for uData in datas['URM']:
        if uData['NewAdd'] == 'False' and uData['Check'] == 'OOldProduct':

            Acheck = SPARawModel.getRP(uData['RPN'])

            if Acheck:
                ANewAso = SPARFModel(SQuantity=uData['NRPQ'], SPrice=uData['RPP'],
                                     SName=uData['RPN'], SDescription=uData['RPD'], SWeight=uData['RPW'])

                ANewAso.rawP_ID = uData['id']
                SPARFModel.saveFP(ANewAso)

                NAcheck = SPARawModel.getRP(uData['RPN'])
                if NAcheck:
                    NAcheck.RPQuantity = int(
                        NAcheck.RPQuantity) - int(uData['NRPQ'])

                    SPARawModel.updateRP(SPARawModel)

                newCheck.RawMats.append(ANewAso)

                SPARFModel.updateFP(newCheck)
    for nData in datas['NRM']:
        if nData['NewAdd'] == 'True' and nData['Check'] == 'NewProduct':

            Acheck = SPARawModel.getRP(nData['RPN'])

            if Acheck:
                ANewAso = SPARFModel(SQuantity=nData['NRPQ'], SPrice=nData['RPP'],
                                     SName=nData['RPN'], SDescription=nData['RPD'], SWeight=nData['RPW'])

                ANewAso.rawP_ID = nData['id']
                SPARFModel.saveFP(ANewAso)

                NAcheck = SPARawModel.getRP(nData['RPN'])
                if NAcheck:
                    NAcheck.RPQuantity = int(
                        NAcheck.RPQuantity) - int(nData['NRPQ'])

                    SPARawModel.updateRP(SPARawModel)

                newCheck.RawMats.append(ANewAso)

                SPARFModel.updateFP(newCheck)
    return {'message': 'Trying to Update', 'status': 201}


@ FinalProduct.route('/dfp/<id>', methods=['PUT'])
def deleteFinalProduct(id):

    newCheck = SPAFinalModel.getidFP(id)

    newCheck.FPDeleted = True

    for add in newCheck.RawMats:
        getRawMaterials = SPARawModel.getidRP(add.rawP_ID)
        if getRawMaterials:
            oneCheck = int(getRawMaterials.RPQuantity) + int(add.SQuantity)
            getRawMaterials.RPQuantity = oneCheck
            SPARawModel.updateRP(SPARawModel)
    SPAFinalModel.updateFP(SPAFinalModel)

    return {'message': 'Trying to Delete', 'status': 201}
