Crypto Alpha v1
================================
Identifies High Potential Cryptocurrency Investments

Dependencies:
-------------

Python-Binance:
https://github.com/sammchardy/python-binance

Python Flask:
http://flask.pocoo.org/

MongoDB:
https://api.mongodb.com/python/current/

Authentication:
---------------

1. Put a .authentication file in root project directory
2. Add info to it in following way:

	    key: <your key here>
	
	    secret: <your secret here>
	
	    twilio_sid:ACcc841ff7e8536aa6b59305da39850fe6

       auth_token:c13a9010670a559a3a08f81dc9362f79


Initializing MongoDB:
--------------------
On Max OS:

   Installing Mongo DB With Brew:
   
    $ brew install mongodb
            
   Starting MongoDB:
   
    $ brew services start mongodb
    
   Populating Database:
   	
   In main.py, make sure that the first paramater is set to true if you want to populate your database. After 
   it is populated switch it to false. It will take around 12 times the period you specify in hours to populate fully.
	
	mw = MarketWatch(repopulate=True, period=.5)
