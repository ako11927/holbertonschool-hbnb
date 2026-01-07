"""Place API endpoints."""
from flask_restx import Namespace, Resource, fields, reqparse
from business_logic.facade import HBnBFacade
from business_logic.exceptions import ValidationError, NotFoundError
from decimal import Decimal

api = Namespace('places', description='Place operations')

# Request parsers
place_parser = reqparse.RequestParser()
place_parser.add_argument('user_id', type=str, required=True, help='User ID (owner)')
place_parser.add_argument('name', type=str, required=True, help='Place name')
place_parser.add_argument('description', type=str, required=False, help='Description')
place_parser.add_argument('number_rooms', type=int, required=True, help='Number of rooms')
place_parser.add_argument('number_bathrooms', type=int, required=True, help='Number of bathrooms')
place_parser.add_argument('max_guest', type=int, required=True, help='Maximum guests')
place_parser.add_argument('price_by_night', type=float, required=True, help='Price per night')
place_parser.add_argument('latitude', type=float, required=True, help='Latitude')
place_parser.add_argument('longitude', type=float, required=True, help='Longitude')
place_parser.add_argument('city_id', type=str, required=True, help='City ID')
place_parser.add_argument('amenity_ids', type=str, action='append', required=False, help='Amenity IDs')

update_place_parser = reqparse.RequestParser()
update_place_parser.add_argument('name', type=str, required=False, help='Place name')
update_place_parser.add_argument('description', type=str, required=False, help='Description')
update_place_parser.add_argument('number_rooms', type=int, required=False, help='Number of rooms')
update_place_parser.add_argument('number_bathrooms', type=int, required=False, help='Number of bathrooms')
update_place_parser.add_argument('max_guest', type=int, required=False, help='Maximum guests')
update_place_parser.add_argument('price_by_night', type=float, required=False, help='Price per night')
update_place_parser.add_argument('latitude', type=float, required=False, help='Latitude')
update_place_parser.add_argument('longitude', type=float, required=False, help='Longitude')
update_place_parser.add_argument('amenity_ids', type=str, action='append', required=False, help='Amenity IDs')

# Simplified response models (no cross-references)
place_model = api.model('Place', {
    'id': fields.String(description='Place ID'),
    'user_id': fields.String(description='Owner user ID'),
    'name': fields.String(description='Place name'),
    'description': fields.String(description='Description'),
    'number_rooms': fields.Integer(description='Number of rooms'),
    'number_bathrooms': fields.Integer(description='Number of bathrooms'),
    'max_guest': fields.Integer(description='Maximum guests'),
    'price_by_night': fields.String(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'city_id': fields.String(description='City ID'),
    'amenity_ids': fields.List(fields.String, description='Amenity IDs'),
    'average_rating': fields.Float(description='Average rating'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

facade = HBnBFacade()

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """
        Retrieve all places.
        
        Returns:
            List of all places
        """
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @api.doc('create_place')
    @api.expect(place_parser)
    @api.marshal_with(place_model, code=201)
    @api.response(400, 'Invalid input')
    @api.response(404, 'User or City not found')
    def post(self):
        """
        Create a new place.
        
        Returns:
            Created place data
        """
        args = place_parser.parse_args()
        
        # Convert price to Decimal
        if 'price_by_night' in args and args['price_by_night'] is not None:
            args['price_by_night'] = Decimal(str(args['price_by_night']))
        
        # Validate coordinates
        if args['latitude'] < -90 or args['latitude'] > 90:
            api.abort(400, 'Latitude must be between -90 and 90')
        if args['longitude'] < -180 or args['longitude'] > 180:
            api.abort(400, 'Longitude must be between -180 and 180')
        
        # Validate numeric fields
        if args['number_rooms'] < 0:
            api.abort(400, 'Number of rooms cannot be negative')
        if args['number_bathrooms'] < 0:
            api.abort(400, 'Number of bathrooms cannot be negative')
        if args['max_guest'] < 0:
            api.abort(400, 'Maximum guests cannot be negative')
        if args['price_by_night'] < 0:
            api.abort(400, 'Price cannot be negative')
        
        try:
            place = facade.create_place(args)
            
            # Add amenities if provided
            if args.get('amenity_ids'):
                for amenity_id in args['amenity_ids']:
                    try:
                        facade.add_amenity_to_place(place.id, amenity_id)
                    except NotFoundError:
                        # Skip amenities that don't exist
                        pass
            
            return place.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """
        Retrieve a place by ID.
        
        Args:
            place_id: Place identifier
            
        Returns:
            Place data
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f'Place {place_id} not found')
        
        return place.to_dict(), 200

    @api.doc('update_place')
    @api.expect(update_place_parser)
    @api.marshal_with(place_model)
    @api.response(400, 'Invalid input')
    def put(self, place_id):
        """
        Update place information.
        
        Args:
            place_id: Place identifier
            
        Returns:
            Updated place data
        """
        args = update_place_parser.parse_args()
        
        # Remove None values
        update_data = {k: v for k, v in args.items() if v is not None}
        
        if not update_data:
            api.abort(400, 'No update data provided')
        
        # Get existing place
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f'Place {place_id} not found')
        
        try:
            # Validate coordinates if provided
            if 'latitude' in update_data and (update_data['latitude'] < -90 or update_data['latitude'] > 90):
                api.abort(400, 'Latitude must be between -90 and 90')
            if 'longitude' in update_data and (update_data['longitude'] < -180 or update_data['longitude'] > 180):
                api.abort(400, 'Longitude must be between -180 and 180')
            
            # Validate numeric fields if provided
            if 'number_rooms' in update_data and update_data['number_rooms'] < 0:
                api.abort(400, 'Number of rooms cannot be negative')
            if 'number_bathrooms' in update_data and update_data['number_bathrooms'] < 0:
                api.abort(400, 'Number of bathrooms cannot be negative')
            if 'max_guest' in update_data and update_data['max_guest'] < 0:
                api.abort(400, 'Maximum guests cannot be negative')
            if 'price_by_night' in update_data and update_data['price_by_night'] < 0:
                api.abort(400, 'Price cannot be negative')
            
            # Convert price to Decimal if provided
            if 'price_by_night' in update_data:
                update_data['price_by_night'] = Decimal(str(update_data['price_by_night']))
            
            # Update place attributes
            for key, value in update_data.items():
                if hasattr(place, key):
                    setattr(place, key, value)
            
            # Handle amenity updates
            if 'amenity_ids' in update_data:
                # Clear existing amenities
                place.amenity_ids = []
                place.amenities = []
                
                # Add new amenities
                for amenity_id in update_data['amenity_ids']:
                    try:
                        facade.add_amenity_to_place(place.id, amenity_id)
                    except NotFoundError:
                        # Skip amenities that don't exist
                        pass
            
            # Save the place
            place.save()
            
            # Update in repository
            facade.place_repository.update(place_id, place.to_dict())
            
            return place.to_dict(), 200
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')
