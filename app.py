from flask import Flask, jsonify, abort, request
from redis import Redis
from flask import make_response
import os 
import re 

app = Flask(__name__)
redis = Redis(host='redis', port =5000)

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

