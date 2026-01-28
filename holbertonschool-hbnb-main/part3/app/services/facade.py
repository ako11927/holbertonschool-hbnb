"""Application Facade for HBnB.

This class coordinates higher‑level operations and delegates persistence
to repository objects.  By depending only on the abstract ``Repository``
interface we can swap out the underlying implementation (in‑memory vs
SQLAlchemy) without changing the business logic.
"""

from app import db
from app.persistence.repository import InMemoryRepository, UserRepository
from app.models.user import User


class HBnBFacade:
    """Facade exposing high‑level operations over domain entities.

    The constructor wires repositories for each aggregate.  At this stage of
    the project only ``User`` is persisted with SQLAlchemy; the other models
    still use simple in‑memory objects, so we keep their repositories as
    ``InMemoryRepository`` for now.

    As additional SQLAlchemy models are introduced, their corresponding
    repositories can be migrated to ``SQLAlchemyRepository`` in the same way
    as ``user_repo`` below.
    """

    def __init__(self):
        # Users are stored in the relational database via SQLAlchemy using a
        # dedicated ``UserRepository``.  The Facade depends only on the
        # repository interface, not on SQLAlchemy itself, which keeps the
        # persistence details encapsulated.
        self.user_repo = UserRepository(db.session)

        # The remaining repositories still use the in‑memory implementation.
        # This keeps the behaviour consistent with the current codebase while
        # making it easy to migrate each entity to SQLAlchemy in the future.
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID."""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Get user by email."""
        # Delegate to the repository's specialised query method; the Facade
        # still owns business logic such as enforcing uniqueness.
        return self.user_repo.get_by_email(email)

    def update_user(self, user_id, user_data):
        """Update user information."""
        # First get the user
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        # Check if email is being changed and if it's unique
        if 'email' in user_data and user_data['email'] != user.email:
            existing = self.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        
        # Update the user
        user.update(user_data)
        return user

    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information."""
        # First get the amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        # Update the amenity
        amenity.update(amenity_data)
        return amenity

    # Place methods
    def create_place(self, place_data):
        """Create a new place."""
        from app.models.place import Place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place information."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update(place_data)
        return place

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place."""
        return [r for r in self.review_repo.get_all() if getattr(r, 'place_id', None) == place_id]

    # Review methods
    def create_review(self, review_data):
        """Create a new review."""
        from app.models.review import Review
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews."""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Update a review."""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            r = int(review_data['rating'])
            if 1 <= r <= 5:
                review.rating = r
        return review

    def delete_review(self, review_id):
        """Delete a review."""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
