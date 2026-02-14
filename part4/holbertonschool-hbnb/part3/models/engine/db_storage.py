#!/usr/bin/python3
"""
Enhanced DBStorage module for HBNB
"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import redis
from datetime import datetime, timedelta


class DBStorage:
    """
    Enhanced database storage with caching and connection pooling
    """
    __engine = None
    __session = None
    __redis_cache = None
    
    def __init__(self):
        """Initialize DBStorage with enhanced features"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            echo=False
        )
        
        # Initialize Redis cache
        redis_host = os.getenv('HBNB_REDIS_HOST', 'localhost')
        redis_port = os.getenv('HBNB_REDIS_PORT', 6379)
        try:
            self.__redis_cache = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=0,
                decode_responses=True
            )
        except:
            self.__redis_cache = None
        
        if env == 'test':
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """
        Query all objects with caching support
        """
        cache_key = f"all_{cls.__name__ if cls else 'all'}"
        
        # Try to get from cache first
        if self.__redis_cache:
            cached = self.__redis_cache.get(cache_key)
            if cached:
                return eval(cached)
        
        classes = [User, State, City, Amenity, Place, Review]
        objects = {}
        
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                key = f"{type(obj).__name__}.{obj.id}"
                objects[key] = obj
        else:
            for cls in classes:
                query = self.__session.query(cls).all()
                for obj in query:
                    key = f"{type(obj).__name__}.{obj.id}"
                    objects[key] = obj
        
        # Cache the results
        if self.__redis_cache:
            self.__redis_cache.setex(
                cache_key,
                300,  # 5 minutes TTL
                str(objects)
            )
        
        return objects
    
    def new(self, obj):
        """Add new object to session"""
        self.__session.add(obj)
    
    def save(self):
        """Commit all changes to database"""
        try:
            self.__session.commit()
            # Invalidate relevant cache entries
            if self.__redis_cache:
                self.__redis_cache.delete("all_*")
        except Exception as e:
            self.__session.rollback()
            raise e
    
    def delete(self, obj=None):
        """Delete object from database"""
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        """Create all tables and session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
    
    def close(self):
        """Close session"""
        if self.__session:
            self.__session.remove()
        if self.__redis_cache:
            self.__redis_cache.close()
    
    def get(self, cls, id):
        """
        Enhanced get method with caching
        """
        if cls and id:
            cache_key = f"{cls.__name__}_{id}"
            
            # Try cache first
            if self.__redis_cache:
                cached = self.__redis_cache.get(cache_key)
                if cached:
                    return eval(cached)
            
            # Query database
            result = self.__session.query(cls).filter_by(id=id).first()
            
            # Cache the result
            if result and self.__redis_cache:
                self.__redis_cache.setex(
                    cache_key,
                    600,  # 10 minutes TTL
                    str(result)
                )
            
            return result
        return None
    
    def count(self, cls=None):
        """
        Count objects in storage
        """
        if cls:
            return self.__session.query(cls).count()
        total = 0
        for cls in [User, State, City, Amenity, Place, Review]:
            total += self.__session.query(cls).count()
        return total
