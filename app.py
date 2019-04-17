#!/usr/bin/env python
from flask import Flask, jsonify, abort, request
import os
import copy
import json
import re
import requests
app = Flask(__name__)
games_instock = [
	{
		'ID': 1,
		'Name': 'Assassin\'s Creed 3 ',
		'Developer': 'Ubisoft Montreal',
		'Publisher': 'Ubisoft',
		'Car': '1'
	},
	{
		'ID': 2,
		'Name': 'Need for Speed',
		'Developer': 'Ghost Games',
		'Publisher': 'Electronic Arts',
		'Car': '2'
	},
	{
		'ID': 3,
		'Name': 'Call of Duty: WWII',
		'Developer': 'Sledgehammer Games',
		'Publisher': 'Activision Blizzard',
		'Car': '3'
	},
	{
		'ID': 4,
		'Name': 'Wolfenstein II: The New Colossus',
		'Developer': 'MachineGames',
		'Publisher': 'Bethesda Softworks',
		'Car': '1'
	},
	{
		'ID': 5,
		'Name': 'Cyberpunk 2077',
		'Developer': 'CD Projekt Red',
		'Publisher': 'CD Projekt',
		'Car': '1'
	},
	{
		'ID': 6,
		'Name': 'Titanfall 2',
		'Developer': 'Respawn Entertainment',
		'Publisher': 'Electronic Arts',
		'Car': '1'
	}
]

#Hello function (introducing)
@app.route('/')
def hello():
	#redis.incr('counter')
	return 'Hello. This service provides information about games in stock.'

#Info about games in stock by ID
@app.route('/games_instock/<int:game_id>', methods=['GET'])
def getGame(game_id):
	if( request.args.get('embedded','') == "car"):
			embGames = copy.deepcopy(games_instock)
			try:
				req = requests.get('http://web2:81/cars/'+embGames[int(game_id)]['Car'])
				req = json.loads(req.text)
				embGames[int(game_id)]['Car'] = req
			except request.exceptions.RequestException as e:
				embGames[int(game_id)]['Car'] = 'null'
			return jsonify(embGames[int(game_id)]),200
	else:
		game = [gametmp for gametmp in games_instock if (gametmp['ID'] == game_id)]
		if(game):
			return jsonify(game),200
		else:
			return "Not found ID!",404

#Info about games in stock
@app.route('/games_instock',methods=['GET'])
def getGames():
	if( request.args.get('embedded','') == "car"):
			embGames = copy.deepcopy(games_instock)
			for i in range(0,len(games_instock)):
				try:
					req = requests.get('http://web2:81/cars/'+embGames[i]['Car'])
					req = json.loads(req.text)
					embGames[int(i)]['Car'] = req
				except request.exceptions.RequestException as e:
					embGames[i]['Car'] = 'null'
			return jsonify(embGames),200
	else:
		return jsonify({'Games':games_instock}),200

#Delete game
@app.route('/games_instock/<int:game_id>', methods=['DELETE'])
def deleteGame(game_id):
	game = [game for game in games_instock if game['ID'] == game_id]
	games_instock.remove(game[0])
	return getGames(),200

#Add new game
@app.route('/games_instock', methods=['POST'])
def addNewGame():
	if not request.json:
		abort(400)
	if(request.args.get('embedded','') == 'car'):
		car = request.json['Car']
		#req = requests.post('http://web2:81/cars',json = {"vin":car['vin'],"brand":car['brand'],"model":car['model'],"year":car['year'],"fuel_type":car['fuel_type'],"engine_volume":car["engine_volume"],"trim":car['trim'],"price":car['price'],"owner":car['owner']})
		req = requests.post('http://web2:81/cars',json = {"brand":car['brand'],"model":car['model']})
		req = json.loads(req.text)
		if 'Name' in request.json and 'Developer' in request.json and 'Publisher' in request.json:
			game={
				'ID': games_instock[-1]['ID'] +1,
				'Name': request.json['Name'],
				'Developer': request.json['Developer'],
				'Publisher': request.json['Publisher'],
				'Car':req['id']
			}
			games_instock.append(game)
			return jsonify(game),201
		else:
			return "Bad JSON request",400
	else:
		if 'Name' in request.json and 'Developer' in request.json and 'Publisher' in request.json:
			game={
				'ID': games_instock[-1]['ID'] +1,
				'Name': request.json['Name'],
				'Developer': request.json['Developer'],
				'Publisher': request.json['Publisher'],
				'Car': request.json['Car']
			}
			games_instock.append(game)
			return jsonify(game),201
		else:
			return "Bad JSON request",400
#Patching game
@app.route('/games_instock/<int:game_id>', methods=['PATCH'])
def patGame(game_id):
	game= [game for game in games_instock if game['ID'] == game_id]
	if(game):
		if 'Name' in request.json:
			game[0]['Name'] = request.json['Name']
		if 'Developer' in request.json:
			game[0]['Developer'] = request.json['Developer']
		if 'Publisher' in request.json:
			game[0]['Publisher'] = request.json['Publisher']
		return jsonify({'Modified': game[0]}),200
	else:
		return "Bad ID",404

#Modifie game attributes
@app.route('/games_instock/<int:game_id>', methods=['PUT'])
def modGame(game_id):
	game = [game for game in games_instock if game['ID'] == game_id]
	if(game):
		if 'Name' in request.json:
			game[0]['Name'] = request.json['Name']
		else:
			game[0].pop('Name',None)
		if 'Developer' in request.json:
			game[0]['Developer'] = request.json['Developer']
		else:
			game[0].pop('Developer',None)
		if 'Publisher' in request.json:
			game[0]['Publisher'] = request.json['Publisher']
		else:
			game[0].pop('Publisher',None)
		if 'Car' in request.json:
			game[0]['Car'] = request.json['Car']
		else:
			game[0].pop('Car',None)
		return jsonify({'Modified':game[0]}),200
	else:
		return "Not found",404

#Modifie info
@app.route('/games_instock/<int:game_id>/car',methods=['PUT'])
def modInfo(game_id):
	req = request.put('http://web2:81/cars/'+games_instock[int(game_id)]['Car'],json = {"id":request.json.get('id',1),"vin":request.json['vin'],"brand":request.json['brand'],"model":request.json['model'],"year":request.json['year'],"fuel_type":request.json['fuel_type'],"engine_volume":request.json["engine_volume"],"trim":request.json['trim'],"price":request.json['price'],"owner":request.json['owner']})
	req = json.loads(req.text)
	return jsonify(req),200

if __name__== "__main__":
	app.run(host="0.0.0.0", debug=True)
