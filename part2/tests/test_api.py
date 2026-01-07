"""API tests."""
import unittest
import json
from app import create_app
from business_logic.facade import HBnBFacade


class TestAPI(unittest.TestCase):
    """Test cases for API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.facade = HBnBFacade()
    
    def test_api_status(self):
        """Test API status endpoint."""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'OK')
    
    def test_create_user(self):
        """Test user creation."""
        user_data = {
            'email': '11927@holbertonstudents.com',
            'password': '123456',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        response = self.client.post('/api/v1/users/', data=user_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], user_data['email'])
        self.assertEqual(data['first_name'], user_data['first_name'])
        self.assertEqual(data['last_name'], user_data['last_name'])
        self.assertNotIn('password', data)  # Password should not be in response
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        user_data = {
            'email': 'invalid-email',
            'password': '123456',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        response = self.client.post('/api/v1/users/', data=user_data)
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_users(self):
        """Test retrieving all users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_get_user(self):
        """Test retrieving a specific user."""
        # First create a user
        user_data = {
            'email': 'test2@holbertonstudents.com',
            'password': '123456',
            'first_name': 'Jane',
            'last_name': 'Smith'
        }
        
        create_response = self.client.post('/api/v1/users/', data=user_data)
        user_id = json.loads(create_response.data)['id']
        
        # Then retrieve it
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], user_data['email'])
    
    def test_update_user(self):
        """Test updating a user."""
        # First create a user
        user_data = {
            'email': 'test3@holbertonstudents.com',
            'password': '123456',
            'first_name': 'Original',
            'last_name': 'Name'
        }
        
        create_response = self.client.post('/api/v1/users/', data=user_data)
        user_id = json.loads(create_response.data)['id']
        
        # Update the user
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        
        response = self.client.put(f'/api/v1/users/{user_id}', data=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')
    
    def test_create_place(self):
        """Test place creation."""
        # First create a user
        user_data = {
            'email': 'owner@holbertonstudents.com',
            'password': '123456',
            'first_name': 'Owner',
            'last_name': 'User'
        }
        
        user_response = self.client.post('/api/v1/users/', data=user_data)
        user_id = json.loads(user_response.data)['id']
        
        # Create a city (simplified - in real app, cities would be created via API)
        from business_logic.models.city import City
        city = City(name='Test City', state_id='test-state')
        self.facade.city_repository.create(city)
        
        # Create place
        place_data = {
            'user_id': user_id,
            'name': 'Beautiful Apartment in Riyadh',
            'description': 'A lovely apartment in Riyadh city center',
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guest': 4,
            'price_by_night': 100.50,
            'latitude': 24.7136,
            'longitude': 46.6753,
            'city_id': city.id
        }
        
        response = self.client.post('/api/v1/places/', data=place_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], place_data['name'])
        self.assertEqual(float(data['price_by_night']), 100.50)
    
    def test_create_review(self):
        """Test review creation."""
        # Create user
        user_data = {
            'email': 'reviewer@holbertonstudents.com',
            'password': '123456',
            'first_name': 'Reviewer',
            'last_name': 'User'
        }
        
        user_response = self.client.post('/api/v1/users/', data=user_data)
        user_id = json.loads(user_response.data)['id']
        
        # Create place (simplified)
        from business_logic.models.place import Place
        from business_logic.models.city import City
        
        city = City(name='Review City', state_id='test-state')
        self.facade.city_repository.create(city)
        
        place = Place(
            user_id=user_id,
            name='Review Place in Riyadh',
            city_id=city.id,
            number_rooms=1,
            number_bathrooms=1,
            max_guest=2,
            price_by_night=50.00,
            latitude=24.7136,
            longitude=46.6753
        )
        self.facade.place_repository.create(place)
        
        # Create review
        review_data = {
            'user_id': user_id,
            'place_id': place.id,
            'text': 'Great place in Riyadh!',
            'rating': 5
        }
        
        response = self.client.post('/api/v1/reviews/', data=review_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['text'], review_data['text'])
        self.assertEqual(data['rating'], 5)
    
    def test_delete_review(self):
        """Test review deletion."""
        # Create review (simplified)
        from business_logic.models.review import Review
        review = Review(
            user_id='test-user-id',
            place_id='test-place-id',
            text='Test review for Riyadh apartment',
            rating=4
        )
        self.facade.review_repository.create(review)
        
        # Delete review
        response = self.client.delete(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 204)
        
        # Verify deletion
        response = self.client.get(f'/api/v1/reviews/{review.id}')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
