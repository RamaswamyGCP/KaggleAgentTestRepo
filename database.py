"""
Database operations for User Management API
WARNING: Contains intentional SQL injection vulnerabilities!
"""

import sqlite3
import os


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database with users table"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def create_user(username, password, email):
    """Create a new user"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # VULNERABILITY: Password stored in plain text
        cursor.execute(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, password, email)
        )
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
        
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username):
    """
    Get user details by username
    VULNERABILITY: SQL Injection vulnerability!
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # CRITICAL VULNERABILITY: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    user = cursor.execute(query).fetchone()
    conn.close()
    
    if user:
        return dict(user)
    return None


def authenticate_user(username, password):
    """Authenticate user with username and password"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Plain text password comparison
    user = cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    
    conn.close()
    
    if user:
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    return None


def get_all_users():
    """Get all users from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    users = cursor.execute('SELECT id, username, email, created_at FROM users').fetchall()
    conn.close()
    
    return [dict(user) for user in users]


def delete_user(username):
    """Delete a user by username"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # VULNERABILITY: Another SQL injection point
    query = f"DELETE FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0


# Initialize database on import
init_database()

