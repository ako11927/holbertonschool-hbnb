"""User ORM model for HBnB. Inherits from SQLAlchemy BaseModel; password hashed with Flask-Bcrypt."""
from app import bcrypt, db
from app.models.baseclass import BaseModel


class User(BaseModel):
    """User entity: first_name, last_name, email (unique), hashed password, is_admin."""

    __tablename__ = "users"

    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, password: str) -> None:
        """Hash and set the user's password using Flask-Bcrypt."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify a plain password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert to dict; never expose password."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
