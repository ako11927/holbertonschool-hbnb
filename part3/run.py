"Run file for HBnB application."
import os
from app import create_app, db
from config import config

# Determine environment, default to development
env = os.environ.get("FLASK_ENV", "development")
ConfigClass = config.get(env, config["default"])

# Create Flask app with selected configuration
app = create_app(ConfigClass)

# Initialize database tables (only users table at this stage; other entities use in-memory).
with app.app_context():
    db.create_all()
    print(f"Database tables created for {env} environment.")

if __name__ == "__main__":
    # Run Flask server
    app.run(host="0.0.0.0", port=5000)


