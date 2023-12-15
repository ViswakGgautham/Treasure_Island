import random
import mysql.connector as mysql
from flask import Flask
from flask_cors import CORS

con=mysql.connect(host='localhost', user='root',password='password',database='flight_game')
cursor=con.cursor()


app = Flask(__name__)
CORS(app)
sum = 0
sum2 = 0
sum3 = 1000
@app.route('/gold', methods=['GET','POST'])
def gold():
    global sum, sum2, sum3
    gold = random.randint(1,20)
    sum = sum + gold
    used = random.randint(1,10)
    sum2 = sum2 + used
    sum3 = sum3 - used
    d = {'gold': sum, 'new':gold, 'used':sum2, 'remaining':sum3}
    return d

if __name__ == '__main__':
    app.run(debug=True)
