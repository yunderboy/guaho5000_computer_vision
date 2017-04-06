from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/coordinates', methods=['GET', 'POST'])
def get_coordinates():

    if request.method == 'POST':
        print('Received POST request')
        coords = request.get_json()
        print(coords)
        return coords

    else:
        print('Received GET request')

    return '200'

if __name__ == '__main__':
    app.run()