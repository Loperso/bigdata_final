from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = {}
@app.route('/', methods=['POST'])
def receive_data():
    time = request.form['time']
    min = request.form['min']
    max = request.form['max']
    avg = request.form['avg']

    print('Recibido ', time, min, max, avg)
    data[time] = {'time': time, 'min': min, 'max': max, 'avg': avg}
    print(data)
    return 'Dato recibido'

@app.route('/dashboard')
def dashboard():
    return  data

app.run()

