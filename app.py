from flask import Flask, jsonify, abort, request
from redis import Redis
import os  

app = Flask(__name__)
redis = Redis(host='redis', port =6379)

games_instock = [
	{
		'ID': 1,
		'Name': 'Assassin\'s Creed 3 ',
		'Developer': 'Ubisoft Montreal',
		'Publisher': 'Ubisoft'
	},
	{
		'ID': 2,
		'Name': 'Need for Speed',
		'Developer': 'Ghost Games',
		'Publisher': 'Electronic Arts'
	},
	{
		'ID': 3,
		'Name': 'Call of Duty: WWII',
		'Developer': 'Sledgehammer Games',
		'Publisher': 'Activision Blizzard'
	},
	{
		'ID': 4,
		'Name': 'Wolfenstein II: The New Colossus',
		'Developer': 'MachineGames',
		'Publisher': 'Bethesda Softworks'
	},
	{
		'ID': 5,
		'Name': 'Cyberpunk 2077',
		'Developer': 'CD Projekt Red',
		'Publisher': 'CD Projekt'
	},
	{
		'ID': 6,
		'Name': 'Titanfall 2',
		'Developer': 'Respawn Entertainment',
		'Publisher': 'Electronic Arts'
	}
]

#Hello function (introducing)
@app.route('/')
def hello():
	redis.incr('counter')
	return 'Hello. This service provides information about games in stock. We see you %s time.' %redis.get('counter')

#Info about games in stock by ID
@app.route('/games_instock/<int:game_id>', methods=['GET'])
def getGame(game_id):
	game = [gametmp for gametmp in games_instock if (gametmp['ID'] == game_id)]
	if(game):
		return jsonify(game)
	else:
		return 404,"Not found ID!"

#Info about games in stock
@app.route('/games_instock',methods=['GET'])
def getGames():
	return jsonify({'Games':games_instock})

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
	if 'Name' in request.json and 'Developer' in request.json and 'Publisher' in request.json:
		game={
			'ID': games_instock[-1]['ID'] +1,
			'Name': request.json['Name'],
			'Developer': request.json['Developer'],
			'Publisher': request.json['Publisher']
		}
		games_instock.append(game)
		return getGame(games_instock[-1]['ID']),201
	else:
		return "Bad JSON request",400

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
		return jsonify({'Modified':game[0]}),200
	else:
		return 404,"Not found"


if __name__== "__main__":
	app.run(host="0.0.0.0", debug=True)
