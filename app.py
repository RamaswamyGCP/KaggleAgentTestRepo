"""
User Management API - Flask Application
WARNING: Contains intentional security vulnerabilities for testing purposes!
"""

from flask import Flask, request, jsonify
import jwt
import datetime
import database
from auth import generate_token, verify_token

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key
SECRET_KEY = "sk_live_12345abcdef_super_secret_key_do_not_share"


@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        # VULNERABILITY: No input validation
        if not username or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # VULNERABILITY: Password stored in plain text
        user_id = database.create_user(username, password, email)
        
        if user_id:
            return jsonify({
                'message': 'User registered successfully',
                'user_id': user_id
            }), 201
        else:
            return jsonify({'error': 'User already exists'}), 409
            
    except Exception as e:
        # VULNERABILITY: Information disclosure through error messages
        return jsonify({'error': str(e), 'traceback': str(e.__traceback__)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Authenticate user
        user = database.authenticate_user(username, password)
        
        if user:
            # Generate JWT token
            token = generate_token(user['id'], SECRET_KEY)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': user
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<username>', methods=['GET'])
def get_user(username):
    """Get user details by username"""
    try:
        # VULNERABILITY: SQL Injection vulnerability
        user = database.get_user_by_username(username)
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/users', methods=['GET'])
def list_users():
    """List all users (requires authentication)"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization token provided'}), 401
        
        # VULNERABILITY: Weak token verification
        token = auth_header.replace('Bearer ', '')
        user_id = verify_token(token, SECRET_KEY)
        
        if not user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Get all users
        users = database.get_all_users()
        return jsonify({'users': users}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/delete/<username>', methods=['DELETE'])
def delete_user(username):
    """Delete a user (admin only)"""
    # VULNERABILITY: No authentication check for admin endpoint!
    try:
        success = database.delete_user(username)
        
        if success:
            return jsonify({'message': f'User {username} deleted'}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # VULNERABILITY: Debug mode enabled
    # VULNERABILITY: Accessible from all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)

