"""
Quick integration test to verify the app components work together.
"""

import os
import json
from auth import AuthManager
from calculator import Calculator
from storage import UserStorage, HistoryStorage
from models import CalculationRecord
from datetime import datetime


def test_complete_flow():
    """Test the complete user flow: register, login, calculate, view history."""
    
    # Clean up test files if they exist
    test_user_file = "data/test_users.json"
    test_history_file = "data/test_history.json"
    
    for file in [test_user_file, test_history_file]:
        if os.path.exists(file):
            os.remove(file)
    
    # Initialize components with test files
    user_storage = UserStorage(test_user_file)
    history_storage = HistoryStorage(test_history_file)
    auth_manager = AuthManager(user_storage)
    calculator = Calculator()
    
    # Test 1: Register a new user
    print("Test 1: User Registration")
    success, message = auth_manager.register_user("testuser", "testpass123")
    assert success, f"Registration failed: {message}"
    print(f"✓ {message}")
    
    # Test 2: Try to register duplicate user
    print("\nTest 2: Duplicate Registration Prevention")
    success, message = auth_manager.register_user("testuser", "anotherpass")
    assert not success, "Duplicate registration should fail"
    assert "already exists" in message.lower()
    print(f"✓ {message}")
    
    # Test 3: Login with correct credentials
    print("\nTest 3: User Login")
    success, message = auth_manager.authenticate_user("testuser", "testpass123")
    assert success, f"Login failed: {message}"
    assert auth_manager.is_authenticated()
    assert auth_manager.get_current_user() == "testuser"
    print(f"✓ {message}")
    
    # Test 4: Perform calculations
    print("\nTest 4: Calculator Operations")
    
    # Addition
    result, error = calculator.calculate(5, '+', 3)
    assert error is None, f"Addition failed: {error}"
    assert result == 8, f"Expected 8, got {result}"
    print(f"✓ 5 + 3 = {result}")
    
    # Subtraction
    result, error = calculator.calculate(10, '-', 4)
    assert error is None, f"Subtraction failed: {error}"
    assert result == 6, f"Expected 6, got {result}"
    print(f"✓ 10 - 4 = {result}")
    
    # Multiplication
    result, error = calculator.calculate(7, '*', 6)
    assert error is None, f"Multiplication failed: {error}"
    assert result == 42, f"Expected 42, got {result}"
    print(f"✓ 7 * 6 = {result}")
    
    # Division
    result, error = calculator.calculate(20, '/', 4)
    assert error is None, f"Division failed: {error}"
    assert result == 5, f"Expected 5, got {result}"
    print(f"✓ 20 / 4 = {result}")
    
    # Division by zero
    result, error = calculator.calculate(10, '/', 0)
    assert result is None, "Division by zero should return None"
    assert error is not None, "Division by zero should return error"
    print(f"✓ Division by zero error: {error}")
    
    # Test 5: Save calculations to history
    print("\nTest 5: History Storage")
    history_storage.add_calculation("testuser", 5, '+', 3, 8)
    history_storage.add_calculation("testuser", 10, '-', 4, 6)
    history_storage.add_calculation("testuser", 7, '*', 6, 42)
    print("✓ Added 3 calculations to history")
    
    # Test 6: Retrieve user history
    print("\nTest 6: History Retrieval")
    history = history_storage.get_user_history("testuser")
    assert len(history) == 3, f"Expected 3 history items, got {len(history)}"
    print(f"✓ Retrieved {len(history)} history items")
    
    # Verify history is ordered by most recent first
    # (Most recent should be the multiplication)
    assert history[0]['operand1'] == 7
    assert history[0]['operator'] == '*'
    print("✓ History is ordered correctly (most recent first)")
    
    # Test 7: History isolation (different user)
    print("\nTest 7: History Isolation")
    auth_manager.register_user("user2", "pass2")
    history_storage.add_calculation("user2", 1, '+', 1, 2)
    
    user1_history = history_storage.get_user_history("testuser")
    user2_history = history_storage.get_user_history("user2")
    
    assert len(user1_history) == 3, "User 1 should have 3 items"
    assert len(user2_history) == 1, "User 2 should have 1 item"
    print("✓ History is properly isolated between users")
    
    # Test 8: Logout
    print("\nTest 8: User Logout")
    auth_manager.logout_user()
    assert not auth_manager.is_authenticated()
    assert auth_manager.get_current_user() is None
    print("✓ User logged out successfully")
    
    # Test 9: Data persistence
    print("\nTest 9: Data Persistence")
    
    # Create new instances to simulate app restart
    new_user_storage = UserStorage(test_user_file)
    new_history_storage = HistoryStorage(test_history_file)
    
    # Verify user data persisted
    user = new_user_storage.get_user("testuser")
    assert user is not None, "User data should persist"
    print("✓ User data persisted across restart")
    
    # Verify history data persisted
    history = new_history_storage.get_user_history("testuser")
    assert len(history) == 3, "History should persist"
    print("✓ History data persisted across restart")
    
    # Clean up test files
    for file in [test_user_file, test_history_file]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED!")
    print("="*50)
    print("\nThe Streamlit Calculator app is ready to use!")
    print("Run it with: streamlit run app.py")


if __name__ == "__main__":
    test_complete_flow()
