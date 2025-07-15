"""
OpenSilex API Client - Facilities Module
Handles facility management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse
from urllib.parse import quote

@dataclass
class FacilitySearchParams:
    """Parameters for facility search"""
    name: Optional[str] = None
    facility_type: Optional[str] = None
    page: int = 0
    page_size: int = 20


@dataclass
class FacilityCreationData:
    """Data structure for creating facilities"""
    uri: Optional[str] = None
    name: str = None
    facility_type: str = None
    address: Optional[str] = None


class FacilitiesClient:
    """
    Client for managing facilities in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Facilities client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_facilities(self, params: FacilitySearchParams = None) -> APIResponse:
        """
        Search for facilities
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of facilities
        """
        if params is None:
            params = FacilitySearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.facility_type:
            query_params['type'] = params.facility_type
        
        return self.client.get('/core/facilities', params=query_params)
    
    def get_facility_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific facility by URI
        
        Args:
            uri: Facility URI
            
        Returns:
            APIResponse with facility details
        """
        return self.client.get(f'/core/facilities/{quote(uri, safe="")}')
    
    def create_facility(self, facility_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new facility
        
        Args:
            facility_data: Facility creation data
            
        Returns:
            APIResponse with created facility URI
        """
        return self.client.post('/core/facilities', data=facility_data)
    
    def update_facility(self, facility_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing facility
        
        Args:
            facility_data: Facility update data
            
        Returns:
            APIResponse with updated facility URI
        """
        return self.client.put('/core/facilities', data=facility_data)
    
    def delete_facility(self, uri: str) -> APIResponse:
        """
        Delete a facility
        
        Args:
            uri: Facility URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/facilities/{quote(uri, safe="")}')
