# iOS-Style Streamlit Calculator

A beautiful web-based calculator application with iOS-inspired design, user authentication, and calculation history tracking.

## Features

✨ **iOS-Inspired Design**
- Smooth animations and transitions
- iOS-style button colors (orange operators, gray numbers)
- Rounded corners and elegant shadows
- Responsive design for mobile and desktop

🔐 **User Authentication**
- Secure user registration with bcrypt password hashing
- Login/logout functionality
- Session management with Streamlit session state

🧮 **Calculator Functionality**
- Basic arithmetic operations: addition, subtraction, multiplication, division
- Decimal number support
- Error handling for division by zero
- Clear button to reset calculations

📊 **Calculation History**
- Automatic saving of all calculations
- Per-user history isolation
- Timestamp tracking
- Most recent calculations displayed first

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

The required packages are:
- streamlit>=1.28.0
- bcrypt>=4.0.0
- hypothesis>=6.82.0 (for testing)
- pytest>=7.4.0 (for testing)

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Calculator

1. **Sign Up**: Create a new account with a username and password
2. **Login**: Enter your credentials to access the calculator
3. **Calculate**: 
   - Click number buttons (0-9) to enter numbers
   - Click operator buttons (+, -, ×, ÷) to select operations
   - Click = to see the result
   - Click C to clear and start over
4. **View History**: Scroll down to see your calculation history
5. **Logout**: Click the Logout button when done

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── auth.py                     # Authentication manager
├── calculator.py               # Calculator engine
├── storage.py                  # Data persistence (JSON files)
├── models.py                   # Data models
├── ui_renderer.py              # UI components and styling
├── requirements.txt            # Python dependencies
├── data/                       # Data storage directory
│   ├── users.json             # User accounts (created automatically)
│   └── history.json           # Calculation history (created automatically)
└── tests/                      # Test files
    ├── test_auth.py
    ├── test_calculator.py
    ├── test_models.py
    ├── test_storage.py
    └── test_ui_renderer.py
```

## Running Tests

Run all tests:
```bash
pytest
```

Run integration test:
```bash
python test_app_integration.py
```

## Architecture

The application follows a clean architecture with separated concerns:

- **UI Layer** (`ui_renderer.py`): Handles all rendering and styling
- **Business Logic** (`auth.py`, `calculator.py`): Core functionality
- **Data Layer** (`storage.py`, `models.py`): Data persistence and models
- **Application** (`app.py`): Orchestrates all components

## Security

- Passwords are hashed using bcrypt before storage
- No plain text passwords are ever stored
- Session state is managed securely through Streamlit
- User data is isolated per account

## Data Storage

User data and calculation history are stored in JSON files in the `data/` directory:
- `users.json`: User accounts with hashed passwords
- `history.json`: Calculation history per user

These files are created automatically on first use.

## Requirements Implemented

This application implements all requirements from the specification:

1. ✅ Basic arithmetic operations (add, subtract, multiply, divide)
2. ✅ User authentication system (register, login, logout)
3. ✅ Calculation history tracking per user
4. ✅ iOS-inspired user interface with animations
5. ✅ Session management
6. ✅ Responsive design for different screen sizes
7. ✅ Data persistence across sessions
8. ✅ Input validation and error handling

## Browser Compatibility

The application works best in modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari

## Troubleshooting

**Issue**: Application won't start
- **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Can't create account
- **Solution**: Check that the `data/` directory is writable

**Issue**: History not showing
- **Solution**: Make sure you're logged in and have performed at least one calculation

## License

This project is part of the Streamlit Calculator specification implementation.

## Contributing

This is a complete implementation of the specification. For modifications or enhancements, please refer to the design document in `.kiro/specs/streamlit-calculator/design.md`.
