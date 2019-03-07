from flask import Flask, jsonify, abort, request
from redis import Redis
from flask import make_response
import os 
import re 

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

#Info about games in stock
@app.route('/games_instock',methods=['GET'])
def getGames():
	if(request.args.get('Name','')):
		games = []
		for i in games_instock:
			if(re.search(request.args.get('Name',''), i["Name"], re.IGNORECASE)):
				games.append(i)
		return jsonify(games)
	else:
		return jsonify(games_instock),200

#Dealing with 404
@app.errorhandler(404)
def notFound(error):
	return make_response(jsonify({'error': 'Not Found'}), 404)

#Delete game
@app.route('/games_instock/<int:game_id>', methods=['DELETE'])
def deleteGame(game_id):
	game = [game for game in games_instock if game['ID'] == game_id]
	games_instock.remove(game[0])
	return jsonfy(True),200

#Add new game 
@app.route('/games_instock', methods=['POST'])
def addNewGame():
	if not request.json:
		abort(400)
	game={
		'ID': games_instock[-1]['ID'] +1,
		'Name': request.json['Name'],
		'Developer': request.json['Developer'],
		'Publisher': request.json['Publisher']
	}
	games_instock.append(game)
	return jsonfy(game),201,{'Location':'/games_instock/'+str(games_instock[-1]['ID'])}

#Modifie game attributes
@app.route('/games_instock/<int:game_id>', methods=['PUT'])
def modGame(game_id):
	game = [game for game in games_instock if game['ID'] == game_id]
	if 'Name' in request.json:
		game[0]['Name'] = request.json['Name']
	if 'Developer' in request.json:
		game[0]['Developer'] = request.json['Developer']
	if 'Publisher' in request.json:
		game[0]['Publisher'] = request.json['Publisher']
	return jsonify({'game':game[0]})


if __name__== "__main__":
	app.run(host="0.0.0.0", debug=True)
