"User model for HBnB using SQLAlchemy."
from datetime import datetime
from app import db, bcrypt

class User(db.Model):
    "User class representing a user in the system with hashed password."

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        "Hash and set the user's password."
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf8")

    def check_password(self, password):
        "Check hashed password."
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        "Convert user to dictionary without password."
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"

