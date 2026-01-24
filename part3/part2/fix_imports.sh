#!/bin/bash
echo "=== Fixing Import Issues ==="

# Install dependencies
echo "1. Installing dependencies..."
pip3 install Flask flask-restx python-dotenv

# Fix typing imports
echo -e "\n2. Fixing typing imports..."
for file in business_logic/models/*.py; do
    echo "Checking $file"
    if ! grep -q "^from typing import" "$file" && ! grep -q "^import typing" "$file"; then
        sed -i '1s/^/from typing import Dict, Any, Optional, List\n\n/' "$file"
        echo "  Added typing imports to $file"
    fi
done

# Check BaseModel
echo -e "\n3. Checking BaseModel..."
if ! grep -q "from typing import" business_logic/models/base_model.py; then
    sed -i '1s/^/from typing import Dict, Any\n\n/' business_logic/models/base_model.py
fi

echo -e "\n4. Testing fixes..."
python3 -c "
try:
    from business_logic.models.user import User
    print('✅ User model imports')
    user = User(email='test@test.com', password='123456', first_name='John', last_name='Doe')
    print('✅ User creates successfully')
    print(f'User ID: {user.id}')
except Exception as e:
    print(f'❌ Error: {e}')
"
