#Build and run service : 
docker-compose up -d 

#GET 
In Postman:
GET https://193.219.91.103:14569/games_instock

#GET by id 
In Postman:
GET https://193.219.91.103:14569/games_instock/<ID (int)>	#By default 1-6

#POST
In Postman:
Need to set up JSON/application, in BODY write new game in JSON format
POST https://193.219.91.103:14569/games_instock

#PUT
In Postman:
PUT https://193.219.91.103:14569/games_instock/<ID (int)>	#By default 1-6
In BODY write JSON file.

#DELETE
In Postman:
DELETE https://193.219.91.103:14569/games_instock/<ID (int)>	#By delault 1-6

#hello()
URL: https://193.219.91.103:14569

