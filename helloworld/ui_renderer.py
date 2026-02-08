"""
UI Renderer module for Streamlit Calculator.

This module provides the UIRenderer class responsible for rendering
the iOS-inspired interface with custom CSS styling and animations.
"""

import streamlit as st
from typing import List, Dict


class UIRenderer:
    """
    Renders iOS-inspired interface with animations and styling.
    
    This class handles all UI rendering including CSS injection,
    forms, calculator interface, and history display.
    """
    
    @staticmethod
    def inject_custom_css() -> None:
        """
        Inject custom CSS for iOS-style design and animations.
        
        Implements iOS-inspired styling with:
        - Rounded corners for buttons
        - Smooth transitions and hover effects
        - iOS color scheme (orange operators, gray numbers)
        - Box shadows for depth
        - Clean typography
        
        Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
        """
        css = """
        <style>
        /* Import professional fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Hide empty containers and spacing */
        .element-container:has(> .stMarkdown > div > .calculator-container) {
            margin-top: -50px;
        }
        
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* Matte Black Background with Subtle Pattern */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(240, 147, 251, 0.03) 0%, transparent 50%),
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255, 255, 255, 0.01) 2px, rgba(255, 255, 255, 0.01) 4px);
            min-height: 100vh;
        }
        
        /* Calculator container - Dark Glass on Black */
        .calculator-container {
            background: 
                linear-gradient(135deg, 
                    rgba(30, 30, 30, 0.95) 0%,
                    rgba(20, 20, 20, 0.98) 100%);
            border-radius: 35px;
            padding: 30px 25px;
            box-shadow: 
                0 20px 60px 0 rgba(0, 0, 0, 0.8),
                0 5px 15px 0 rgba(0, 0, 0, 0.6),
                inset 0 0 0 1px rgba(255, 255, 255, 0.08),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(40px) saturate(200%);
            -webkit-backdrop-filter: blur(40px) saturate(200%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            animation: liquidGlassFloat 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
            max-width: 400px;
            margin: 0 auto;
        }
        
        .calculator-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(
                circle at center,
                rgba(255, 255, 255, 0.3) 0%,
                transparent 70%
            );
            animation: liquidFlow 8s ease-in-out infinite;
            pointer-events: none;
        }
        
        @keyframes liquidFlow {
            0%, 100% {
                transform: translate(0%, 0%) rotate(0deg);
            }
            33% {
                transform: translate(10%, 10%) rotate(120deg);
            }
            66% {
                transform: translate(-10%, 5%) rotate(240deg);
            }
        }
        
        @keyframes liquidGlassFloat {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.95);
                filter: blur(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
                filter: blur(0);
            }
        }
        
        /* Button base - Liquid Glass Effect - Compact */
        .stButton > button {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            border: none;
            font-size: 24px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 
                0 6px 20px rgba(0, 0, 0, 0.3),
                0 2px 6px rgba(0, 0, 0, 0.2),
                inset 0 0 0 1px rgba(255, 255, 255, 0.15),
                inset 0 2px 0 rgba(255, 255, 255, 0.3);
            margin: 3px;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }
        
        /* Liquid ripple effect */
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: radial-gradient(
                circle,
                rgba(255, 255, 255, 0.6) 0%,
                rgba(255, 255, 255, 0.3) 50%,
                transparent 100%
            );
            transform: translate(-50%, -50%);
            transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1), 
                        height 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .stButton > button:active::before {
            width: 400px;
            height: 400px;
            transition: width 0.3s ease-out, height 0.3s ease-out;
        }
        
        /* Liquid shimmer overlay */
        .stButton > button::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.3) 50%,
                transparent 70%
            );
            animation: liquidShimmer 3s ease-in-out infinite;
            pointer-events: none;
        }
        
        @keyframes liquidShimmer {
            0%, 100% {
                transform: translateX(-100%) translateY(-100%) rotate(45deg);
            }
            50% {
                transform: translateX(100%) translateY(100%) rotate(45deg);
            }
        }
        
        /* Number buttons - Dark Liquid Glass */
        .stButton > button[kind="secondary"] {
            background: 
                linear-gradient(135deg,
                    rgba(60, 60, 60, 0.8) 0%,
                    rgba(50, 50, 50, 0.9) 100%);
            color: rgba(255, 255, 255, 0.95);
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: 
                linear-gradient(135deg,
                    rgba(80, 80, 80, 0.9) 0%,
                    rgba(70, 70, 70, 1) 100%);
            transform: translateY(-4px) scale(1.08);
            box-shadow: 
                0 12px 28px rgba(0, 0, 0, 0.5),
                0 4px 12px rgba(0, 0, 0, 0.3),
                inset 0 0 0 1px rgba(255, 255, 255, 0.2),
                inset 0 2px 0 rgba(255, 255, 255, 0.3);
        }
        
        .stButton > button[kind="secondary"]:active {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 
                0 6px 12px rgba(0, 0, 0, 0.12),
                inset 0 2px 6px rgba(0, 0, 0, 0.08);
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Operator buttons - Liquid Orange Glass */
        .stButton > button[kind="primary"] {
            background: 
                linear-gradient(135deg,
                    rgba(255, 149, 0, 0.9) 0%,
                    rgba(255, 107, 0, 0.8) 100%);
            color: #ffffff;
            font-weight: 700;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.25);
            box-shadow: 
                0 8px 24px rgba(255, 149, 0, 0.35),
                0 2px 6px rgba(255, 149, 0, 0.25),
                inset 0 0 0 1px rgba(255, 255, 255, 0.3),
                inset 0 2px 0 rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px) saturate(150%);
            -webkit-backdrop-filter: blur(10px) saturate(150%);
        }
        
        .stButton > button[kind="primary"]:hover {
            background: 
                linear-gradient(135deg,
                    rgba(255, 177, 67, 0.95) 0%,
                    rgba(255, 140, 0, 0.9) 100%);
            transform: translateY(-6px) scale(1.1);
            box-shadow: 
                0 20px 40px rgba(255, 149, 0, 0.45),
                0 6px 16px rgba(255, 149, 0, 0.35),
                inset 0 0 0 1px rgba(255, 255, 255, 0.4),
                inset 0 2px 0 rgba(255, 255, 255, 0.6);
            filter: brightness(1.15) saturate(1.2);
        }
        
        .stButton > button[kind="primary"]:active {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 
                0 8px 16px rgba(255, 149, 0, 0.4),
                inset 0 2px 6px rgba(0, 0, 0, 0.15);
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Special buttons (clear, equals) */
        .stButton > button[kind="tertiary"] {
            background: #a5a5a5;
            color: #ffffff;
        }
        
        .stButton > button[kind="tertiary"]:hover {
            background: #b8b8b8;
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        .stButton > button[kind="tertiary"]:active {
            transform: scale(0.95);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Display area - Dark Liquid Glass with Preview */
        .calculator-display {
            background: 
                linear-gradient(135deg,
                    rgba(40, 40, 40, 0.6) 0%,
                    rgba(30, 30, 30, 0.8) 100%);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: right;
            min-height: 90px;
            box-shadow: 
                inset 0 0 0 1px rgba(255, 255, 255, 0.08),
                inset 0 2px 0 rgba(255, 255, 255, 0.12),
                inset 0 4px 12px rgba(0, 0, 0, 0.4),
                0 2px 8px rgba(0, 0, 0, 0.3);
            transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        /* Expression preview line */
        .expression-preview {
            font-size: 18px;
            font-weight: 400;
            color: rgba(255, 255, 255, 0.5);
            min-height: 22px;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        
        /* Preview answer (before equals) */
        .preview-answer {
            color: rgba(255, 255, 255, 0.4);
            font-size: 16px;
            margin-left: 8px;
        }
        
        /* Main display */
        .main-display {
            font-size: 48px;
            font-weight: 300;
            color: rgba(255, 255, 255, 0.95);
            letter-spacing: 2px;
            transition: all 0.3s ease;
        }
        
        /* Main display when showing final answer (bold) */
        .main-display-bold {
            font-size: 48px;
            font-weight: 700;
            color: rgba(255, 255, 255, 1);
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
            transition: all 0.3s ease;
        }
        
        /* Liquid light reflection */
        .calculator-display::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255, 255, 255, 0.4) 50%,
                transparent 100%
            );
            animation: liquidReflection 4s ease-in-out infinite;
        }
        
        @keyframes liquidReflection {
            0%, 100% {
                left: -100%;
            }
            50% {
                left: 100%;
            }
        }
        
        @keyframes liquidDisplayFloat {
            0%, 100% {
                transform: translateY(0);
                box-shadow: 
                    inset 0 0 0 1px rgba(255, 255, 255, 0.3),
                    inset 0 2px 0 rgba(255, 255, 255, 0.5),
                    inset 0 -2px 8px rgba(0, 0, 0, 0.05),
                    0 4px 16px rgba(0, 0, 0, 0.08);
            }
            50% {
                transform: translateY(-2px);
                box-shadow: 
                    inset 0 0 0 1px rgba(255, 255, 255, 0.4),
                    inset 0 2px 0 rgba(255, 255, 255, 0.6),
                    inset 0 -2px 8px rgba(0, 0, 0, 0.05),
                    0 8px 24px rgba(102, 126, 234, 0.15);
            }
        }
        
        .calculator-display:hover {
            transform: scale(1.01) translateY(-3px);
            box-shadow: 
                inset 0 0 0 1px rgba(255, 255, 255, 0.4),
                inset 0 2px 0 rgba(255, 255, 255, 0.6),
                inset 0 -2px 8px rgba(0, 0, 0, 0.05),
                0 12px 32px rgba(102, 126, 234, 0.2);
        }
        
        /* Input fields - Premium style */
        .stTextInput > div > div > input {
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 16px 20px;
            font-size: 17px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 
                0 4px 12px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            font-weight: 500;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 
                0 0 0 4px rgba(102, 126, 234, 0.2),
                0 8px 24px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            outline: none;
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 1);
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(0, 0, 0, 0.4);
            font-weight: 400;
        }
        
        /* Form buttons - Premium gradient */
        .stForm button[type="submit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            border: none;
            border-radius: 15px;
            padding: 18px 32px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            width: 100%;
            box-shadow: 
                0 8px 20px rgba(102, 126, 234, 0.4),
                0 2px 4px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        
        .stForm button[type="submit"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .stForm button[type="submit"]:hover::before {
            left: 100%;
        }
        
        .stForm button[type="submit"]:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            transform: translateY(-4px) scale(1.02);
            box-shadow: 
                0 16px 32px rgba(102, 126, 234, 0.5),
                0 4px 8px rgba(102, 126, 234, 0.4),
                inset 0 2px 0 rgba(255, 255, 255, 0.4);
        }
        
        .stForm button[type="submit"]:active {
            transform: translateY(-1px) scale(1);
            box-shadow: 
                0 6px 12px rgba(102, 126, 234, 0.4),
                inset 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        /* History container - Glass morphism */
        .history-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 25px;
            padding: 30px;
            margin-top: 30px;
            box-shadow: 
                0 8px 32px 0 rgba(31, 38, 135, 0.37),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: containerFadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s backwards;
        }
        
        /* History items with stagger animation */
        .history-item {
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(240, 240, 240, 0.9));
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            border-left: 5px solid transparent;
            border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
            box-shadow: 
                0 4px 12px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.8);
            animation: historyItemSlide 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
        }
        
        @keyframes historyItemSlide {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .history-item:hover {
            background: linear-gradient(145deg, rgba(255, 255, 255, 1), rgba(250, 250, 250, 1));
            transform: translateX(10px) scale(1.02);
            box-shadow: 
                0 12px 24px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 1);
            border-left-width: 8px;
        }
        
        /* Success and error messages */
        .stSuccess {
            background: #34c759;
            color: #ffffff;
            border-radius: 10px;
            padding: 12px 16px;
            animation: slideIn 0.3s ease;
        }
        
        .stError {
            background: #ff3b30;
            color: #ffffff;
            border-radius: 10px;
            padding: 12px 16px;
            animation: slideIn 0.3s ease;
        }
        
        /* Animations */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        /* Disable text selection on UI elements */
        .stButton > button,
        .calculator-display,
        h1, h2, h3 {
            user-select: none;
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
        }
        
        /* Header styling - Clean white on black */
        h1, h2, h3 {
            color: rgba(255, 255, 255, 0.95);
            font-weight: 700;
            animation: fadeInDown 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            text-shadow: 
                0 2px 8px rgba(0, 0, 0, 0.5),
                0 4px 16px rgba(102, 126, 234, 0.2);
            letter-spacing: -0.5px;
        }
        
        /* Hide extra spacing elements */
        .stMarkdown p {
            margin: 0 !important;
        }
        
        /* Compact column spacing */
        [data-testid="column"] {
            padding: 0 !important;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Card styling - Apple Liquid Glass */
        .auth-card {
            background: 
                linear-gradient(135deg,
                    rgba(255, 255, 255, 0.25) 0%,
                    rgba(255, 255, 255, 0.1) 100%);
            border-radius: 40px;
            padding: 55px;
            box-shadow: 
                0 8px 32px 0 rgba(0, 0, 0, 0.1),
                0 2px 8px 0 rgba(0, 0, 0, 0.05),
                inset 0 0 0 1px rgba(255, 255, 255, 0.3),
                inset 0 2px 0 0 rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(40px) saturate(200%);
            -webkit-backdrop-filter: blur(40px) saturate(200%);
            border: 1px solid rgba(255, 255, 255, 0.2);
            animation: liquidCardEntrance 1s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }
        
        .auth-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(
                circle at center,
                rgba(255, 255, 255, 0.2) 0%,
                transparent 70%
            );
            animation: liquidCardFlow 10s ease-in-out infinite;
            pointer-events: none;
        }
        
        @keyframes liquidCardFlow {
            0%, 100% {
                transform: translate(0%, 0%) scale(1);
            }
            50% {
                transform: translate(20%, 20%) scale(1.2);
            }
        }
        
        @keyframes liquidCardEntrance {
            from {
                opacity: 0;
                transform: translateY(50px) scale(0.9);
                filter: blur(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
                filter: blur(0);
            }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .stButton > button {
                width: 60px;
                height: 60px;
                font-size: 20px;
                margin: 3px;
            }
            
            .calculator-display {
                font-size: 36px;
                padding: 15px;
                min-height: 60px;
            }
            
            .auth-card {
                padding: 30px 20px;
            }
        }
        
        @media (max-width: 480px) {
            .stButton > button {
                width: 50px;
                height: 50px;
                font-size: 18px;
                margin: 2px;
            }
            
            .calculator-display {
                font-size: 28px;
                padding: 12px;
                min-height: 50px;
            }
        }
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def render_login_form() -> None:
        """
        Render login form with styling.

        Creates a styled login form with username and password inputs,
        submit button, and link to switch to signup view.

        Requirements: 2.3, 2.4, 8.2, 8.3
        """
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("🔐 Login")

        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login")

            if submit:
                # Store credentials in session state for processing
                st.session_state['login_submit'] = True
                st.session_state['login_username_value'] = username
                st.session_state['login_password_value'] = password

        # Link to signup
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Don't have an account?")
        with col2:
            if st.button("Sign Up"):
                st.session_state['view'] = 'signup'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    
    @staticmethod
    def render_signup_form() -> None:
        """
        Render signup form with styling.
        
        Creates a styled signup form with username and password inputs,
        submit button, and link to switch to login view.
        
        Requirements: 2.1, 8.2, 8.3
        """
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("📝 Sign Up")
        
        with st.form("signup_form"):
            username = st.text_input("Username", key="signup_username")
            password = st.text_input("Password", type="password", key="signup_password")
            password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
            submit = st.form_submit_button("Create Account")
            
            if submit:
                # Validate password confirmation
                if password != password_confirm:
                    st.session_state['signup_error'] = "Passwords do not match"
                else:
                    # Store credentials in session state for processing
                    st.session_state['signup_submit'] = True
                    st.session_state['signup_username_value'] = username
                    st.session_state['signup_password_value'] = password
        
        # Link to login
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Already have an account?")
        with col2:
            if st.button("Login"):
                st.session_state['view'] = 'login'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_calculator() -> None:
        """
        Render calculator interface with iOS-style buttons.
        
        Creates an iOS-inspired calculator interface with:
        - Number buttons (0-9)
        - Operator buttons (+, -, *, /)
        - Equals button and clear button
        - Display area for current calculation
        - Toggle for scientific mode
        
        Requirements: 1.1, 1.2, 1.3, 1.4, 4.1
        """
        st.markdown('<div class="calculator-container">', unsafe_allow_html=True)
        
        # Initialize calculator state if not exists
        if 'calc_display' not in st.session_state:
            st.session_state['calc_display'] = '0'
        if 'calc_operand1' not in st.session_state:
            st.session_state['calc_operand1'] = None
        if 'calc_operator' not in st.session_state:
            st.session_state['calc_operator'] = None
        if 'calc_new_number' not in st.session_state:
            st.session_state['calc_new_number'] = True
        if 'scientific_mode' not in st.session_state:
            st.session_state['scientific_mode'] = False
        
        # Toggle button for scientific mode - Compact
        if st.session_state['scientific_mode']:
            mode_btn = st.button("📱 Basic", key="mode_toggle", type="secondary", use_container_width=True)
        else:
            mode_btn = st.button("🔬 Scientific", key="mode_toggle", type="primary", use_container_width=True)
        
        if mode_btn:
            st.session_state['scientific_mode'] = not st.session_state['scientific_mode']
            st.rerun()
        
        # Display area with expression preview and live answer
        # Build expression preview
        expression_preview = ""
        preview_answer = ""
        is_final_answer = st.session_state.get('calc_is_final_answer', False)
        
        if st.session_state.get('calc_operand1') is not None:
            op1 = st.session_state['calc_operand1']
            if op1 == int(op1):
                expression_preview = str(int(op1))
            else:
                expression_preview = str(op1)
            
            if st.session_state.get('calc_operator'):
                operator_display = st.session_state['calc_operator']
                if operator_display == '*':
                    operator_display = '×'
                elif operator_display == '/':
                    operator_display = '÷'
                elif operator_display == '^':
                    operator_display = 'ʸ'
                expression_preview += f" {operator_display} "
                
                # Show second operand if we're entering it
                if not st.session_state.get('calc_new_number', True):
                    expression_preview += st.session_state['calc_display']
                    
                    # Calculate live preview
                    try:
                        from calculator import Calculator
                        calc = Calculator()
                        op2 = float(st.session_state['calc_display'])
                        result, error = calc.calculate(op1, st.session_state['calc_operator'], op2)
                        if result is not None and not error:
                            if result == int(result):
                                preview_answer = f"= {int(result)}"
                            else:
                                preview_answer = f"= {result}"
                    except:
                        pass
        
        # Determine if we should show bold (final answer)
        display_class = "main-display-bold" if is_final_answer else "main-display"
        
        st.markdown(
            f'''<div class="calculator-display">
                <div class="expression-preview">{expression_preview} <span class="preview-answer">{preview_answer}</span></div>
                <div class="{display_class}">{st.session_state["calc_display"]}</div>
            </div>''',
            unsafe_allow_html=True
        )
        
        if st.session_state['scientific_mode']:
            # Scientific Calculator Layout
            # Row 1: Scientific functions
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                if st.button("sin", key="btn_sin", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = 'sin'
                    st.rerun()
            with col2:
                if st.button("cos", key="btn_cos", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = 'cos'
                    st.rerun()
            with col3:
                if st.button("tan", key="btn_tan", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = 'tan'
                    st.rerun()
            with col4:
                if st.button("√", key="btn_sqrt", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = 'sqrt'
                    st.rerun()
            with col5:
                if st.button("x²", key="btn_square", type="primary", use_container_width=True):
                    st.session_state['calc_operator_pressed'] = '^'
                    st.session_state['calc_operand2_value'] = 2
                    st.rerun()
            
            # Row 2: More scientific functions
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                if st.button("ln", key="btn_ln", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = 'ln'
                    st.rerun()
            with col2:
                if st.button("log", key="btn_log", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = 'log'
                    st.rerun()
            with col3:
                if st.button("x!", key="btn_factorial", type="primary", use_container_width=True):
                    st.session_state['calc_sci_function'] = '!'
                    st.rerun()
            with col4:
                if st.button("xʸ", key="btn_power", type="primary", use_container_width=True):
                    st.session_state['calc_operator_pressed'] = '^'
                    st.rerun()
            with col5:
                if st.button("π", key="btn_pi", type="secondary", use_container_width=True):
                    st.session_state['calc_number_pressed'] = '3.14159265359'
                    st.rerun()
        
        # Standard calculator buttons
        # Row 1: Clear and operators
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("C", key="btn_clear", type="tertiary", use_container_width=True):
                st.session_state['calc_display'] = '0'
                st.session_state['calc_operand1'] = None
                st.session_state['calc_operator'] = None
                st.session_state['calc_new_number'] = True
                st.rerun()
        with col2:
            st.write("")  # Empty space
        with col3:
            st.write("")  # Empty space
        with col4:
            if st.button("÷", key="btn_div", type="primary", use_container_width=True):
                st.session_state['calc_operator_pressed'] = '/'
                st.rerun()
        
        # Row 2: 7, 8, 9, *
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("7", key="btn_7", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '7'
                st.rerun()
        with col2:
            if st.button("8", key="btn_8", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '8'
                st.rerun()
        with col3:
            if st.button("9", key="btn_9", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '9'
                st.rerun()
        with col4:
            if st.button("×", key="btn_mul", type="primary", use_container_width=True):
                st.session_state['calc_operator_pressed'] = '*'
                st.rerun()
        
        # Row 3: 4, 5, 6, -
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("4", key="btn_4", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '4'
                st.rerun()
        with col2:
            if st.button("5", key="btn_5", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '5'
                st.rerun()
        with col3:
            if st.button("6", key="btn_6", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '6'
                st.rerun()
        with col4:
            if st.button("−", key="btn_sub", type="primary", use_container_width=True):
                st.session_state['calc_operator_pressed'] = '-'
                st.rerun()
        
        # Row 4: 1, 2, 3, +
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("1", key="btn_1", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '1'
                st.rerun()
        with col2:
            if st.button("2", key="btn_2", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '2'
                st.rerun()
        with col3:
            if st.button("3", key="btn_3", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '3'
                st.rerun()
        with col4:
            if st.button("+", key="btn_add", type="primary", use_container_width=True):
                st.session_state['calc_operator_pressed'] = '+'
                st.rerun()
        
        # Row 5: 0, ., =
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("0", key="btn_0", type="secondary", use_container_width=True):
                st.session_state['calc_number_pressed'] = '0'
                st.rerun()
        with col2:
            if st.button(".", key="btn_dot", type="secondary", use_container_width=True):
                st.session_state['calc_dot_pressed'] = True
                st.rerun()
        with col3:
            st.write("")  # Empty space
        with col4:
            if st.button("=", key="btn_equals", type="primary", use_container_width=True):
                st.session_state['calc_equals_pressed'] = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def render_history(history: List[Dict]) -> None:
        """
        Render calculation history with formatting.
        
        Displays calculation records with expression, result, and timestamp.
        Shows appropriate message for empty history.
        
        Args:
            history: List of calculation records to display
        
        Requirements: 3.2, 3.3, 3.4, 3.5
        """
        st.markdown('<div class="history-container">', unsafe_allow_html=True)
        st.subheader("📊 Calculation History")
        
        if not history or len(history) == 0:
            # Display message for empty history
            st.info("No calculations yet. Start calculating to see your history!")
        else:
            # Display each calculation record
            for record in history:
                operand1 = record['operand1']
                operator = record['operator']
                operand2 = record['operand2']
                result = record['result']
                timestamp = record['timestamp']
                
                # Format the expression
                expression = f"{operand1} {operator} {operand2} = {result}"
                
                # Format timestamp (handle both string and datetime)
                if isinstance(timestamp, str):
                    # Parse ISO format timestamp
                    from datetime import datetime
                    try:
                        dt = datetime.fromisoformat(timestamp)
                        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        time_str = timestamp
                else:
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # Display as styled history item
                st.markdown(
                    f'<div class="history-item">'
                    f'<strong>{expression}</strong><br>'
                    f'<small style="color: #666;">{time_str}</small>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    @staticmethod
    def show_error(message: str) -> None:
        """
        Display error message with styling.
        
        Args:
            message: Error message to display
        """
        st.error(message)
    
    @staticmethod
    def show_success(message: str) -> None:
        """
        Display success message with styling.
        
        Args:
            message: Success message to display
        """
        st.success(message)
