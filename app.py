import json
import os
import random
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

import config
from game import Game

load_dotenv()

app = Flask(__name__)
# lisätty cors
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Tietokantayhteys
config.conn = mysql.connector.connect(host='localhost', user='root',password='password',database='flight_game')
sum = 0
sum2 = 0
sum3 = 1000
@app.route('/gold', methods=['GET','POST'])
def gold():
    global sum, sum2, sum3
    gold = random.randint(100,110)
    sum = sum + gold
    used = random.randint(100,200)
    sum2 = sum2 + used
    sum3 = sum3 - used
    d = {'gold': sum, 'new':gold, 'used':sum2, 'remaining':sum3}
    return d


def fly(id, dest, consumption=0, player=None):
    if id==0:
        game = Game(0, dest, consumption, player)
    else:
        game = Game(id, dest, consumption)
    game.location[0].fetchWeather(game)
    nearby = game.location[0].find_nearby_airports()
    for a in nearby:
        game.location.append(a)
    json_data = json.dumps(game, default=lambda o: o.__dict__, indent=4)
    return json_data


# http://127.0.0.1:5000/flyto?game=fEC7n0loeL95awIxgY7M&dest=EFHK&consumption=123
@app.route('/flyto')
def flyto():
    args = request.args
    id = args.get("game")
    dest = args.get("dest")
    consumption = args.get("consumption")
    json_data = fly(id, dest, consumption)
    print("*** Called flyto endpoint ***")
    return json_data


# http://127.0.0.1:5000/newgame?player=Vesa&loc=EFHK
@app.route('/newgame')
def newgame():
    args = request.args
    player = args.get("player")
    dest = args.get("loc")
    json_data = fly(0, dest, 0, player)
    return json_data

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
