"""API routes."""
from flask import Blueprint
from app.api.v1.controllers.user_controller import UserController
from app.api.v1.controllers.place_controller import PlaceController
from app.api.v1.controllers.review_controller import ReviewController
from app.api.v1.controllers.amenity_controller import AmenityController

# Initialize controllers
user_controller = UserController()
place_controller = PlaceController()
review_controller = ReviewController()
amenity_controller = AmenityController()

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# User routes
api_bp.route('/users', methods=['GET'])(user_controller.get_users)
api_bp.route('/users', methods=['POST'])(user_controller.create_user)
api_bp.route('/users/<string:user_id>', methods=['GET'])(user_controller.get_user)
api_bp.route('/users/<string:user_id>', methods=['PUT'])(user_controller.update_user)
api_bp.route('/users/<string:user_id>', methods=['DELETE'])(user_controller.delete_user)

# Place routes
api_bp.route('/places', methods=['GET'])(place_controller.get_places)
api_bp.route('/places', methods=['POST'])(place_controller.create_place)
api_bp.route('/places/<string:place_id>', methods=['GET'])(place_controller.get_place)
api_bp.route('/places/<string:place_id>', methods=['PUT'])(place_controller.update_place)
api_bp.route('/places/<string:place_id>', methods=['DELETE'])(place_controller.delete_place)
api_bp.route('/places/search', methods=['GET'])(place_controller.search_places)
api_bp.route('/places/city', methods=['GET'])(place_controller.get_places_by_city)
api_bp.route('/places/price-range', methods=['GET'])(place_controller.get_places_by_price_range)
api_bp.route('/places/filter', methods=['GET'])(place_controller.get_places_with_filters)

# Review routes
api_bp.route('/reviews', methods=['GET'])(review_controller.get_reviews)
api_bp.route('/reviews', methods=['POST'])(review_controller.create_review)
api_bp.route('/reviews/<string:review_id>', methods=['GET'])(review_controller.get_review)
api_bp.route('/reviews/<string:review_id>', methods=['PUT'])(review_controller.update_review)
api_bp.route('/reviews/<string:review_id>', methods=['DELETE'])(review_controller.delete_review)
api_bp.route('/reviews/rating', methods=['GET'])(review_controller.get_reviews_by_rating)
api_bp.route('/reviews/recent', methods=['GET'])(review_controller.get_recent_reviews)

# Amenity routes
api_bp.route('/amenities', methods=['GET'])(amenity_controller.get_amenities)
api_bp.route('/amenities', methods=['POST'])(amenity_controller.create_amenity)
api_bp.route('/amenities/<string:amenity_id>', methods=['GET'])(amenity_controller.get_amenity)
api_bp.route('/amenities/<string:amenity_id>', methods=['PUT'])(amenity_controller.update_amenity)
api_bp.route('/amenities/<string:amenity_id>', methods=['DELETE'])(amenity_controller.delete_amenity)
api_bp.route('/amenities/search', methods=['GET'])(amenity_controller.search_amenities)
