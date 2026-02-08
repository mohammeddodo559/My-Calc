"""
Streamlit Calculator Application

A web-based calculator with iOS-inspired design, user authentication,
and calculation history tracking.
"""

import streamlit as st
from auth import AuthManager
from calculator import Calculator
from storage import HistoryStorage
from ui_renderer import UIRenderer


def initialize_session_state():
    """
    Initialize session state keys on first load.
    
    Sets up all necessary session state variables for authentication,
    view routing, and calculator state.
    
    Requirements: 5.1, 5.3
    """
    # Authentication state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    
    # View routing state
    if 'view' not in st.session_state:
        st.session_state['view'] = 'login'  # Default to login view
    
    # Calculator state
    if 'calc_display' not in st.session_state:
        st.session_state['calc_display'] = '0'
    if 'calc_operand1' not in st.session_state:
        st.session_state['calc_operand1'] = None
    if 'calc_operator' not in st.session_state:
        st.session_state['calc_operator'] = None
    if 'calc_new_number' not in st.session_state:
        st.session_state['calc_new_number'] = True
    
    # Form submission flags
    if 'login_submit' not in st.session_state:
        st.session_state['login_submit'] = False
    if 'signup_submit' not in st.session_state:
        st.session_state['signup_submit'] = False


def handle_calculator_input(calculator: Calculator, history_storage: HistoryStorage, username: str):
    """
    Handle calculator button presses and perform calculations.
    
    Processes number buttons, operator buttons, equals, clear, and scientific functions.
    Saves successful calculations to history.
    
    Args:
        calculator: Calculator instance for performing operations
        history_storage: HistoryStorage instance for saving calculations
        username: Current user's username
    
    Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 3.1, 8.1
    """
    # Handle scientific functions (unary operations)
    if st.session_state.get('calc_sci_function'):
        func = st.session_state['calc_sci_function']
        try:
            current_value = float(st.session_state['calc_display'])
            result, error = calculator.calculate(current_value, func)
            
            if error:
                UIRenderer.show_error(error)
                st.session_state['calc_display'] = '0'
            else:
                if result == int(result):
                    st.session_state['calc_display'] = str(int(result))
                else:
                    st.session_state['calc_display'] = str(round(result, 10))
                st.session_state['calc_new_number'] = True
        except ValueError:
            UIRenderer.show_error("Invalid input")
            st.session_state['calc_display'] = '0'
        
        st.session_state['calc_sci_function'] = None
    
    # Handle number button presses
    if st.session_state.get('calc_number_pressed'):
        number = st.session_state['calc_number_pressed']
        
        # Reset final answer flag when starting new input
        st.session_state['calc_is_final_answer'] = False
        
        if st.session_state['calc_new_number']:
            # Start new number
            st.session_state['calc_display'] = number
            st.session_state['calc_new_number'] = False
        else:
            # Append to existing number
            if st.session_state['calc_display'] == '0':
                st.session_state['calc_display'] = number
            else:
                st.session_state['calc_display'] += number
        
        st.session_state['calc_number_pressed'] = None
    
    # Handle decimal point
    if st.session_state.get('calc_dot_pressed'):
        if '.' not in st.session_state['calc_display']:
            if st.session_state['calc_new_number']:
                st.session_state['calc_display'] = '0.'
                st.session_state['calc_new_number'] = False
            else:
                st.session_state['calc_display'] += '.'
        st.session_state['calc_dot_pressed'] = False
    
    # Handle operator button presses
    if st.session_state.get('calc_operator_pressed'):
        operator = st.session_state['calc_operator_pressed']
        
        # Check if we have a preset operand2 (for x² button)
        if st.session_state.get('calc_operand2_value'):
            try:
                current_value = float(st.session_state['calc_display'])
                operand2 = st.session_state['calc_operand2_value']
                
                result, error = calculator.calculate(current_value, operator, operand2)
                
                if error:
                    UIRenderer.show_error(error)
                    st.session_state['calc_display'] = '0'
                else:
                    if result == int(result):
                        st.session_state['calc_display'] = str(int(result))
                    else:
                        st.session_state['calc_display'] = str(result)
                    st.session_state['calc_new_number'] = True
                
                st.session_state['calc_operand2_value'] = None
            except ValueError:
                UIRenderer.show_error("Invalid input")
                st.session_state['calc_display'] = '0'
        else:
            try:
                current_value = float(st.session_state['calc_display'])
                
                # If there's a pending operation, calculate it first
                if st.session_state['calc_operand1'] is not None and st.session_state['calc_operator'] is not None:
                    operand1 = st.session_state['calc_operand1']
                    prev_operator = st.session_state['calc_operator']
                    
                    result, error = calculator.calculate(operand1, prev_operator, current_value)
                    
                    if error:
                        UIRenderer.show_error(error)
                        st.session_state['calc_display'] = '0'
                        st.session_state['calc_operand1'] = None
                        st.session_state['calc_operator'] = None
                    else:
                        # Format whole numbers without decimal
                        if result == int(result):
                            st.session_state['calc_display'] = str(int(result))
                        else:
                            st.session_state['calc_display'] = str(result)
                        st.session_state['calc_operand1'] = result
                else:
                    st.session_state['calc_operand1'] = current_value
                
                st.session_state['calc_operator'] = operator
                st.session_state['calc_new_number'] = True
                
            except ValueError:
                UIRenderer.show_error("Invalid input. Please enter a valid number.")
                st.session_state['calc_display'] = '0'
                st.session_state['calc_operand1'] = None
                st.session_state['calc_operator'] = None
        
        st.session_state['calc_operator_pressed'] = None
    
    # Handle equals button
    if st.session_state.get('calc_equals_pressed'):
        if st.session_state['calc_operand1'] is not None and st.session_state['calc_operator'] is not None:
            try:
                operand1 = st.session_state['calc_operand1']
                operator = st.session_state['calc_operator']
                operand2 = float(st.session_state['calc_display'])
                
                result, error = calculator.calculate(operand1, operator, operand2)
                
                if error:
                    UIRenderer.show_error(error)
                    st.session_state['calc_display'] = '0'
                    st.session_state['calc_operand1'] = None
                    st.session_state['calc_operator'] = None
                    st.session_state['calc_is_final_answer'] = False
                else:
                    # Display result (format whole numbers without decimal)
                    if result == int(result):
                        st.session_state['calc_display'] = str(int(result))
                    else:
                        st.session_state['calc_display'] = str(result)
                    
                    # Mark as final answer (for bold display)
                    st.session_state['calc_is_final_answer'] = True
                    
                    # Save to history
                    history_storage.add_calculation(username, operand1, operator, operand2, result)
                    
                    # Reset calculator state
                    st.session_state['calc_operand1'] = None
                    st.session_state['calc_operator'] = None
                    st.session_state['calc_new_number'] = True
                    
            except ValueError:
                UIRenderer.show_error("Invalid input. Please enter a valid number.")
                st.session_state['calc_display'] = '0'
                st.session_state['calc_operand1'] = None
                st.session_state['calc_operator'] = None
                st.session_state['calc_is_final_answer'] = False
        
        st.session_state['calc_equals_pressed'] = False


def main():
    """
    Main application entry point.
    
    Handles view routing based on authentication state and user selection.
    Routes to login/signup/calculator views as appropriate.
    Processes authentication forms and updates session state.
    
    Requirements: 2.1, 2.3, 2.4, 2.6, 5.1, 5.2, 5.5
    """
    # Configure page
    st.set_page_config(
        page_title="iOS Calculator",
        page_icon="🧮",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Inject custom CSS
    UIRenderer.inject_custom_css()
    
    # Initialize components
    auth_manager = AuthManager()
    
    # View routing logic
    if not auth_manager.is_authenticated():
        # User is not authenticated - show login or signup
        if st.session_state['view'] == 'signup':
            UIRenderer.render_signup_form()
            
            # Process signup form submission
            if st.session_state.get('signup_submit', False):
                username = st.session_state.get('signup_username_value', '')
                password = st.session_state.get('signup_password_value', '')
                
                success, message = auth_manager.register_user(username, password)
                
                if success:
                    UIRenderer.show_success(message)
                    # Switch to login view after successful registration
                    st.session_state['view'] = 'login'
                    st.session_state['signup_submit'] = False
                    st.rerun()
                else:
                    UIRenderer.show_error(message)
                    st.session_state['signup_submit'] = False
            
            # Display signup error if password mismatch
            if st.session_state.get('signup_error'):
                UIRenderer.show_error(st.session_state['signup_error'])
                st.session_state['signup_error'] = None
        else:
            # Default to login view
            st.session_state['view'] = 'login'
            UIRenderer.render_login_form()
            
            # Process login form submission
            if st.session_state.get('login_submit', False):
                username = st.session_state.get('login_username_value', '')
                password = st.session_state.get('login_password_value', '')
                
                success, message = auth_manager.authenticate_user(username, password)
                
                if success:
                    UIRenderer.show_success(message)
                    st.session_state['login_submit'] = False
                    st.rerun()
                else:
                    UIRenderer.show_error(message)
                    st.session_state['login_submit'] = False
    else:
        # User is authenticated - show calculator interface
        # Compact header with username and logout
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"<h2 style='margin:0;padding:0;'>🧮 {auth_manager.get_current_user()}</h2>", unsafe_allow_html=True)
        with col2:
            if st.button("Logout", type="secondary", use_container_width=True):
                auth_manager.logout_user()
                st.session_state['view'] = 'login'
                st.rerun()
        
        # Initialize calculator and history storage
        calculator = Calculator()
        history_storage = HistoryStorage()
        
        # Process calculator button presses
        handle_calculator_input(calculator, history_storage, auth_manager.get_current_user())
        
        # Render calculator interface
        UIRenderer.render_calculator()
        
        # Load and display user's calculation history
        st.markdown("---")
        user_history = history_storage.get_user_history(auth_manager.get_current_user())
        UIRenderer.render_history(user_history)


if __name__ == "__main__":
    main()
