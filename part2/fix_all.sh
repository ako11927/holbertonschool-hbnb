#!/bin/bash
echo "=== Fixing All Issues ==="

echo "1. Updating werkzeug to compatible version..."
pip3 install --upgrade werkzeug==2.3.0 Flask==2.3.3 flask-restx==1.1.0

echo -e "\n2. Checking dependencies..."
pip3 list | grep -E "Flask|werkzeug|flask-restx"

echo -e "\n3. Fixing user.py duplicate imports..."
# Remove the duplicate line at top of user.py
sed -i '/^from typing import Dict, Any, Optional, List/{N;/^from typing import Dict, Any, Optional, List\nfrom typing import/d}' business_logic/models/user.py

echo -e "\n4. Testing imports..."
python3 -c "
try:
    from werkzeug import __version__ as werkzeug_version
    print(f'✅ werkzeug version: {werkzeug_version}')
    
    from flask import Flask
    print('✅ Flask imports')
    
    from flask_restx import Api
    print('✅ flask-restx imports')
    
    from app import create_app
    print('✅ App imports')
    
    from business_logic.models.user import User
    user = User(email='test@test.com', password='123456')
    print(f'✅ User created: {user.id}')
    
    print('\n✅ ALL IMPORTS SUCCESSFUL')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
"
