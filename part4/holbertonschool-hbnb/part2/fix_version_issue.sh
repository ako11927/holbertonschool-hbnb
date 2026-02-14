#!/bin/bash
echo "=== Fixing Version Compatibility Issue ==="

# Check current versions
echo "Current versions:"
pip3 list | grep -E "(flask|werkzeug|restx)" || echo "Not installed"

# Fix 1: Downgrade Werkzeug (most likely solution)
echo -e "\n1. Downgrading Werkzeug to 2.x..."
pip3 install "werkzeug==2.3.8" --force-reinstall

# Fix 2: If that doesn't work, also downgrade Flask-RESTX
echo -e "\n2. Ensuring compatible Flask-RESTX..."
pip3 install "flask-restx==1.1.0" --force-reinstall 2>/dev/null || true

# Fix 3: Update requirements.txt to prevent future issues
echo -e "\n3. Updating requirements.txt..."
cat > requirements.txt << 'REQEOF'
Flask==2.3.3
flask-restx==1.1.0
werkzeug==2.3.8
REQEOF

echo -e "\n4. Installing from updated requirements..."
pip3 install -r requirements.txt

echo -e "\n5. Verifying fix..."
python3 -c "
try:
    import werkzeug
    print(f'✅ Werkzeug version: {werkzeug.__version__}')
    
    import flask
    import flask_restx
    print(f'✅ Flask version: {flask.__version__}')
    print(f'✅ Flask-RESTX version: {flask_restx.__version__}')
    
    # Test the import that was failing
    from werkzeug import __version__ as werkzeug_version
    print(f'✅ werkzeug.__version__ import works: {werkzeug_version}')
    
    print('\\n✅ Version compatibility fixed!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
"
