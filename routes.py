import time

from pymongo import MongoClient
from bson import json_util,ObjectId
from flask import Flask,request,jsonify

from application import application


host = 'mongodb://gabrielbur:ab12cd34@ds235431.mlab.com:35431/climatedb'
client = MongoClient(host)
db = client.climatedb


@application.route('/climate', methods=['GET'])
def get_all():
    output = []
    query = request.args.get('date')
    
    if query is None:
        result = db.climate.find({})
    else:
        result = db.climate.find({'date':query})

    try:
        for c in result:
            output.append({'id':json_util.dumps(c['_id']),
                           'date':c['date'],
                           'temperature':c['temperature'],
                           'rainfall':c['rainfall']})                       
    except:
        output = "Erro, tente novamente mais tarde"
    finally:
        output = jsonify({'result':output})
        return output

  
@application.route('/climate/<string:id>', methods=['GET'])
def get_by_id(id):  
    try:
        c = db.climate.find_one({'_id':ObjectId(id)})
        if c is not None:
            output = {'id':json_util.dumps(c['_id']),
                      'date':c['date'],
                      'temperature':c['temperature'], 
                      'rainfall':c['rainfall']}
        else:
            output = "Nenhum registro encontrado."
    except:
        output = "Erro, tente novamente mais tarde"
    finally:
        output = jsonify({'result':output})
        return output


@application.route('/climate/predict', methods=['GET'])
def get_predict():
    output = []
    current_date = time.strftime('%d/%m/%Y')
    try:
        for c in db.climate.find({'date':current_date}):
            output.append({'id':json_util.dumps(c['_id']),
                           'date':c['date'],
                           'temperature':c['temperature'], 
                           'rainfall':c['rainfall']})
    except:
        output = "Erro, tente novamente mais tarde"
    finally:
        output = jsonify({'result':output})
        return output


@application.route('/climate', methods=['POST'])
def create_climate():
    try:
        ##get posted climate
        date = request.json['date']
        temperature = request.json['temperature']
        rainfall = request.json['rainfall']

        #parse string to a string-date
        date = time.strptime(date,'%d/%m/%Y')
        date = time.strftime('%d/%m/%Y',date)

        climate = {'date':date,
                   'temperature':temperature, 
                   'rainfall':rainfall}
        #result is the response for climate insertion 
        result = db.climate.insert(climate)
        #seach the new climate, added before
        new_climate = db.climate.find_one({'_id':result})
        
        output = {'id':json_util.dumps(new_climate['_id']),
                  'date':new_climate['date'],
                  'temperature':new_climate['temperature'],
                  'rainfall':new_climate['rainfall']}
    except:
        output = "Erro, tente novamente mais tarde"

    finally:
        output = jsonify({'result':output})
        return output
    


@application.route('/climate/<string:id>', methods=['DELETE'])
def delete_climate(id):
    try:
        output = db.climate.delete_one({'_id':ObjectId(id)})

        if output.deleted_count == 1:
            output = "Registro deletado"
        else:
            output = "Registro não encontrado"
    except:
        output = "Erro, tente novamente mais tarde"
    finally:
        output = jsonify({'result':output})
        return output



