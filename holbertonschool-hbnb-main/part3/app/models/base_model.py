"""SQLAlchemy-mapped base model for all entities.

This class centralises the common columns that all persisted entities share:

- ``id``: primary key
- ``created_at``: timestamp set when the row is first inserted
- ``updated_at``: timestamp automatically updated on each modification

Design choices
--------------

* We subclass :class:`db.Model` and mark the class as ``__abstract__`` so that
  SQLAlchemy does not create a physical ``basemodel`` table.  Concrete models
  (such as ``User``) inherit from :class:`BaseModel` to gain the columns.
* Timestamps use ``datetime.utcnow`` for predictable, timezone‑agnostic
  values, and ``onupdate`` ensures ``updated_at`` is refreshed on UPDATE
  statements without extra manual code.
* The helper methods (:meth:`to_dict`, :meth:`save`, :meth:`update`) keep the
  same external behaviour as the original in‑memory base class so existing
  calling code continues to work.
"""

from datetime import datetime
from typing import Any, Dict

from app import db


class BaseModel(db.Model):
    """Abstract SQLAlchemy base model with common columns and helpers."""

    __abstract__ = True

    # We keep ``id`` as an integer primary key to match how the rest of the
    # project (API routes, JWT identities, etc.) already treat user IDs.
    id = db.Column(db.Integer, primary_key=True)

    # ``created_at`` is set once on INSERT, ``updated_at`` is set on INSERT
    # and automatically refreshed whenever the row is updated.
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serialisable dictionary.

        We intentionally ignore private attributes (including SQLAlchemy's
        internal state) and serialise datetimes using ISO 8601 strings so the
        API layer can safely JSON‑encode the result.
        """
        result: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if key in ("created_at", "updated_at") and hasattr(
                value, "isoformat"
            ):
                result[key] = value.isoformat()
            else:
                result[key] = value
        result["__class__"] = self.__class__.__name__
        return result

    def save(self) -> "BaseModel":
        """Update the in‑memory ``updated_at`` timestamp.

        This mirrors the behaviour of the original base class and is useful
        for non‑database uses. Database persistence (session add/commit) is
        still handled by the repository / service layer.
        """
        self.updated_at = datetime.utcnow()
        return self

    def update(self, **kwargs: Any) -> "BaseModel":
        """Update model attributes in a generic way.

        Business‑specific update rules live in the service layer; this helper
        is only a convenience for trivial attribute updates.
        """
        for key, value in kwargs.items():
            if key not in ("id", "created_at", "__class__"):
                setattr(self, key, value)
        self.save()
        return self

    def __str__(self) -> str:
        """Human‑readable string representation."""
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"

    def __repr__(self) -> str:
        """Official string representation."""
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """Compare instances by primary key."""
        if isinstance(other, BaseModel):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        """Allow instances to be used in sets / as dict keys."""
        return hash(self.id)
