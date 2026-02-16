from app import db, bcrypt
from .base_model import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)   # ✅ مهم للتاسك

    # ========== Relationships ==========
    # One-to-Many: User -> Place
    places = db.relationship('Place', backref='owner', lazy=True)

    # One-to-Many: User -> Review
    reviews = db.relationship('Review', backref='author', lazy=True)

    # ========== Methods ==========
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
