"""Unit tests for AuthManager class.

Tests authentication functionality including registration, login, logout,
and session management.
"""

import pytest
import bcrypt
from unittest.mock import MagicMock, patch
from auth import AuthManager
from storage import UserStorage


@pytest.fixture
def mock_storage():
    """Create a mock UserStorage for testing."""
    storage = MagicMock(spec=UserStorage)
    storage.user_exists.return_value = False
    storage.get_user.return_value = None
    return storage


@pytest.fixture
def auth_manager(mock_storage):
    """Create AuthManager with mock storage."""
    with patch('streamlit.session_state', {}):
        manager = AuthManager(user_storage=mock_storage)
        return manager


class TestAuthManagerInitialization:
    """Tests for AuthManager initialization."""
    
    def test_init_with_storage(self, mock_storage):
        """Test initialization with provided storage."""
        with patch('streamlit.session_state', {}):
            manager = AuthManager(user_storage=mock_storage)
            assert manager.user_storage == mock_storage
    
    def test_init_without_storage(self):
        """Test initialization creates default storage."""
        with patch('streamlit.session_state', {}):
            manager = AuthManager()
            assert isinstance(manager.user_storage, UserStorage)
    
    def test_session_state_initialization(self):
        """Test session state is initialized correctly."""
        session_state = {}
        with patch('streamlit.session_state', session_state):
            AuthManager()
            assert 'authenticated' in session_state
            assert session_state['authenticated'] is False
            assert 'username' in session_state
            assert session_state['username'] is None


class TestUserRegistration:
    """Tests for user registration functionality."""
    
    def test_register_user_success(self, auth_manager, mock_storage):
        """Test successful user registration."""
        mock_storage.user_exists.return_value = False
        
        success, message = auth_manager.register_user("testuser", "password123")
        
        assert success is True
        assert "Account created successfully" in message
        assert "testuser" in message
        mock_storage.save_user.assert_called_once()
        
        # Verify password was hashed
        call_args = mock_storage.save_user.call_args
        username, password_hash = call_args[0]
        assert username == "testuser"
        assert password_hash != "password123"  # Should be hashed
        
        # Verify hash is valid bcrypt hash
        assert bcrypt.checkpw(b"password123", password_hash.encode('utf-8'))
    
    def test_register_duplicate_username(self, auth_manager, mock_storage):
        """Test registration with existing username fails."""
        mock_storage.user_exists.return_value = True
        
        success, message = auth_manager.register_user("existinguser", "password123")
        
        assert success is False
        assert "Username already exists" in message
        mock_storage.save_user.assert_not_called()
    
    def test_register_empty_username(self, auth_manager, mock_storage):
        """Test registration with empty username fails."""
        success, message = auth_manager.register_user("", "password123")
        
        assert success is False
        assert "Username cannot be empty" in message
        mock_storage.save_user.assert_not_called()
    
    def test_register_whitespace_username(self, auth_manager, mock_storage):
        """Test registration with whitespace-only username fails."""
        success, message = auth_manager.register_user("   ", "password123")
        
        assert success is False
        assert "Username cannot be empty" in message
        mock_storage.save_user.assert_not_called()
    
    def test_register_empty_password(self, auth_manager, mock_storage):
        """Test registration with empty password fails."""
        success, message = auth_manager.register_user("testuser", "")
        
        assert success is False
        assert "Password cannot be empty" in message
        mock_storage.save_user.assert_not_called()
    
    def test_register_whitespace_password(self, auth_manager, mock_storage):
        """Test registration with whitespace-only password fails."""
        success, message = auth_manager.register_user("testuser", "   ")
        
        assert success is False
        assert "Password cannot be empty" in message
        mock_storage.save_user.assert_not_called()


class TestUserAuthentication:
    """Tests for user authentication functionality."""
    
    def test_authenticate_valid_credentials(self, auth_manager, mock_storage):
        """Test authentication with valid credentials."""
        # Create a valid password hash
        password = "password123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        mock_storage.get_user.return_value = {
            "username": "testuser",
            "password_hash": password_hash.decode('utf-8')
        }
        
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("testuser", password)
        
        assert success is True
        assert "Welcome back" in message
        assert "testuser" in message
        assert session_state['authenticated'] is True
        assert session_state['username'] == "testuser"
    
    def test_authenticate_invalid_password(self, auth_manager, mock_storage):
        """Test authentication with invalid password."""
        # Create a password hash for different password
        correct_password = "password123"
        password_hash = bcrypt.hashpw(correct_password.encode('utf-8'), bcrypt.gensalt())
        
        mock_storage.get_user.return_value = {
            "username": "testuser",
            "password_hash": password_hash.decode('utf-8')
        }
        
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("testuser", "wrongpassword")
        
        assert success is False
        assert "Invalid credentials" in message
        assert session_state['authenticated'] is False
        assert session_state['username'] is None
    
    def test_authenticate_nonexistent_user(self, auth_manager, mock_storage):
        """Test authentication with non-existent username."""
        mock_storage.get_user.return_value = None
        
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("nonexistent", "password123")
        
        assert success is False
        assert "Invalid credentials" in message
        assert session_state['authenticated'] is False
        assert session_state['username'] is None
    
    def test_authenticate_empty_username(self, auth_manager, mock_storage):
        """Test authentication with empty username fails."""
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("", "password123")
        
        assert success is False
        assert "Username cannot be empty" in message
        mock_storage.get_user.assert_not_called()
    
    def test_authenticate_empty_password(self, auth_manager, mock_storage):
        """Test authentication with empty password fails."""
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("testuser", "")
        
        assert success is False
        assert "Password cannot be empty" in message
        mock_storage.get_user.assert_not_called()
    
    def test_authenticate_whitespace_username(self, auth_manager, mock_storage):
        """Test authentication with whitespace-only username fails."""
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("   ", "password123")
        
        assert success is False
        assert "Username cannot be empty" in message
        mock_storage.get_user.assert_not_called()
    
    def test_authenticate_whitespace_password(self, auth_manager, mock_storage):
        """Test authentication with whitespace-only password fails."""
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            success, message = auth_manager.authenticate_user("testuser", "   ")
        
        assert success is False
        assert "Password cannot be empty" in message
        mock_storage.get_user.assert_not_called()


class TestSessionManagement:
    """Tests for session management functionality."""
    
    def test_logout_clears_session(self, auth_manager):
        """Test logout clears session state."""
        session_state = {'authenticated': True, 'username': 'testuser'}
        with patch('streamlit.session_state', session_state):
            auth_manager.logout_user()
        
        assert session_state['authenticated'] is False
        assert session_state['username'] is None
    
    def test_is_authenticated_when_logged_in(self, auth_manager):
        """Test is_authenticated returns True when logged in."""
        session_state = {'authenticated': True, 'username': 'testuser'}
        with patch('streamlit.session_state', session_state):
            assert auth_manager.is_authenticated() is True
    
    def test_is_authenticated_when_logged_out(self, auth_manager):
        """Test is_authenticated returns False when logged out."""
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            assert auth_manager.is_authenticated() is False
    
    def test_is_authenticated_missing_key(self, auth_manager):
        """Test is_authenticated returns False when key missing."""
        session_state = {}
        with patch('streamlit.session_state', session_state):
            assert auth_manager.is_authenticated() is False
    
    def test_get_current_user_when_authenticated(self, auth_manager):
        """Test get_current_user returns username when authenticated."""
        session_state = {'authenticated': True, 'username': 'testuser'}
        with patch('streamlit.session_state', session_state):
            assert auth_manager.get_current_user() == 'testuser'
    
    def test_get_current_user_when_not_authenticated(self, auth_manager):
        """Test get_current_user returns None when not authenticated."""
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            assert auth_manager.get_current_user() is None
    
    def test_get_current_user_missing_username(self, auth_manager):
        """Test get_current_user returns None when username missing."""
        session_state = {'authenticated': True}
        with patch('streamlit.session_state', session_state):
            assert auth_manager.get_current_user() is None


class TestPasswordHashing:
    """Tests for password hashing security."""
    
    def test_password_never_stored_plaintext(self, auth_manager, mock_storage):
        """Test that plain text passwords are never stored."""
        mock_storage.user_exists.return_value = False
        
        auth_manager.register_user("testuser", "mySecretPassword123")
        
        # Get the password hash that was saved
        call_args = mock_storage.save_user.call_args
        _, password_hash = call_args[0]
        
        # Verify it's not the plain text password
        assert password_hash != "mySecretPassword123"
        
        # Verify it's a valid bcrypt hash (starts with $2b$)
        assert password_hash.startswith('$2b$')
    
    def test_same_password_different_hashes(self, auth_manager, mock_storage):
        """Test that same password produces different hashes (due to salt)."""
        mock_storage.user_exists.return_value = False
        
        # Register two users with same password
        auth_manager.register_user("user1", "samepassword")
        hash1 = mock_storage.save_user.call_args[0][1]
        
        auth_manager.register_user("user2", "samepassword")
        hash2 = mock_storage.save_user.call_args[0][1]
        
        # Hashes should be different due to different salts
        assert hash1 != hash2
        
        # But both should verify against the same password
        assert bcrypt.checkpw(b"samepassword", hash1.encode('utf-8'))
        assert bcrypt.checkpw(b"samepassword", hash2.encode('utf-8'))


class TestIntegrationWithRealStorage:
    """Integration tests with real UserStorage."""
    
    def test_full_registration_and_login_flow(self, tmp_path):
        """Test complete registration and login flow with real storage."""
        # Create temporary storage file
        storage_file = tmp_path / "test_users.json"
        storage = UserStorage(filepath=str(storage_file))
        
        session_state = {'authenticated': False, 'username': None}
        with patch('streamlit.session_state', session_state):
            auth_manager = AuthManager(user_storage=storage)
            
            # Register a new user
            success, message = auth_manager.register_user("integrationuser", "testpass123")
            assert success is True
            
            # Verify user exists in storage
            assert storage.user_exists("integrationuser")
            
            # Logout (reset session)
            auth_manager.logout_user()
            assert not auth_manager.is_authenticated()
            
            # Login with correct credentials
            success, message = auth_manager.authenticate_user("integrationuser", "testpass123")
            assert success is True
            assert auth_manager.is_authenticated()
            assert auth_manager.get_current_user() == "integrationuser"
            
            # Logout again
            auth_manager.logout_user()
            assert not auth_manager.is_authenticated()
            assert auth_manager.get_current_user() is None
            
            # Try login with wrong password
            success, message = auth_manager.authenticate_user("integrationuser", "wrongpass")
            assert success is False
            assert not auth_manager.is_authenticated()
