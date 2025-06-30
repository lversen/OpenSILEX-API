"""
OpenSilex API Client - Base Module
Provides foundational classes for interacting with the OpenSilex API
"""

import requests
import json
import logging
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin
from dataclasses import dataclass
from enum import Enum


class APIException(Exception):
    """Custom exception for API errors"""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class HTTPMethod(Enum):
    """HTTP methods enumeration"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class APIResponse:
    """Standard API response wrapper"""
    success: bool
    data: Any
    status_code: int
    message: str = None
    errors: List[str] = None


class BaseAPIClient:
    """
    Base client for OpenSilex API operations
    Handles authentication, request formation, and response parsing
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the OpenSilex API
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.auth_token: Optional[str] = None
        self.logger = self._setup_logger()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Language': 'en'
        })
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for the client"""
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def authenticate(self, identifier: str, password: str) -> APIResponse:
        """
        Authenticate with the OpenSilex API
        
        Args:
            identifier: User identifier (email/username)
            password: User password
            
        Returns:
            APIResponse with authentication token
        """
        auth_data = {
            "identifier": identifier,
            "password": password
        }
        
        try:
            response = self._make_request(
                method=HTTPMethod.POST,
                endpoint="/security/authenticate",
                data=auth_data,
                require_auth=False
            )
            
            if response.success and response.data:
                # Debug: Log what we received
                self.logger.debug(f"Auth response data type: {type(response.data)}")
                self.logger.debug(f"Auth response data: {response.data}")
                
                # The token should be directly in response.data since _parse_response
                # already extracted the 'result' field
                token = None
                if isinstance(response.data, dict):
                    token = response.data.get('token')
                
                if token:
                    self.auth_token = token
                    self.session.headers['Authorization'] = f"Bearer {token}"
                    self.logger.info("Authentication successful")
                    return APIResponse(
                        success=True,
                        data={"token": token},
                        status_code=response.status_code,
                        message="Authentication successful"
                    )
                else:
                    self.logger.error(f"No token found in response data: {response.data}")
            
            return APIResponse(
                success=False,
                data=None,
                status_code=response.status_code,
                message="Authentication failed: No token in response"
            )
            
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            raise APIException(f"Authentication failed: {str(e)}")
    
    def _make_request(
        self,
        method: HTTPMethod,
        endpoint: str,
        data: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
        require_auth: bool = True,
        custom_headers: Dict[str, str] = None
    ) -> APIResponse:
        """
        Make HTTP request to the API
        
        Args:
            method: HTTP method
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: URL parameters
            require_auth: Whether authentication is required
            custom_headers: Additional headers
            
        Returns:
            APIResponse object
        """
        if require_auth and not self.auth_token:
            raise APIException("Authentication required. Please authenticate first.")
        
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        # Prepare headers
        headers = self.session.headers.copy()
        if custom_headers:
            headers.update(custom_headers)
        
        # Prepare request arguments
        request_args = {
            'url': url,
            'headers': headers,
            'timeout': self.timeout
        }
        
        if params:
            request_args['params'] = params
        
        if data and method in [HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.PATCH]:
            request_args['json'] = data
        
        try:
            self.logger.debug(f"Making {method.value} request to {url}")
            response = self.session.request(method.value, **request_args)
            
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise APIException(f"Request failed: {str(e)}")
    
    def _parse_response(self, response: requests.Response) -> APIResponse:
        """
        Parse HTTP response into APIResponse object
        
        Args:
            response: requests.Response object
            
        Returns:
            APIResponse object
        """
        try:
            # Try to parse JSON response
            if response.headers.get('content-type', '').startswith('application/json'):
                response_data = response.json()
            else:
                response_data = response.text
        except json.JSONDecodeError:
            response_data = response.text
        
        success = 200 <= response.status_code < 300
        
        # Extract error information if available
        errors = []
        message = None
        data = response_data
        
        if isinstance(response_data, dict):
            # Handle OpenSILEX response structure
            if 'metadata' in response_data and 'result' in response_data:
                # This is a standard OpenSILEX response
                metadata = response_data.get('metadata', {})
                result = response_data.get('result')
                
                # The result IS the data we want
                data = result
                
                # Check for errors in metadata
                if 'status' in metadata and isinstance(metadata['status'], list):
                    for status in metadata['status']:
                        if 'message' in status:
                            errors.append(status['message'])
            else:
                # Handle other response formats (non-OpenSILEX standard)
                if 'error' in response_data:
                    errors.append(response_data['error'])
                if 'message' in response_data:
                    message = response_data['message']
                # Note: We don't extract 'result' here because this is not
                # the OpenSILEX format (no metadata field)
        
        if not success and not errors:
            errors.append(f"HTTP {response.status_code}: {response.reason}")
        
        return APIResponse(
            success=success,
            data=data,
            status_code=response.status_code,
            message=message,
            errors=errors if errors else None
        )
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> APIResponse:
        """Make GET request"""
        return self._make_request(HTTPMethod.GET, endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> APIResponse:
        """Make POST request"""
        return self._make_request(HTTPMethod.POST, endpoint, data=data, params=params)
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> APIResponse:
        """Make PUT request"""
        return self._make_request(HTTPMethod.PUT, endpoint, data=data, params=params)
    
    def delete(self, endpoint: str, params: Dict[str, Any] = None) -> APIResponse:
        """Make DELETE request"""
        return self._make_request(HTTPMethod.DELETE, endpoint, params=params)
    
    def logout(self) -> APIResponse:
        """
        Logout and clear authentication
        """
        if self.auth_token:
            try:
                response = self.post("/security/logout")
                self.auth_token = None
                if 'Authorization' in self.session.headers:
                    del self.session.headers['Authorization']
                self.logger.info("Logout successful")
                return response
            except Exception as e:
                self.logger.error(f"Logout error: {str(e)}")
                # Clear token even if logout fails
                self.auth_token = None
                if 'Authorization' in self.session.headers:
                    del self.session.headers['Authorization']
        
        return APIResponse(
            success=True,
            data=None,
            status_code=200,
            message="Logged out"
        )
    
    def is_authenticated(self) -> bool:
        """Check if client is authenticated"""
        return self.auth_token is not None