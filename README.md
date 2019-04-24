#Build and run service : 
docker-compose up -d 

#hello()
URL: https://193.219.91.103:14569

###1 task

#GET 
In Postman:
GET 193.219.91.103:14569/games_instock

#GET by id 
In Postman:
GET 193.219.91.103:14569/games_instock/<ID (int)>	#By default 1-6

#POST
In Postman:
Need to set up JSON/application, in BODY write new game in JSON format
POST 193.219.91.103:14569/games_instock

#PUT
In Postman:
PUT 193.219.91.103:14569/games_instock/<ID (int)>	#By default 1-6
In BODY write JSON file.

#DELETE
In Postman:
DELETE 193.219.91.103:14569/games_instock/<ID (int)>	#By delault 1-6

###2 task

#GET 
In Postman:
GET 193.219.91.103:14569/games_instock?embedded=car

#GET by id 
In Postman:
GET 193.219.91.103:14569/games_instock/<INT ID>?embedded=car	#By default 0-5

#POST
In Postman:
Need to set up JSON/application, in BODY write new game in JSON format:
{
    "Name": "Assassins Creed 3",
    "Developer": "Ubisoft Montreal",
    "Publisher": "Ubisoft",
    "Car":{
        "vin":"WAUZZZ3161F037877",
        "brand":"Audi",
        "model":"A6",
        "year":"2010",
        "fuel_type":"Dyzelinas",
        "engine_volume":"3.0",
        "trim":"S-Line",
        "price":"15000.00"
    }
}
POST 193.219.91.103:14569/games_instock

#PUT
In Postman:
Need to set up JSON/application, in BODY write new game in JSON format:
{
    "Name": "Assassins Creed 3",
    "Developer": "Ubisoft Montreal",
    "Publisher": "Ubisoft",
    "Car": "3"
}
PUT 193.219.91.103:14569/games_instock/1

#PUT to change car
In Postman:
Need to set up JSON/application, in BODY write new game in JSON format:
{
    "vin":"WDB2093161F037877",
    "brand":"Mercedes",
    "model":"CLS",
    "year":"2013",
    "fuel_type":"Benzinas",
    "engine_volume":"3.0",
    "trim":"Elegance",
    "price":"38000.00"
}
PUT 193.219.91.103:14569/games_instock/2/car #By default 1-5
