"""User model for HBnB using SQLAlchemy and Flask-Bcrypt.

The ``User`` entity is a full SQLAlchemy model that:

- Inherits from :class:`BaseModel` to get the shared ``id``, ``created_at``
  and ``updated_at`` columns.
- Stores passwords **only** in hashed form using Flask‑Bcrypt.  The public
  API remains ``set_password`` / ``check_password`` so that callers never
  touch the raw hash directly.
"""

from app import bcrypt, db
from .base_model import BaseModel


class User(BaseModel):
    """User class representing a user in the system with hashed password."""

    __tablename__ = "users"

    # Domain‑specific columns; ``id``, ``created_at`` and ``updated_at`` come
    # from :class:`BaseModel`.
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(
        db.String(120),
        unique=True,
        index=True,  # efficient lookup for login / uniqueness checks
        nullable=False,
    )
    # Store only the Bcrypt hash, never the raw password.
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.

        The hashing logic continues to use Flask‑Bcrypt exactly as before; we
        simply store the result in the ``password`` column.
        """
        self.password = bcrypt.generate_password_hash(password).decode("utf8")

    def check_password(self, password: str) -> bool:
        """Validate a plaintext password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self) -> dict:
        """Convert user to dictionary without exposing the password hash."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
