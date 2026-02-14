#!/usr/bin/env python3
from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB API', description='Test API')

@api.route('/test')
class Test(Resource):
    def get(self):
        return {'message': 'API is working'}

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    print("Test endpoint: http://localhost:5000/test")
    app.run(debug=True, host='0.0.0.0', port=5000)
