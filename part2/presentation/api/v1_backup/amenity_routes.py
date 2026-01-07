"""Amenity API endpoints."""
from flask_restx import Namespace, Resource, fields, reqparse
from business_logic.facade import HBnBFacade
from business_logic.exceptions import ValidationError, NotFoundError

api = Namespace('amenities', description='Amenity operations')

# Request parsers
amenity_parser = reqparse.RequestParser()
amenity_parser.add_argument('name', type=str, required=True, help='Amenity name')
amenity_parser.add_argument('description', type=str, required=False, help='Description')
amenity_parser.add_argument('icon', type=str, required=False, help='Icon name')
amenity_parser.add_argument('category', type=str, required=False, help='Category')

update_amenity_parser = reqparse.RequestParser()
update_amenity_parser.add_argument('name', type=str, required=False, help='Amenity name')
update_amenity_parser.add_argument('description', type=str, required=False, help='Description')
update_amenity_parser.add_argument('icon', type=str, required=False, help='Icon name')
update_amenity_parser.add_argument('category', type=str, required=False, help='Category')

# Response models
amenity_model = api.model('Amenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'description': fields.String(description='Description'),
    'icon': fields.String(description='Icon name'),
    'category': fields.String(description='Category'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

facade = HBnBFacade()

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        """
        Retrieve all amenities.
        
        Returns:
            List of all amenities
        """
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.doc('create_amenity')
    @api.expect(amenity_parser)
    @api.marshal_with(amenity_model, code=201)
    @api.response(400, 'Invalid input')
    def post(self):
        """
        Create a new amenity.
        
        Returns:
            Created amenity data
        """
        args = amenity_parser.parse_args()
        
        try:
            amenity = facade.create_amenity(args)
            return amenity.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """
        Retrieve an amenity by ID.
        
        Args:
            amenity_id: Amenity identifier
            
        Returns:
            Amenity data
        """
        amenity = facade.amenity_repository.get(amenity_id)
        if not amenity:
            api.abort(404, f'Amenity {amenity_id} not found')
        return amenity.to_dict(), 200

    @api.doc('update_amenity')
    @api.expect(update_amenity_parser)
    @api.marshal_with(amenity_model)
    @api.response(400, 'Invalid input')
    def put(self, amenity_id):
        """
        Update amenity information.
        
        Args:
            amenity_id: Amenity identifier
            
        Returns:
            Updated amenity data
        """
        args = update_amenity_parser.parse_args()
        
        # Remove None values
        update_data = {k: v for k, v in args.items() if v is not None}
        
        if not update_data:
            api.abort(400, 'No update data provided')
        
        # Get existing amenity
        amenity = facade.amenity_repository.get(amenity_id)
        if not amenity:
            api.abort(404, f'Amenity {amenity_id} not found')
        
        try:
            # Update amenity attributes
            for key, value in update_data.items():
                if hasattr(amenity, key):
                    setattr(amenity, key, value)
            
            # Save the amenity
            amenity.save()
            
            # Update in repository
            facade.amenity_repository.update(amenity_id, amenity.to_dict())
            
            return amenity.to_dict(), 200
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')
