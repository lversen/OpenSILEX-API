"""
OpenSilex API Client - Persons Module
Handles person management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse
from urllib.parse import quote

@dataclass
class PersonSearchParams:
    """Parameters for person search"""
    name: Optional[str] = None
    email: Optional[str] = None
    page: int = 0
    page_size: int = 20

@dataclass
class PersonCreationData:
    """Data structure for creating persons"""
    uri: Optional[str] = None
    first_name: str = None
    last_name: str = None
    email: str = None
    affiliation: Optional[str] = None
    phone_number: Optional[str] = None
    orcid: Optional[str] = None
    account: Optional[str] = None

class PersonsClient:
    """
    Client for managing persons in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Persons client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_persons(self, params: PersonSearchParams = None) -> APIResponse:
        """
        Search for persons
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of persons
        """
        if params is None:
            params = PersonSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.email:
            query_params['email'] = params.email
        
        return self.client.get('/security/persons', params=query_params)
    
    def get_person_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific person by URI
        
        Args:
            uri: Person URI
            
        Returns:
            APIResponse with person details
        """
        return self.client.get(f'/security/persons/{quote(uri, safe="")}')
    
    def create_person(self, person_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new person
        
        Args:
            person_data: Person creation data
            
        Returns:
            APIResponse with created person URI
        """
        return self.client.post('/security/persons', data=person_data)
    
    def update_person(self, person_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing person
        
        Args:
            person_data: Person update data
            
        Returns:
            APIResponse with updated person URI
        """
        return self.client.put('/security/persons', data=person_data)

    def get_persons_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple persons by their URIs
        
        Args:
            uris: List of person URIs
            
        Returns:
            APIResponse with list of persons
        """
        params = {'uris': uris}
        return self.client.get('/security/persons/by_uris', params=params)
