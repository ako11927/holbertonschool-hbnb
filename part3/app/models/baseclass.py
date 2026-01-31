"""SQLAlchemy abstract base model for all ORM entities.

Maps the BaseModel concept to Flask-SQLAlchemy with common columns:
id (UUID string), created_at, updated_at. Marked abstract so no table is created.
"""
import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    """Abstract base for all SQLAlchemy models. Provides id (UUID), created_at, updated_at."""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
