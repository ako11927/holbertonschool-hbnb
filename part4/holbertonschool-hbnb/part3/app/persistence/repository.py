"""Repository abstraction and implementations.
   InMemoryRepository: existing in-memory store.
   SQLAlchemyRepository: db.session-backed store; generic, reusable for any mapped model."""
from abc import ABC, abstractmethod

from app import db


class Repository(ABC):
    """Abstract repository interface. All persistence adapters implement this."""

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of Repository."""

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value),
            None,
        )


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-backed repository implementing the Repository interface.
    Generic and reusable for any Flask-SQLAlchemy model. Uses db.session for all operations.
    DB init (create_all, migrations) is deferred; model mapping is done in a later task."""

    def __init__(self, model_class):
        self._model = model_class

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return db.session.get(self._model, obj_id)

    def get_all(self):
        return db.session.query(self._model).all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return
        if hasattr(obj, "update") and callable(getattr(obj, "update")):
            obj.update(data)
        else:
            for k, v in data.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
        db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return (
            db.session.query(self._model)
            .filter_by(**{attr_name: attr_value})
            .first()
        )


class UserRepository(SQLAlchemyRepository):
    """Repository bound to User model. Adds user-specific query by email."""

    def __init__(self):
        from app.models.user import User
        super().__init__(User)

    def get_user_by_email(self, email):
        """Return the user with the given email, or None."""
        return self.get_by_attribute("email", email)
