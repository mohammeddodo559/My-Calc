"""Storage layer for Streamlit Calculator Application.

This module provides JSON file-based storage for users and calculation history.
"""

import json
import os
from typing import Optional


class UserStorage:
    """JSON file-based storage for user accounts.
    
    Attributes:
        filepath: Path to the JSON file storing user data
    """
    
    def __init__(self, filepath: str = "data/users.json"):
        """Initialize storage with file path.
        
        Args:
            filepath: Path to JSON file for user storage
        """
        self.filepath = filepath
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:
        """Ensure the directory for the storage file exists."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def user_exists(self, username: str) -> bool:
        """Check if username already exists.
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists, False otherwise
        """
        users = self.load_users()
        return username in users
    
    def save_user(self, username: str, password_hash: str) -> None:
        """Save new user with hashed password.
        
        Args:
            username: Username for the new user
            password_hash: Bcrypt hashed password
        """
        users = self.load_users()
        users[username] = {
            "password_hash": password_hash
        }
        self.save_users(users)
    
    def get_user(self, username: str) -> Optional[dict]:
        """Retrieve user data.
        
        Args:
            username: Username to retrieve
            
        Returns:
            Dictionary with username and password_hash, or None if not found
        """
        users = self.load_users()
        if username in users:
            return {
                "username": username,
                "password_hash": users[username]["password_hash"]
            }
        return None
    
    def load_users(self) -> dict:
        """Load all users from storage.
        
        Returns:
            Dictionary mapping usernames to user data.
            Returns empty dict if file doesn't exist or is corrupted.
        """
        if not os.path.exists(self.filepath):
            return {}
        
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # Handle corrupted or unreadable JSON files gracefully
            # Return empty dict to allow application to continue
            print(f"Warning: Could not load users from {self.filepath}: {e}")
            return {}
    
    def save_users(self, users: dict) -> None:
        """Save all users to storage.
        
        Args:
            users: Dictionary mapping usernames to user data
        """
        self._ensure_directory()
        try:
            with open(self.filepath, 'w') as f:
                json.dump(users, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save users to {self.filepath}: {e}")
            raise


class HistoryStorage:
    """JSON file-based storage for calculation history.
    
    Attributes:
        filepath: Path to the JSON file storing calculation history
    """
    
    def __init__(self, filepath: str = "data/history.json"):
        """Initialize storage with file path.
        
        Args:
            filepath: Path to JSON file for history storage
        """
        self.filepath = filepath
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:
        """Ensure the directory for the storage file exists."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def add_calculation(self, username: str, operand1: float, operator: str, 
                       operand2: float, result: float) -> None:
        """Add calculation record for user.
        
        Args:
            username: User who performed calculation
            operand1: First operand
            operator: Operation performed (+, -, *, /)
            operand2: Second operand
            result: Calculation result
        """
        from datetime import datetime
        from models import CalculationRecord
        
        history = self.load_history()
        
        # Initialize user's history list if it doesn't exist
        if username not in history:
            history[username] = []
        
        # Create calculation record
        record = CalculationRecord(
            operand1=operand1,
            operator=operator,
            operand2=operand2,
            result=result,
            timestamp=datetime.now()
        )
        
        # Add to user's history
        history[username].append(record.to_dict())
        
        # Save updated history
        self.save_history(history)
    
    def get_user_history(self, username: str) -> list[dict]:
        """Get calculation history for user, ordered by most recent first.
        
        Args:
            username: User whose history to retrieve
            
        Returns:
            List of calculation records with timestamp, ordered by most recent first
        """
        history = self.load_history()
        
        # Get user's history or empty list if user has no history
        user_history = history.get(username, [])
        
        # Sort by timestamp in descending order (most recent first)
        # Handle both string and datetime timestamps
        sorted_history = sorted(
            user_history,
            key=lambda x: x['timestamp'],
            reverse=True
        )
        
        return sorted_history
    
    def load_history(self) -> dict:
        """Load all history from storage.
        
        Returns:
            Dictionary mapping usernames to lists of calculation records.
            Returns empty dict if file doesn't exist or is corrupted.
        """
        if not os.path.exists(self.filepath):
            return {}
        
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # Handle corrupted or unreadable JSON files gracefully
            # Return empty dict to allow application to continue
            print(f"Warning: Could not load history from {self.filepath}: {e}")
            return {}
    
    def save_history(self, history: dict) -> None:
        """Save all history to storage.
        
        Args:
            history: Dictionary mapping usernames to lists of calculation records
        """
        self._ensure_directory()
        try:
            with open(self.filepath, 'w') as f:
                json.dump(history, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save history to {self.filepath}: {e}")
            raise
