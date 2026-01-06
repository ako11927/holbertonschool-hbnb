"""User API endpoints."""
from flask_restx import Namespace, Resource, fields, reqparse
from business_logic.facade import HBnBFacade
from business_logic.exceptions import ValidationError, NotFoundError, DuplicateError

api = Namespace('users', description='User operations')

# Request parsers
user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help='Email address')
user_parser.add_argument('password', type=str, required=True, help='Password')
user_parser.add_argument('first_name', type=str, required=False, help='First name')
user_parser.add_argument('last_name', type=str, required=False, help='Last name')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('email', type=str, required=False, help='Email address')
update_user_parser.add_argument('password', type=str, required=False, help='Password')
update_user_parser.add_argument('first_name', type=str, required=False, help='First name')
update_user_parser.add_argument('last_name', type=str, required=False, help='Last name')

# Response models
user_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'full_name': fields.String(description='Full name'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """
        Retrieve all users.
        
        Returns:
            List of all users
        """
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.doc('create_user')
    @api.expect(user_parser)
    @api.marshal_with(user_model, code=201)
    @api.response(400, 'Invalid input')
    @api.response(409, 'User already exists')
    def post(self):
        """
        Create a new user.
        
        Returns:
            Created user data
        """
        args = user_parser.parse_args()
        
        try:
            user = facade.create_user(args)
            return user.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except DuplicateError as e:
            api.abort(409, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """
        Retrieve a user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            User data
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f'User {user_id} not found')
        return user.to_dict(), 200

    @api.doc('update_user')
    @api.expect(update_user_parser)
    @api.marshal_with(user_model)
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        """
        Update user information.
        
        Args:
            user_id: User identifier
            
        Returns:
            Updated user data
        """
        args = update_user_parser.parse_args()
        
        # Remove None values
        update_data = {k: v for k, v in args.items() if v is not None}
        
        if not update_data:
            api.abort(400, 'No update data provided')
        
        # Get existing user
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f'User {user_id} not found')
        
        try:
            # Update user attributes
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            # Save the user
            user.save()
            
            # Update in repository
            facade.user_repository.update(user_id, user.to_dict())
            
            return user.to_dict(), 200
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')
