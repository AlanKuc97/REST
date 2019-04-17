#!/usr/bin/env python

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

Cars=[
 {
	'id':1,
	'vin':'WDB2093161F037877',
	'brand':'Mercedes',
	'model':'CLS',
	'year':'2013',
	'fuel_type':'Benzinas',
	'engine_volume':'3.0',
	'trim':'Elegance',
	'price':'38000.00',
	'owner':1
 },
 {
	'id':2,
	'vin':'WBA2093161F036479',
	'brand':'BMW',
	'model':'525D',
	'year':'2016',
	'fuel_type':'Dyzelinas',
	'engine_volume':'2.0',
	'trim':'Individual',
	'price':'40000.00',
	'owner':2
 },
 { 
	'id':3,
	'vin':'WDB2093161F066497',
	'brand':'Mercedes',
	'model':'CLK',
	'year':'2011',
	'fuel_type':'Dyzelinas',
	'engine_volume':'3.0',
	'trim':'Avantgarde',
	'price':'25000.00',
	'owner':3
 },
 { 
	'id':4,
	'vin':'WAUZZZ3161F037877',
	'brand':'Audi',
	'model':'A6',
	'year':'2010',
	'fuel_type':'Dyzelinas',
	'engine_volume':'3.0',
	'trim':'S-Line',
	'price':'15000.00',
	'owner':4
 }
 ]

Owners=[
 {
	'id':1,
	'ak':'35905113465',
	'name':'Jonas',
	'surname':'Jonaitis',
	'address':'Naugarduko g. 24, Vilnius',
	'ownedCar':1
 },
 {
	'id':2,
	'ak':'48308118765',
	'name':'Egle',
	'surname':'Eglaite',
	'address':'Fabijoniskiu g. 115, Vilnius',
	'ownedCar':2
 },
 {
	'id':3,
	'ak':'35911256865',
	'name':'Petras',
	'surname':'Petraitis',
	'address':'Vilniaus g. 58, Panevezys',
	'ownedCar':3
 },
 {
	'id':4,
	'ak':'47803259665',
	'name':'Greta',
	'surname':'Gretaite',
	'address':'Taikos pr. 234, Klaipeda',
	'ownedCar':4
 }
 ]

#Car functions:

@app.route('/cars', methods=['GET'])
def getAllCars():

	c1 = 0
	c2 = 0
		
	model = request.args.get("model")
	brand = request.args.get("brand")
	
	if(model):
		c1 = [ car for car in Cars if (car['model'] == model) ]
		return jsonify(c1)
	elif(brand):
		c2 = [ car for car in Cars if (car['brand'] == brand) ]
		return jsonify(c2)
	elif not request.args:		 
		return jsonify({'cars':Cars})
	else:
		return "Bad request",400

@app.route('/cars/<int:carId>',methods=['GET'])
def getCar(carId):
	
	usr = [ car for car in Cars if (car['id'] == carId) ]

	if(usr):
		return jsonify(usr)
	else:
		return "No car with Id %s found" %carId, 404


@app.route('/cars/<int:carID>/owners')
def getCarOwner(carID):
        c = [ car for car in Cars if (car['id'] == carID) ]
        id = c[0]['owner']

	if(c):
        	return getOwner(id)
	else:
		return 'No owner found',404

@app.route('/cars/<int:carId>',methods=['PUT'])
def updateCar(carId):

  	c = [ car for car in Cars if (car['id'] == carId) ]
        
	if(c):
		if 'vin' in request.json:
			c[0]['vin'] = request.json['vin']
		else:
			c[0].pop('vin', None)
    		if 'brand' in request.json: 
	 		c[0]['brand'] = request.json['brand']		
		else:
			return "No brand given",400
    		if 'model' in request.json:
			c[0]['model'] = request.json['model']
		else:	
	 		return "No model given",400	
		if 'year' in request.json:
			c[0]['year'] = request.json['year']
		else:	
			c[0].pop('year',None)
		if 'fuel_type' in request.json:
                	c[0]['fuel_type'] = request.json['fuel_type']
		else:
			c[0].pop('fuel_type',None)
        	if 'engine_volume' in request.json:
                	c[0]['engine_volume'] = request.json['engine_volume']
		else:
			c[0].pop('engine_volume',None)
        	if 'trim' in request.json:
                	c[0]['trim'] = request.json['trim']
		else:
			c[0].pop('trim',None)
        	if 'price' in request.json:
                	c[0]['price'] = request.json['price']
		else:
			c[0].pop('price',None)
		if 'owner' in request.json:
			c[0]['owner'] = request.json['owner']	
		else:
			c[0].pop('owner',None)
		return jsonify(c),201	
	else:
		return 'No car with Id %s found' %carId,404


@app.route('/cars/<int:carId>',methods=['PATCH'])
def patchCar(carId):

        c = [ car for car in Cars if (car['id'] == carId) ]

	if(c):	

		if 'vin' in request.json:
			c[0]['vin'] = request.json['vin']
        	if 'brand' in request.json :
                	c[0]['brand'] = request.json['brand']
       		if 'model' in request.json:
                	c[0]['model'] = request.json['model']
		if 'year' in request.json:
			c[0]['year'] = request.json['year']
		if 'fuel_type' in request.json:
			c[0]['fuel_type'] = request.json['fuel_type']
		if 'engine_volume' in request.json:
			c[0]['engine_volume'] = request.json['engine_volume']
        	if 'trim' in request.json :
                	c[0]['trim'] = request.json['trim']
       		if 'price' in request.json:
                	c[0]['price'] = request.json['price']
		if 'owner' in request.json:
			c[0]['owner'] = request.json['owner']

        	return jsonify({'owner':c[0]})
	else:
		return 'No car with Id %s found' %carId, 404

@app.route('/cars',methods=['POST'])
def createCar():
	
	data = request.get_json()

    if 'brand' in request.json :
        data['brand'] = request.json['brand']
	else:
		return "No Brand given", 400
    if 'model' in request.json:
        data['model'] = request.json['model']
	else:
		return "No model given", 400

	data['id'] = Cars[-1]['id']+1

    Cars.append(data)
    return jsonify(data),201

@app.route('/cars/<int:carId>',methods=['DELETE'])
def deleteCar(carId):
    	c = [ car for car in Cars if (car['id'] == carId) ]
	
        if(c):
		Cars.remove(c[0])
        	return jsonify({'response':'Success'})
	else:
		return 'No car with Id %s found' %carId,404

@app.route('/owners', methods=['GET'])
def getAllOwners():

	o1 = 0
	o2 = 0
		
	name = request.args.get("name")
	surname = request.args.get("surname")
	
	if(name):
		o1 = [ owner for owner in Owners if (owner['name'] == name) ]
		return jsonify(o1)
	elif(surname):
		o2 = [ owner for owner in Owners if (owner['surname'] == surname) ]
		return jsonify(o2)
	elif not request.args:		 
		return jsonify({'owners':Owners})
	else:
		return "Bad request", 404

@app.route('/owners/<int:ownerId>',methods=['GET'])
def getOwner(ownerId):
        usr = [ owner for owner in Owners if (owner['id'] == ownerId) ]
	if(usr):
        	return jsonify({'owner':usr})
	else:
		return 'No owner with Id %s found' %ownerId, 404

@app.route('/owners/<int:ownerID>/cars')
def getOwnedCar(ownerID):
	o = [ owner for owner in Owners if (owner['id'] == ownerID) ]
	id = o[0]['ownedCar']
	return getCar(id)


@app.route('/owners/<int:ownerId>',methods=['PUT'])
def updateOwner(ownerId):

  	o = [ owner for owner in Owners if (owner['id'] == ownerId) ]
        
	if(o):
		if 'ak' in request.json:
			o[0]['ak'] = request.json['ak']
		else:
			o[0].pop('ak', None)
    		if 'name' in request.json: 
	 		o[0]['name'] = request.json['name']		
		else:
			return "No name given", 400
    		if 'surname' in request.json:
			o[0]['surname'] = request.json['surname']
		else:	
	 		return "No surname given",400		
		if 'address' in request.json:
			o[0]['address'] = request.json['address']
		else:	
			o[0].pop('address',None)
		if 'ownedCar' in request.json:
                	o[0]['ownedCar'] = request.json['ownedCar']
		else:
			o[0].pop('ownedCar',None)
	 
		return jsonify(o),201	
	else:
		return 'No owner with Id %s found' %ownerId,404
	
@app.route('/owners/<int:ownerId>',methods=['PATCH'])
def patchOwner(ownerId):

        o = [ owner for owner in Owners if (owner['id'] == ownerId) ]

	if(o):	

		if 'ak' in request.json:
			o[0]['ak'] = request.json['ak']
        	if 'name' in request.json :
                	o[0]['name'] = request.json['name']
       		if 'surname' in request.json:
                	o[0]['surname'] = request.json['surname']
		if 'address' in request.json:
			o[0]['address'] = request.json['address']
		if 'owner' in request.json:
			o[0]['owner'] = request.json['owner']

        	return jsonify({'owner':o[0]}),201
	else:
		return 'No owner with Id %s found' %ownerId, 404

@app.route('/owners',methods=['POST'])
def createOwner():

	data = request.get_json()
	data['id'] = Owners[-1]['id']+1

	
        if 'name' in request.json :
               	data['name'] = request.json['name']
	else:
		return "No name given", 400
       	if 'surname' in request.json:
               	data['surname'] = request.json['surname']
	else:
		return "No surname given", 400

        Owners.append(data)
        return jsonify(data),201

@app.route('/owners/<int:ownerId>',methods=['DELETE'])
def deleteOwner(ownerId):
        o = [ owner for owner in Owners if (owner['id'] == ownerId) ]

        if(o):
		Owners.remove(o[0])
        	return jsonify({'response':'Success'})
	else:
		return 'No owner with Id %s found' %ownerId,404

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=81)
