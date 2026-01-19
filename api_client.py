import os
import requests
from typing import Optional, Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class APIClient:
    """Client for interacting with the API endpoints."""
    
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000/api/v1")
    
    @staticmethod
    def login(username: str, password: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Login and get access token.
        
        Args:
            username: User's username/email
            password: User's password
            
        Returns:
            Tuple of (response_dict, error_message). If successful, response_dict contains
            access_token and token_type. If failed, response_dict is None and error_message
            contains the error description.
        """
        try:
            response = requests.post(
                f"{APIClient.BASE_URL}/login",
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json"
                },
                json={
                    "username": username,
                    "password": password
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e.response, 'text'):
                error_msg = e.response.text
            return None, error_msg
    
    @staticmethod
    def process_query(query: str, thread_id: str, access_token: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Process a chat query.
        
        Args:
            query: User's query
            thread_id: Thread ID for the chat session
            access_token: Bearer token for authentication
            
        Returns:
            Tuple of (response_dict, error_message). If successful, response_dict contains
            the API response. If failed, response_dict is None and error_message contains
            the error description.
        """
        try:
            response = requests.post(
                f"{APIClient.BASE_URL}/process",
                headers={
                    "accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "query": query,
                    "thread_id": thread_id
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_msg = e.response.text
                except:
                    pass
            return None, error_msg

