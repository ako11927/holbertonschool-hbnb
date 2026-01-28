"""Repository abstractions for the HBnB application.

This module defines:

- ``Repository``: abstract base class describing the repository interface.
- ``InMemoryRepository``: simple in‑memory implementation used for testing
  and for models that are not yet backed by SQLAlchemy.
- ``SQLAlchemyRepository``: implementation backed by a SQLAlchemy session.

The SQLAlchemy repository is intentionally lightweight – it does **not**
create tables or perform any database initialisation.  It simply assumes
that:

- A SQLAlchemy ``Session`` (typically ``db.session`` from Flask‑SQLAlchemy)
  is provided.
- A SQLAlchemy mapped model class will be passed in later.  For now we keep
  the API and wiring ready for when models are mapped.
"""

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional, Type

from sqlalchemy.orm import Session

from app.models.user import User


class Repository(ABC):
    """Abstract repository interface used throughout the application.

    Implementations must provide basic CRUD operations plus a simple
    attribute‑based lookup method.  The Facade and services depend only on
    this interface, not on the specific persistence technology.
    """

    @abstractmethod
    def add(self, obj: Any) -> Any:
        """Add a new object to the repository."""
        raise NotImplementedError

    @abstractmethod
    def get(self, obj_id: Any) -> Optional[Any]:
        """Return a single object by its identifier, or ``None``."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Iterable[Any]:
        """Return an iterable of all objects in the repository."""
        raise NotImplementedError

    @abstractmethod
    def update(self, obj_id: Any, data: dict) -> Optional[Any]:
        """Update an existing object with ``data`` and return it, or ``None``."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, obj_id: Any) -> bool:
        """Delete an object by id.  Return ``True`` if something was deleted."""
        raise NotImplementedError

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        """Return the first object for which ``getattr(obj, attr_name) == attr_value``."""
        raise NotImplementedError


class InMemoryRepository(Repository):
    """Simple in‑memory implementation used by the early project tasks.

    This implementation is still kept around for:
    - Unit tests that rely on a fast, in‑memory store.
    - Models that are not yet backed by SQLAlchemy.
    """

    def __init__(self) -> None:
        self._storage: dict[Any, Any] = {}

    def add(self, obj: Any) -> Any:
        """Store an object in the internal dictionary keyed by ``obj.id``."""
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id: Any) -> Optional[Any]:
        return self._storage.get(obj_id)

    def get_all(self) -> list[Any]:
        return list(self._storage.values())

    def update(self, obj_id: Any, data: dict) -> Optional[Any]:
        obj = self.get(obj_id)
        if not obj:
            return None
        # Delegate the actual mutation to the entity if it provides ``update``.
        update_fn = getattr(obj, "update", None)
        if callable(update_fn):
            update_fn(data)
        else:
            for key, value in data.items():
                setattr(obj, key, value)
        return obj

    def delete(self, obj_id: Any) -> bool:
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name, None) == attr_value
            ),
            None,
        )


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the :class:`Repository` interface.

    This class is responsible only for interacting with a SQLAlchemy session.
    It does **not**:
    - create or configure the database engine,
    - create tables,
    - or define SQLAlchemy models.

    Those concerns are handled elsewhere (e.g. in the Flask application
    factory and model definitions).

    Parameters
    ----------
    model:
        The SQLAlchemy mapped model class this repository manages.
    session:
        A SQLAlchemy :class:`Session` (usually ``db.session`` in a Flask app).
    """

    def __init__(self, model: Type[Any], session: Session) -> None:
        self.model = model
        self.session = session

    # --- CRUD methods ----------------------------------------------------

    def add(self, obj: Any) -> Any:
        """Add a new object and commit the change.

        We commit here to preserve the behaviour of the in‑memory repository
        (where changes are immediately visible) and to keep usage simple for
        the current project stage.  If a more advanced unit‑of‑work pattern
        is introduced later, the commit responsibility can be moved out of
        the repository.
        """
        self.session.add(obj)
        self.session.commit()
        # Ensure any autogenerated fields (e.g. primary keys) are populated.
        try:
            self.session.refresh(obj)
        except Exception:
            # Refresh is not strictly required; ignore any issues here.
            pass
        return obj

    # The in‑memory implementation exposes ``get`` only.  For repositories
    # backed by SQLAlchemy we also provide an explicit ``get_by_id`` helper
    # that simply delegates to ``get``.  This keeps backwards compatibility
    # with the existing interface while supporting a slightly richer, more
    # expressive API for callers that prefer the explicit naming.

    def get_by_id(self, obj_id: Any) -> Optional[Any]:
        """Return a single object by primary key, or ``None``."""
        return self.get(obj_id)

    def get(self, obj_id: Any) -> Optional[Any]:
        """Return a single object by primary key, or ``None``."""
        # ``Session.get`` is the preferred 2.x API.
        try:
            return self.session.get(self.model, obj_id)  # type: ignore[arg-type]
        except Exception:
            # Fallback for older SQLAlchemy versions if needed.
            return (
                self.session.query(self.model).get(obj_id)  # type: ignore[call-arg]
            )

    def get_all(self) -> list[Any]:
        """Return all instances of the model."""
        return list(self.session.query(self.model))  # type: ignore[arg-type]

    def update(self, obj_id: Any, data: dict) -> Optional[Any]:
        """Update an object by id using the values in ``data``.

        The entity itself may expose richer update logic; this method keeps
        things generic by simply setting attributes.
        """
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        self.session.commit()
        return obj

    def delete(self, obj_id: Any) -> bool:
        """Delete an object by id.  Return ``True`` if something was deleted."""
        obj = self.get(obj_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True

    def get_by_attribute(self, attr_name: str, attr_value: Any) -> Optional[Any]:
        """Lookup the first row where ``attr_name == attr_value``.

        This mirrors the simple behaviour of the in‑memory implementation
        while delegating the actual work to SQLAlchemy's query API.
        """
        # Prefer attribute access when ``attr_name`` maps to a real column.
        column = getattr(self.model, attr_name, None)
        query = self.session.query(self.model)  # type: ignore[arg-type]
        if column is not None:
            return query.filter(column == attr_value).first()
        # Fallback to ``filter_by`` for dynamic attributes.
        return query.filter_by(**{attr_name: attr_value}).first()


class UserRepository(SQLAlchemyRepository):
    """Repository specialised for :class:`User` entities.

    This class keeps all persistence concerns (session handling, queries)
    inside the repository while leaving business rules (such as who is
    allowed to create or modify a user) in the Facade / service layer.
    """

    def __init__(self, session: Session) -> None:
        # Bind the repository to the concrete ``User`` model and the shared
        # SQLAlchemy session (typically ``db.session`` from Flask‑SQLAlchemy).
        super().__init__(User, session)

    def get_by_email(self, email: str) -> Optional[User]:
        """Return the first user with the given email address, if any."""
        return self.get_by_attribute("email", email)

