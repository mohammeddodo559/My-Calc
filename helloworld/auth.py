"""Authentication manager for Streamlit Calculator Application.

This module provides user authentication functionality including registration,
login, logout, and session management using bcrypt for password hashing.
"""

import bcrypt
import streamlit as st
from typing import Tuple, Optional
from storage import UserStorage


class AuthManager:
    """Manages user authentication and session state.
    
    Handles user registration, authentication, logout, and session management
    using Streamlit's session state and bcrypt for password hashing.
    
    Attributes:
        user_storage: UserStorage instance for persisting user data
    """
    
    def __init__(self, user_storage: Optional[UserStorage] = None):
        """Initialize AuthManager with storage backend.
        
        Args:
            user_storage: UserStorage instance. If None, creates default instance.
        """
        self.user_storage = user_storage or UserStorage()
        self._initialize_session_state()
    
    def _initialize_session_state(self) -> None:
        """Initialize session state keys if they don't exist."""
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
        if 'username' not in st.session_state:
            st.session_state['username'] = None
    
    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Register a new user with hashed password.
        
        Validates input, checks for duplicate usernames, hashes the password
        using bcrypt, and saves the user to storage.
        
        Args:
            username: Unique username for the new user
            password: Plain text password to be hashed
            
        Returns:
            Tuple of (success: bool, message: str)
            - (True, success_message) if registration successful
            - (False, error_message) if registration failed
        """
        # Validate empty username or password
        if not username or not username.strip():
            return False, "Username cannot be empty"
        
        if not password or not password.strip():
            return False, "Password cannot be empty"
        
        # Check if username already exists
        if self.user_storage.user_exists(username):
            return False, "Username already exists. Please choose a different username."
        
        # Hash the password using bcrypt
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        
        # Save user with hashed password
        self.user_storage.save_user(username, password_hash.decode('utf-8'))
        
        return True, f"Account created successfully for {username}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Authenticate user credentials.
        
        Validates input, retrieves user from storage, verifies password hash,
        and updates session state on successful authentication.
        
        Args:
            username: Username to authenticate
            password: Plain text password to verify
            
        Returns:
            Tuple of (success: bool, message: str)
            - (True, success_message) if authentication successful
            - (False, error_message) if authentication failed
        """
        # Validate empty username or password
        if not username or not username.strip():
            return False, "Username cannot be empty"
        
        if not password or not password.strip():
            return False, "Password cannot be empty"
        
        # Retrieve user from storage
        user = self.user_storage.get_user(username)
        
        if user is None:
            return False, "Invalid credentials. Please check your username and password."
        
        # Verify password against stored hash
        password_bytes = password.encode('utf-8')
        stored_hash = user['password_hash'].encode('utf-8')
        
        if bcrypt.checkpw(password_bytes, stored_hash):
            # Authentication successful - update session state
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            return True, f"Welcome back, {username}!"
        else:
            return False, "Invalid credentials. Please check your username and password."
    
    def logout_user(self) -> None:
        """Clear session state and log out user.
        
        Resets authentication state and clears username from session.
        """
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
    
    def is_authenticated(self) -> bool:
        """Check if current session has authenticated user.
        
        Returns:
            True if user is authenticated, False otherwise
        """
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self) -> Optional[str]:
        """Get username of currently authenticated user.
        
        Returns:
            Username string if authenticated, None otherwise
        """
        if self.is_authenticated():
            return st.session_state.get('username')
        return None
