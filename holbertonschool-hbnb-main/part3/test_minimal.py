#!/usr/bin/env python3
from app import create_app

app = create_app()
print("✅ App created successfully")

with app.test_client() as client:
    response = client.get('/api/v1/status')
    print(f"✅ Status endpoint: {response.status_code}")
    print(f"Response: {response.get_json()}")
