import time
import secrets

class SessionManager:
    def __init__(self):
        """Initialize a new session manager with default values"""
        self.current_user = None    # Stores authenticated user's data
        self.logged_in = False      # Tracks login status
        self.session_token = None   # Unique token for the session
        self.session_start_time = None  # Timestamp when session started
        self.session_timeout = 3600  # Session expires after 1 hour (in seconds)

    def start_session(self, user_data):
        """Start a new session with user data
        
        Args:
            user_data: Dictionary containing user information to store in session
            
        Returns:
            str: Generated session token that should be sent to client
        """
        self.current_user = user_data
        self.logged_in = True
        # Generate cryptographically secure random token
        self.session_token = secrets.token_urlsafe(32)  
        self.session_start_time = time.time()
        return self.session_token

    def end_session(self):
        """Terminate the current session and clear all session data"""
        self.current_user = None
        self.logged_in = False
        self.session_token = None
        self.session_start_time = None

    def is_authenticated(self, token=None):
        """Verify if the session is valid and optionally check token match
        
        Args:
            token: Optional session token to validate against stored token
            
        Returns:
            bool: True if session is valid, False otherwise
        """
        if not self.logged_in:
            return False
            
        # Check if session has expired based on timeout
        if self.session_start_time and time.time() - self.session_start_time > self.session_timeout:
            self.end_session()  # Automatically clean up expired session
            return False
            
        # Optional token verification if provided
        if token and token != self.session_token:
            return False
            
        return True

    def get_current_user(self):
        """Retrieve current authenticated user's data
        
        Returns:
            dict/None: User data if session is active, None otherwise
        """
        return self.current_user if self.logged_in else None