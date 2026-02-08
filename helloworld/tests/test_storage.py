"""Unit tests for storage classes."""

import pytest
import json
import os
import tempfile
import shutil
from storage import UserStorage


class TestUserStorage:
    """Test suite for UserStorage class."""
    
    def setup_method(self):
        """Set up test fixtures with temporary file."""
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_filepath = os.path.join(self.temp_dir, "test_users.json")
        self.storage = UserStorage(filepath=self.test_filepath)
    
    def teardown_method(self):
        """Clean up test files."""
        # Use shutil.rmtree to remove directory and all contents
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    # Basic functionality tests
    def test_user_exists_returns_false_for_new_user(self):
        """Test that user_exists returns False for non-existent user."""
        assert not self.storage.user_exists("newuser")
    
    def test_save_user_creates_new_user(self):
        """Test saving a new user."""
        self.storage.save_user("testuser", "hashed_password_123")
        assert self.storage.user_exists("testuser")
    
    def test_get_user_returns_none_for_nonexistent_user(self):
        """Test that get_user returns None for non-existent user."""
        result = self.storage.get_user("nonexistent")
        assert result is None
    
    def test_get_user_returns_user_data(self):
        """Test retrieving user data."""
        self.storage.save_user("testuser", "hashed_password_123")
        user = self.storage.get_user("testuser")
        
        assert user is not None
        assert user["username"] == "testuser"
        assert user["password_hash"] == "hashed_password_123"
    
    def test_save_multiple_users(self):
        """Test saving multiple users."""
        self.storage.save_user("user1", "hash1")
        self.storage.save_user("user2", "hash2")
        self.storage.save_user("user3", "hash3")
        
        assert self.storage.user_exists("user1")
        assert self.storage.user_exists("user2")
        assert self.storage.user_exists("user3")
    
    def test_user_exists_after_save(self):
        """Test that user_exists returns True after saving user."""
        self.storage.save_user("testuser", "hashed_password")
        assert self.storage.user_exists("testuser")
    
    # File persistence tests
    def test_load_users_returns_empty_dict_for_missing_file(self):
        """Test that load_users returns empty dict when file doesn't exist."""
        users = self.storage.load_users()
        assert users == {}
    
    def test_save_users_creates_file(self):
        """Test that save_users creates the JSON file."""
        users = {"testuser": {"password_hash": "hash123"}}
        self.storage.save_users(users)
        
        assert os.path.exists(self.test_filepath)
    
    def test_save_and_load_users_round_trip(self):
        """Test that saving and loading users preserves data."""
        original_users = {
            "user1": {"password_hash": "hash1"},
            "user2": {"password_hash": "hash2"}
        }
        
        self.storage.save_users(original_users)
        loaded_users = self.storage.load_users()
        
        assert loaded_users == original_users
    
    def test_data_persists_across_storage_instances(self):
        """Test that data persists when creating new storage instance."""
        # Save with first instance
        self.storage.save_user("testuser", "hash123")
        
        # Create new instance with same filepath
        new_storage = UserStorage(filepath=self.test_filepath)
        
        # Verify data is still there
        assert new_storage.user_exists("testuser")
        user = new_storage.get_user("testuser")
        assert user["password_hash"] == "hash123"
    
    # Error handling tests
    def test_load_users_handles_corrupted_json(self):
        """Test that load_users handles corrupted JSON gracefully."""
        # Write invalid JSON to file
        os.makedirs(os.path.dirname(self.test_filepath), exist_ok=True)
        with open(self.test_filepath, 'w') as f:
            f.write("{ invalid json content }")
        
        # Should return empty dict instead of crashing
        users = self.storage.load_users()
        assert users == {}
    
    def test_load_users_handles_empty_file(self):
        """Test that load_users handles empty file gracefully."""
        # Create empty file
        os.makedirs(os.path.dirname(self.test_filepath), exist_ok=True)
        with open(self.test_filepath, 'w') as f:
            f.write("")
        
        # Should return empty dict instead of crashing
        users = self.storage.load_users()
        assert users == {}
    
    def test_load_users_handles_non_dict_json(self):
        """Test that load_users handles non-dictionary JSON gracefully."""
        # Write valid JSON but not a dictionary
        os.makedirs(os.path.dirname(self.test_filepath), exist_ok=True)
        with open(self.test_filepath, 'w') as f:
            json.dump(["not", "a", "dict"], f)
        
        # Should handle this gracefully
        users = self.storage.load_users()
        # The actual behavior depends on implementation
        # but it should not crash
        assert isinstance(users, (dict, list))
    
    def test_directory_creation(self):
        """Test that storage creates directory if it doesn't exist."""
        nested_path = os.path.join(self.temp_dir, "nested", "dir", "users.json")
        storage = UserStorage(filepath=nested_path)
        
        storage.save_user("testuser", "hash123")
        
        assert os.path.exists(nested_path)
        assert storage.user_exists("testuser")
    
    # Edge cases
    def test_save_user_with_special_characters_in_username(self):
        """Test saving user with special characters in username."""
        username = "user@example.com"
        self.storage.save_user(username, "hash123")
        
        assert self.storage.user_exists(username)
        user = self.storage.get_user(username)
        assert user["username"] == username
    
    def test_save_user_with_unicode_username(self):
        """Test saving user with unicode characters in username."""
        username = "用户名"
        self.storage.save_user(username, "hash123")
        
        assert self.storage.user_exists(username)
        user = self.storage.get_user(username)
        assert user["username"] == username
    
    def test_update_existing_user_password(self):
        """Test that saving existing user updates password hash."""
        self.storage.save_user("testuser", "old_hash")
        self.storage.save_user("testuser", "new_hash")
        
        user = self.storage.get_user("testuser")
        assert user["password_hash"] == "new_hash"
    
    def test_empty_username(self):
        """Test handling of empty username."""
        self.storage.save_user("", "hash123")
        assert self.storage.user_exists("")
        user = self.storage.get_user("")
        assert user["username"] == ""
    
    def test_json_format_is_readable(self):
        """Test that saved JSON is properly formatted and readable."""
        self.storage.save_user("testuser", "hash123")
        
        with open(self.test_filepath, 'r') as f:
            content = f.read()
            data = json.loads(content)
        
        assert "testuser" in data
        assert data["testuser"]["password_hash"] == "hash123"



class TestHistoryStorage:
    """Test suite for HistoryStorage class."""
    
    def setup_method(self):
        """Set up test fixtures with temporary file."""
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_filepath = os.path.join(self.temp_dir, "test_history.json")
        self.storage = None  # Import will be done in tests
    
    def teardown_method(self):
        """Clean up test files."""
        # Use shutil.rmtree to remove directory and all contents
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def _get_storage(self):
        """Get storage instance, importing if needed."""
        if self.storage is None:
            from storage import HistoryStorage
            self.storage = HistoryStorage(filepath=self.test_filepath)
        return self.storage
    
    # Basic functionality tests
    def test_add_calculation_creates_user_history(self):
        """Test adding first calculation for a user."""
        storage = self._get_storage()
        storage.add_calculation("testuser", 5.0, "+", 3.0, 8.0)
        
        history = storage.get_user_history("testuser")
        assert len(history) == 1
        assert history[0]["operand1"] == 5.0
        assert history[0]["operator"] == "+"
        assert history[0]["operand2"] == 3.0
        assert history[0]["result"] == 8.0
        assert "timestamp" in history[0]
    
    def test_add_multiple_calculations(self):
        """Test adding multiple calculations for a user."""
        storage = self._get_storage()
        storage.add_calculation("testuser", 5.0, "+", 3.0, 8.0)
        storage.add_calculation("testuser", 10.0, "-", 4.0, 6.0)
        storage.add_calculation("testuser", 2.0, "*", 3.0, 6.0)
        
        history = storage.get_user_history("testuser")
        assert len(history) == 3
    
    def test_get_user_history_returns_empty_for_new_user(self):
        """Test that get_user_history returns empty list for user with no history."""
        storage = self._get_storage()
        history = storage.get_user_history("newuser")
        assert history == []
    
    def test_history_isolation_between_users(self):
        """Test that different users have isolated histories."""
        storage = self._get_storage()
        storage.add_calculation("user1", 5.0, "+", 3.0, 8.0)
        storage.add_calculation("user2", 10.0, "-", 4.0, 6.0)
        storage.add_calculation("user1", 2.0, "*", 3.0, 6.0)
        
        user1_history = storage.get_user_history("user1")
        user2_history = storage.get_user_history("user2")
        
        assert len(user1_history) == 2
        assert len(user2_history) == 1
        
        # Verify user1's calculations
        assert any(calc["operand1"] == 5.0 for calc in user1_history)
        assert any(calc["operand1"] == 2.0 for calc in user1_history)
        
        # Verify user2's calculation
        assert user2_history[0]["operand1"] == 10.0
    
    def test_history_ordered_by_most_recent_first(self):
        """Test that history is ordered by timestamp with most recent first."""
        storage = self._get_storage()
        
        # Add calculations with slight delay to ensure different timestamps
        import time
        storage.add_calculation("testuser", 1.0, "+", 1.0, 2.0)
        time.sleep(0.01)  # Small delay to ensure different timestamps
        storage.add_calculation("testuser", 2.0, "+", 2.0, 4.0)
        time.sleep(0.01)
        storage.add_calculation("testuser", 3.0, "+", 3.0, 6.0)
        
        history = storage.get_user_history("testuser")
        
        # Most recent should be first (3.0 + 3.0)
        assert history[0]["operand1"] == 3.0
        assert history[1]["operand1"] == 2.0
        assert history[2]["operand1"] == 1.0
    
    # File persistence tests
    def test_load_history_returns_empty_dict_for_missing_file(self):
        """Test that load_history returns empty dict when file doesn't exist."""
        storage = self._get_storage()
        history = storage.load_history()
        assert history == {}
    
    def test_save_history_creates_file(self):
        """Test that save_history creates the JSON file."""
        storage = self._get_storage()
        history = {"testuser": [{"operand1": 5.0, "operator": "+", "operand2": 3.0, "result": 8.0, "timestamp": "2024-01-01T12:00:00"}]}
        storage.save_history(history)
        
        assert os.path.exists(self.test_filepath)
    
    def test_save_and_load_history_round_trip(self):
        """Test that saving and loading history preserves data."""
        storage = self._get_storage()
        original_history = {
            "user1": [
                {"operand1": 5.0, "operator": "+", "operand2": 3.0, "result": 8.0, "timestamp": "2024-01-01T12:00:00"}
            ],
            "user2": [
                {"operand1": 10.0, "operator": "-", "operand2": 4.0, "result": 6.0, "timestamp": "2024-01-01T13:00:00"}
            ]
        }
        
        storage.save_history(original_history)
        loaded_history = storage.load_history()
        
        assert loaded_history == original_history
    
    def test_data_persists_across_storage_instances(self):
        """Test that data persists when creating new storage instance."""
        from storage import HistoryStorage
        
        # Save with first instance
        storage1 = HistoryStorage(filepath=self.test_filepath)
        storage1.add_calculation("testuser", 5.0, "+", 3.0, 8.0)
        
        # Create new instance with same filepath
        storage2 = HistoryStorage(filepath=self.test_filepath)
        
        # Verify data is still there
        history = storage2.get_user_history("testuser")
        assert len(history) == 1
        assert history[0]["operand1"] == 5.0
    
    # Error handling tests
    def test_load_history_handles_corrupted_json(self):
        """Test that load_history handles corrupted JSON gracefully."""
        storage = self._get_storage()
        
        # Write invalid JSON to file
        os.makedirs(os.path.dirname(self.test_filepath), exist_ok=True)
        with open(self.test_filepath, 'w') as f:
            f.write("{ invalid json content }")
        
        # Should return empty dict instead of crashing
        history = storage.load_history()
        assert history == {}
    
    def test_load_history_handles_empty_file(self):
        """Test that load_history handles empty file gracefully."""
        storage = self._get_storage()
        
        # Create empty file
        os.makedirs(os.path.dirname(self.test_filepath), exist_ok=True)
        with open(self.test_filepath, 'w') as f:
            f.write("")
        
        # Should return empty dict instead of crashing
        history = storage.load_history()
        assert history == {}
    
    def test_directory_creation(self):
        """Test that storage creates directory if it doesn't exist."""
        from storage import HistoryStorage
        
        nested_path = os.path.join(self.temp_dir, "nested", "dir", "history.json")
        storage = HistoryStorage(filepath=nested_path)
        
        storage.add_calculation("testuser", 5.0, "+", 3.0, 8.0)
        
        assert os.path.exists(nested_path)
        history = storage.get_user_history("testuser")
        assert len(history) == 1
    
    # Edge cases
    def test_add_calculation_with_negative_numbers(self):
        """Test adding calculation with negative numbers."""
        storage = self._get_storage()
        storage.add_calculation("testuser", -5.0, "+", -3.0, -8.0)
        
        history = storage.get_user_history("testuser")
        assert history[0]["operand1"] == -5.0
        assert history[0]["operand2"] == -3.0
        assert history[0]["result"] == -8.0
    
    def test_add_calculation_with_floating_point_numbers(self):
        """Test adding calculation with floating point numbers."""
        storage = self._get_storage()
        storage.add_calculation("testuser", 5.5, "*", 2.2, 12.1)
        
        history = storage.get_user_history("testuser")
        assert history[0]["operand1"] == 5.5
        assert history[0]["operand2"] == 2.2
        assert history[0]["result"] == 12.1
    
    def test_add_calculation_with_division(self):
        """Test adding division calculation."""
        storage = self._get_storage()
        storage.add_calculation("testuser", 10.0, "/", 2.0, 5.0)
        
        history = storage.get_user_history("testuser")
        assert history[0]["operator"] == "/"
        assert history[0]["result"] == 5.0
    
    def test_json_format_is_readable(self):
        """Test that saved JSON is properly formatted and readable."""
        storage = self._get_storage()
        storage.add_calculation("testuser", 5.0, "+", 3.0, 8.0)
        
        with open(self.test_filepath, 'r') as f:
            content = f.read()
            data = json.loads(content)
        
        assert "testuser" in data
        assert isinstance(data["testuser"], list)
        assert len(data["testuser"]) == 1
        assert data["testuser"][0]["operand1"] == 5.0
    
    def test_multiple_users_with_multiple_calculations(self):
        """Test complex scenario with multiple users and calculations."""
        storage = self._get_storage()
        
        # User 1 calculations
        storage.add_calculation("user1", 1.0, "+", 1.0, 2.0)
        storage.add_calculation("user1", 2.0, "*", 2.0, 4.0)
        
        # User 2 calculations
        storage.add_calculation("user2", 10.0, "-", 5.0, 5.0)
        storage.add_calculation("user2", 20.0, "/", 4.0, 5.0)
        storage.add_calculation("user2", 3.0, "+", 3.0, 6.0)
        
        # User 3 calculations
        storage.add_calculation("user3", 100.0, "*", 2.0, 200.0)
        
        # Verify each user's history
        user1_history = storage.get_user_history("user1")
        user2_history = storage.get_user_history("user2")
        user3_history = storage.get_user_history("user3")
        
        assert len(user1_history) == 2
        assert len(user2_history) == 3
        assert len(user3_history) == 1
