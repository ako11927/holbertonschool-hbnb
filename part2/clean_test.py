#!/usr/bin/env python3
"""Clean test without any cross-reference issues."""
from flask import Flask
from flask_restx import Api, Resource

# Create minimal app
app = Flask(__name__)
api = Api(app)

@api.route('/test')
class Test(Resource):
    def get(self):
        return {'test': 'OK'}

if __name__ == '__main__':
    print("✅ Basic Flask-RESTx setup works")
    
    # Test with test client
    with app.test_client() as client:
        resp = client.get('/test')
        print(f"✅ Test endpoint: {resp.status_code}")
        print(f"Data: {resp.get_json()}")
