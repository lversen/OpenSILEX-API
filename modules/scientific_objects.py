"""
OpenSilex API Client - Scientific Objects Module
Handles scientific object management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse
from urllib.parse import quote

@dataclass
class ScientificObjectSearchParams:
    """Parameters for scientific object search"""
    name: Optional[str] = None
    rdf_types: Optional[List[str]] = None
    experiment: Optional[str] = None
    factor_levels: Optional[List[str]] = None
    parent: Optional[str] = None
    germplasm: Optional[List[str]] = None
    order_by: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20


@dataclass
class ScientificObjectCreationData:
    """Data structure for creating scientific objects"""
    uri: Optional[str] = None
    name: str = None
    rdf_type: str = None
    experiment: str = None
    relations: Optional[List[Dict[str, Any]]] = None


class ScientificObjectsClient:
    """
    Client for managing scientific objects in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize ScientificObjects client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_scientific_objects(self, params: ScientificObjectSearchParams = None) -> APIResponse:
        """
        Search for scientific objects
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of scientific objects
        """
        if params is None:
            params = ScientificObjectSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.rdf_types:
            query_params['rdf_types'] = params.rdf_types
        if params.experiment:
            query_params['experiment'] = params.experiment
        if params.factor_levels:
            query_params['factor_levels'] = params.factor_levels
        if params.parent:
            query_params['parent'] = params.parent
        if params.germplasm:
            query_params['germplasm'] = params.germplasm
        if params.order_by:
            query_params['order_by'] = params.order_by
        
        return self.client.get('/core/scientific_objects', params=query_params)
    
    def get_scientific_object_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific scientific object by URI
        
        Args:
            uri: Scientific object URI
            
        Returns:
            APIResponse with scientific object details
        """
        return self.client.get(f'/core/scientific_objects/{quote(uri, safe="")}')
    
    def create_scientific_object(self, object_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new scientific object
        
        Args:
            object_data: Scientific object creation data
            
        Returns:
            APIResponse with created scientific object URI
        """
        return self.client.post('/core/scientific_objects', data=object_data)
    
    def update_scientific_object(self, object_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing scientific object
        
        Args:
            object_data: Scientific object update data
            
        Returns:
            APIResponse with updated scientific object URI
        """
        return self.client.put('/core/scientific_objects', data=object_data)
    
    def delete_scientific_object(self, uri: str) -> APIResponse:
        """
        Delete a scientific object
        
        Args:
            uri: Scientific object URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/scientific_objects/{quote(uri, safe="")}')
    
    def get_scientific_objects_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple scientific objects by their URIs
        
        Args:
            uris: List of scientific object URIs
            
        Returns:
            APIResponse with list of scientific objects
        """
        params = {'uris': uris}
        return self.client.get('/core/scientific_objects/by_uris', params=params)
