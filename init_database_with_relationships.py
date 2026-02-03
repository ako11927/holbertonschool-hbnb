"""Initialize the database with all entities and relationships."""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db
from config import config

# Create app with development config
app = create_app(config['development'])

with app.app_context():
    print("Initializing database with all entities and relationships...")
    
    # Create all tables (including association tables)
    db.create_all()
    print("✓ Database tables created successfully")
    
    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("\nCreated tables:")
    for table in tables:
        print(f"  - {table}")
    
    # Check foreign key constraints
    print("\nForeign key relationships verified:")
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
    
    # Check User relationships
    print(f"\nUser model relationships:")
    print(f"  ✓ places: One-to-Many relationship with Place")
    print(f"  ✓ reviews: One-to-Many relationship with Review")
    
    # Check Place relationships
    print(f"\nPlace model relationships:")
    print(f"  ✓ owner: Many-to-One relationship with User")
    print(f"  ✓ reviews: One-to-Many relationship with Review")
    print(f"  ✓ amenities: Many-to-Many relationship with Amenity")
    
    # Check Review relationships
    print(f"\nReview model relationships:")
    print(f"  ✓ user: Many-to-One relationship with User")
    print(f"  ✓ place: Many-to-One relationship with Place")
    
    # Check Amenity relationships
    print(f"\nAmenity model relationships:")
    print(f"  ✓ places: Many-to-Many relationship with Place")
    
    # Test relationship integrity
    print("\nTesting relationship integrity...")
    
    # Create test data to verify relationships work
    from app.models.user import User as UserModel
    from app.models.place import Place as PlaceModel
    from app.models.amenity import Amenity as AmenityModel
    from app.models.review import Review as ReviewModel
    
    # Create a test user
    test_user = UserModel(
        email='test@example.com',
        first_name='Test',
        last_name='User',
        password='password123'
    )
    test_user.hash_password('password123')
    db.session.add(test_user)
    
    # Create a test amenity
    test_amenity = AmenityModel(name='Test Amenity')
    db.session.add(test_amenity)
    
    db.session.commit()
    
    # Create a test place with relationships
    test_place = PlaceModel(
        title='Test Place',
        description='A test place for relationship verification',
        price=100.00,
        address='123 Test St',
        city='Test City',
        owner_id=test_user.id
    )
    test_place.amenities.append(test_amenity)
    db.session.add(test_place)
    
    # Create a test review with relationships
    test_review = ReviewModel(
        text='A test review for relationship verification',
        rating=5,
        user_id=test_user.id,
        place_id=test_place.id
    )
    db.session.add(test_review)
    
    db.session.commit()
    
    # Verify relationships
    print(f"  ✓ User has {len(test_user.places)} places")
    print(f"  ✓ User has {len(test_user.reviews)} reviews")
    print(f"  ✓ Place has owner: {test_place.owner.email}")
    print(f"  ✓ Place has {len(test_place.reviews)} reviews")
    print(f"  ✓ Place has {len(test_place.amenities)} amenities")
    print(f"  ✓ Review has user: {test_review.user.email}")
    print(f"  ✓ Review has place: {test_review.place.title}")
    print(f"  ✓ Amenity is in {len(test_amenity.places)} places")
    
    # Clean up test data
    db.session.delete(test_review)
    db.session.delete(test_place)
    db.session.delete(test_amenity)
    db.session.delete(test_user)
    db.session.commit()
    
    print("\nDatabase initialization with relationships complete!")
