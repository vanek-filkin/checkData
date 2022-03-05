from flask import Flask
from flask_restful import Api
from check_data import CheckData
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

api.add_resource(CheckData, '/check')

if __name__ == '__main__':
    app.run()
