"""
Authentication module for Streamlit dashboard.
Uses streamlit-authenticator to manage user login/logout.
"""
import streamlit as st
import streamlit_authenticator as stauth
import os
from logger_config import get_logger

logger = get_logger(__name__)


def get_auth_config():
    """
    Get authentication configuration from environment variables.
    Format: DASHBOARD_USER_1=username:hashed_password (can have multiple users)
    
    For testing, you can generate hashed passwords using:
    from streamlit_authenticator.utilities import hasher
    hasher.Hasher(['password']).generate()
    """
    # Default credentials for development (MUST be changed in production)
    # Username: admin, Password: admin123
    default_config = {
        "usernames": {
            "admin": {
                "name": "Admin User",
                "password": "$2b$12$YJ0PzKF5LhNvwHbXLhBkJ.w.jEjKpjKWkrFCMNbJH2bHPxXgCKDgW"  # hashed "admin123"
            }
        }
    }
    
    return default_config


def create_authenticator():
    """Initialize the authenticator object."""
    config = get_auth_config()
    
    authenticator = stauth.Authenticate(
        credentials=config["usernames"],
        cookie_name="rsimomentum_auth",
        key="rsimomentum_key_123",  # Should be changed and stored in env var
        cookie_expiry_days=30
    )
    
    return authenticator


def check_authentication():
    """
    Check if user is authenticated. If not, show login form.
    Returns True if authenticated, False otherwise.
    """
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None
    
    if st.session_state.authentication_status is None:
        # Show login form
        authenticator = create_authenticator()
        
        try:
            authenticator.login(location="main", fields={"Form name": "User Login"})
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            st.error("Authentication system error")
            return False
        
        # Update session state based on authentication result
        if st.session_state.get("authentication_status"):
            st.rerun()
        elif st.session_state.get("authentication_status") is False:
            st.error("Username/password is incorrect")
            return False
        else:
            st.warning("Please enter your username and password")
            return False
    
    elif st.session_state.authentication_status:
        # User is authenticated
        return True
    
    else:
        # Authentication failed
        st.error("Authentication failed")
        return False


def show_logout_button():
    """Show logout button in sidebar for authenticated users."""
    if st.session_state.get("authentication_status"):
        authenticator = create_authenticator()
        authenticator.logout(location="sidebar", key="logout_button")


def get_current_user():
    """Get currently logged-in username."""
    return st.session_state.get("username", "unknown")
