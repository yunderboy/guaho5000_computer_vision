from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from inverse_kinematics import control

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

stepper = control.Stepper('4', 63.209, -36.941, 0)


@app.route('/coordinates', methods=['GET', 'POST'])
def get_coordinates():

    if request.method == 'POST':
        print('Received POST request')
        coords = request.get_json()
        print([coords['x'], coords['y'], coords['z']])
        #stepper.main([float(coords['x']), float(coords['y']), float(coords['z'])])
        stepper.main([0.0, 12.0, 12.0])
    else:
        print('Received GET request')

    return 'noice'

if __name__ == '__main__':
    app.run()