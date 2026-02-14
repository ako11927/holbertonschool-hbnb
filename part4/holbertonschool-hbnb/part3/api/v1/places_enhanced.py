#!/usr/bin/python3
"""
Enhanced Places API endpoints with pagination, filtering, and caching
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from functools import wraps
import json
from datetime import datetime


def cache_response(timeout=300):
    """Decorator to cache API responses"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{request.path}?{request.query_string.decode()}"
            
            # Try to get from cache
            redis_cache = storage.__redis_cache if hasattr(storage, '__redis_cache') else None
            if redis_cache:
                cached = redis_cache.get(cache_key)
                if cached:
                    return jsonify(json.loads(cached))
            
            # Execute function
            response = f(*args, **kwargs)
            
            # Cache the response
            if redis_cache and response.status_code == 200:
                redis_cache.setex(
                    cache_key,
                    timeout,
                    response.get_data(as_text=True)
                )
            
            return response
        return decorated_function
    return decorator


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@cache_response(timeout=60)
def get_places(city_id):
    """
    Get all places in a city with enhanced features
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Get filter parameters
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    amenities = request.args.getlist('amenities')
    
    # Build query
    query = storage.__session.query(Place).filter_by(city_id=city_id)
    
    # Apply filters
    if min_price is not None:
        query = query.filter(Place.price_by_night >= min_price)
    if max_price is not None:
        query = query.filter(Place.price_by_night <= max_price)
    
    # Apply amenities filter
    if amenities:
        for amenity_id in amenities:
            query = query.filter(Place.amenities.any(id=amenity_id))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    places = query.offset((page - 1) * per_page).limit(per_page).all()
    
    # Prepare response
    places_list = []
    for place in places:
        place_dict = place.to_dict()
        
        # Add calculated fields
        place_dict['average_rating'] = place.average_rating()
        place_dict['total_reviews'] = len(place.reviews)
        
        # Include only essential information
        essential_fields = ['id', 'name', 'description', 'price_by_night',
                          'latitude', 'longitude', 'average_rating',
                          'total_reviews', 'created_at']
        place_dict = {k: v for k, v in place_dict.items() if k in essential_fields}
        
        places_list.append(place_dict)
    
    response = {
        'data': places_list,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        },
        'filters_applied': {
            'min_price': min_price,
            'max_price': max_price,
            'amenities': amenities
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return jsonify(response)


@app_views.route('/places/<place_id>', methods=['GET'])
@cache_response(timeout=300)
def get_place(place_id):
    """
    Get specific place with detailed information
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    
    place_dict = place.to_dict()
    
    # Enhance with related data
    place_dict['city'] = place.city.to_dict() if place.city else None
    place_dict['user'] = place.user.to_dict() if place.user else None
    
    # Calculate statistics
    place_dict['statistics'] = {
        'average_rating': place.average_rating(),
        'total_reviews': len(place.reviews),
        'total_amenities': len(place.amenities)
    }
    
    # Include reviews preview
    recent_reviews = sorted(place.reviews, key=lambda x: x.created_at, reverse=True)[:3]
    place_dict['recent_reviews'] = [
        {
            'id': review.id,
            'text': review.text[:100] + '...' if len(review.text) > 100 else review.text,
            'rating': review.rating,
            'user_name': review.user.first_name
        }
        for review in recent_reviews
    ]
    
    return jsonify(place_dict)


@app_views.route('/places/search', methods=['POST'])
def search_places():
    """
    Advanced search for places
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    
    data = request.get_json()
    
    # Build query
    query = storage.__session.query(Place)
    
    # Text search
    if 'text' in data:
        search_text = f"%{data['text']}%"
        query = query.filter(
            Place.name.ilike(search_text) |
            Place.description.ilike(search_text)
        )
    
    # Location search
    if 'latitude' in data and 'longitude' in data and 'radius' in data:
        # Simplified distance calculation (for demo purposes)
        # In production, use PostGIS or similar
        lat = data['latitude']
        lng = data['longitude']
        radius = data['radius']
        
        # This is a simplified version - implement proper haversine formula
        query = query.filter(
            Place.latitude.between(lat - radius/111, lat + radius/111),
            Place.longitude.between(lng - radius/111, lng + radius/111)
        )
    
    # Date availability
    if 'check_in' in data and 'check_out' in data:
        # Check for available places (simplified)
        # In production, check against bookings
        pass
    
    # Execute query
    places = query.limit(50).all()
    
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/stats', methods=['GET'])
def get_places_stats():
    """
    Get statistics about places
    """
    stats = {
        'total_places': storage.count(Place),
        'by_city': {},
        'price_distribution': {
            'under_50': storage.__session.query(Place).filter(Place.price_by_night < 50).count(),
            '50_100': storage.__session.query(Place).filter(Place.price_by_night.between(50, 100)).count(),
            '100_200': storage.__session.query(Place).filter(Place.price_by_night.between(100, 200)).count(),
            'over_200': storage.__session.query(Place).filter(Place.price_by_night > 200).count()
        },
        'average_price': storage.__session.query(
            func.avg(Place.price_by_night)
        ).scalar() or 0
    }
    
    return jsonify(stats)
