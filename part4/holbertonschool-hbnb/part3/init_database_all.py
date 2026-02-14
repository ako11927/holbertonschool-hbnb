"""Initialize the database with all entities."""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db
from config import config

# Create app with development config
app = create_app(config['development'])

with app.app_context():
    print("Initializing database with all entities...")
    
    # Create all tables
    db.create_all()
    print("✓ Database tables created successfully")
    
    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("\nCreated tables:")
    for table in tables:
        print(f"  - {table}")
    
    # Check if models are properly mapped
    print("\nEntity models verified:")
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
    
    entities = [User, Place, Review, Amenity]
    for entity in entities:
        print(f"  ✓ {entity.__name__} (table: {entity.__tablename__})")
    
    print("\nDatabase initialization complete!")
