#!/usr/bin/python3
"""
Enhanced WebSocket handler for real-time features in HBNB
"""
import asyncio
import websockets
import json
import jwt
from datetime import datetime
from functools import wraps
from models import storage
from models.user import User
import redis
import logging

# Setup logging
logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages WebSocket connections for real-time features
    """
    
    def __init__(self):
        self.connections = {}
        self.redis_pubsub = None
        self.redis_client = None
        self.setup_redis()
    
    def setup_redis(self):
        """Setup Redis for pub/sub"""
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                db=1,
                decode_responses=True
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info("Redis connected for WebSocket pub/sub")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def authenticate_token(self, token):
        """Authenticate WebSocket connection token"""
        try:
            payload = jwt.decode(
                token,
                'your-secret-key-change-in-production',
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
            user = storage.get(User, user_id)
            return user
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    async def register(self, websocket, user_id):
        """Register a new WebSocket connection"""
        if user_id not in self.connections:
            self.connections[user_id] = set()
        
        self.connections[user_id].add(websocket)
        logger.info(f"User {user_id} connected. Total connections: {len(self.connections)}")
        
        # Send welcome message
        welcome_msg = {
            'type': 'system',
            'message': 'Connected to HBNB WebSocket',
            'timestamp': datetime.utcnow().isoformat(),
            'user_count': len(self.connections)
        }
        await websocket.send(json.dumps(welcome_msg))
    
    async def unregister(self, websocket, user_id):
        """Unregister a WebSocket connection"""
        if user_id in self.connections:
            self.connections[user_id].discard(websocket)
            if not self.connections[user_id]:
                del self.connections[user_id]
        
        logger.info(f"User {user_id} disconnected. Total connections: {len(self.connections)}")
    
    async def send_to_user(self, user_id, message):
        """Send message to specific user"""
        if user_id in self.connections:
            for websocket in self.connections[user_id]:
                try:
                    await websocket.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    logger.warning(f"Connection closed for user {user_id}")
    
    async def broadcast(self, message, exclude_user_id=None):
        """Broadcast message to all connected users"""
        for user_id, connections in self.connections.items():
            if user_id == exclude_user_id:
                continue
            
            for websocket in connections:
                try:
                    await websocket.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    logger.warning(f"Connection closed during broadcast for user {user_id}")
    
    async def handle_message(self, websocket, user, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'chat':
                await self.handle_chat_message(user, data)
            elif msg_type == 'booking_update':
                await self.handle_booking_update(user, data)
            elif msg_type == 'notification_ack':
                await self.handle_notification_ack(user, data)
            elif msg_type == 'typing':
                await self.handle_typing_indicator(user, data)
            else:
                logger.warning(f"Unknown message type: {msg_type}")
        
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            error_msg = {
                'type': 'error',
                'message': 'Invalid JSON format'
            }
            await websocket.send(json.dumps(error_msg))
    
    async def handle_chat_message(self, sender, data):
        """Handle chat messages between users"""
        recipient_id = data.get('recipient_id')
        message = data.get('message')
        
        if not recipient_id or not message:
            return
        
        # Store message in database (simplified)
        chat_data = {
            'sender_id': sender.id,
            'recipient_id': recipient_id,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'chat'
        }
        
        # Send to recipient
        await self.send_to_user(recipient_id, {
            'type': 'chat',
            'sender': {
                'id': sender.id,
                'name': sender.first_name
            },
            'message': message,
            'timestamp': chat_data['timestamp']
        })
        
        # Send delivery confirmation to sender
        await self.send_to_user(sender.id, {
            'type': 'chat_delivered',
            'recipient_id': recipient_id,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        logger.info(f"Chat message from {sender.id} to {recipient_id}")
    
    async def handle_booking_update(self, user, data):
        """Handle booking status updates"""
        booking_id = data.get('booking_id')
        status = data.get('status')
        
        # In a real implementation, update booking in database
        # and notify relevant parties
        
        notification = {
            'type': 'booking_update',
            'booking_id': booking_id,
            'status': status,
            'timestamp': datetime.utcnow().isoformat(),
            'message': f'Booking {booking_id} status updated to {status}'
        }
        
        # Notify user about their booking
        await self.send_to_user(user.id, notification)
        
        # If host needs to be notified, add that logic here
        
        logger.info(f"Booking {booking_id} updated to {status} by user {user.id}")
    
    async def handle_notification_ack(self, user, data):
        """Handle notification acknowledgments"""
        notification_id = data.get('notification_id')
        
        # Mark notification as read in database
        logger.info(f"User {user.id} acknowledged notification {notification_id}")
    
    async def handle_typing_indicator(self, user, data):
        """Handle typing indicators"""
        recipient_id = data.get('recipient_id')
        is_typing = data.get('is_typing', False)
        
        if recipient_id:
            await self.send_to_user(recipient_id, {
                'type': 'typing',
                'user_id': user.id,
                'user_name': user.first_name,
                'is_typing': is_typing,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    async def send_notification(self, user_id, notification):
        """Send notification to user"""
        notification['timestamp'] = datetime.utcnow().isoformat()
        notification['type'] = 'notification'
        
        await self.send_to_user(user_id, notification)
        
        # Store notification in Redis for offline users
        if self.redis_client:
            key = f"notifications:{user_id}"
            self.redis_client.lpush(key, json.dumps(notification))
            self.redis_client.ltrim(key, 0, 99)  # Keep last 100 notifications
    
    async def get_pending_notifications(self, user_id):
        """Get pending notifications for user"""
        if not self.redis_client:
            return []
        
        key = f"notifications:{user_id}"
        notifications = self.redis_client.lrange(key, 0, -1)
        
        # Clear notifications after sending
        self.redis_client.delete(key)
        
        return [json.loads(n) for n in notifications]


# Global WebSocket manager instance
ws_manager = WebSocketManager()


async def websocket_handler(websocket, path):
    """
    Main WebSocket handler function
    """
    user = None
    user_id = None
    
    try:
        # Get authentication token from query parameters
        token = path.split('token=')[-1] if 'token=' in path else None
        
        if not token:
            await websocket.close(1008, "Authentication required")
            return
        
        # Authenticate user
        user = ws_manager.authenticate_token(token)
        if not user:
            await websocket.close(1008, "Invalid token")
            return
        
        user_id = user.id
        
        # Register connection
        await ws_manager.register(websocket, user_id)
        
        # Send pending notifications
        pending_notifications = await ws_manager.get_pending_notifications(user_id)
        for notification in pending_notifications:
            await websocket.send(json.dumps(notification))
        
        # Main message loop
        async for message in websocket:
            await ws_manager.handle_message(websocket, user, message)
    
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e}")
    
    finally:
        # Unregister connection
        if user_id:
            await ws_manager.unregister(websocket, user_id)


async def periodic_broadcast():
    """Periodic broadcast of system stats"""
    while True:
        await asyncio.sleep(60)  # Every minute
        
        stats_message = {
            'type': 'system_stats',
            'timestamp': datetime.utcnow().isoformat(),
            'active_users': len(ws_manager.connections),
            'total_connections': sum(len(conns) for conns in ws_manager.connections.values())
        }
        
        await ws_manager.broadcast(stats_message)


def start_websocket_server():
    """Start WebSocket server"""
    start_server = websockets.serve(
        websocket_handler,
        "localhost",
        8765,
        ping_interval=20,
        ping_timeout=10,
        max_size=2**20  # 1MB max message size
    )
    
    logger.info("Starting WebSocket server on ws://localhost:8765")
    
    # Start periodic broadcast task
    asyncio.get_event_loop().create_task(periodic_broadcast())
    
    return start_server


if __name__ == "__main__":
    # For testing purposes
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(start_websocket_server())
    asyncio.get_event_loop().run_forever()
