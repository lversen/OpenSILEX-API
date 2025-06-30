"""
OpenSilex API Client - Variables Module
Handles variables, entities, and related data types
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse


@dataclass
class VariableSearchParams:
    """Parameters for variable search"""
    name: Optional[str] = None
    order_by: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20
    shared_resource_instance: Optional[str] = None


@dataclass
class EntityCreationData:
    """Data structure for creating entities"""
    uri: Optional[str] = None
    name: str = None
    description: Optional[str] = None
    rdf_type: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None


class VariablesClient:
    """
    Client for managing variables and entities in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Variables client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_variables(self, params: VariableSearchParams = None) -> APIResponse:
        """
        Search for variables
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of variables
        """
        if params is None:
            params = VariableSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.order_by:
            query_params['order_by'] = params.order_by
        if params.shared_resource_instance:
            query_params['sharedResourceInstance'] = params.shared_resource_instance
        
        return self.client.get('/core/variables', params=query_params)
    
    def get_variable_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific variable by URI
        
        Args:
            uri: Variable URI
            
        Returns:
            APIResponse with variable details
        """
        return self.client.get(f'/core/variables/{uri}')
    
    def get_variables_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple variables by their URIs
        
        Args:
            uris: List of variable URIs
            
        Returns:
            APIResponse with list of variables
        """
        params = {'uris': uris}
        return self.client.get('/core/variables/by_uris', params=params)
    
    def create_variable(self, variable_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new variable
        
        Args:
            variable_data: Variable creation data
            
        Returns:
            APIResponse with created variable URI
        """
        return self.client.post('/core/variables', data=variable_data)
    
    def update_variable(self, variable_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing variable
        
        Args:
            variable_data: Variable update data
            
        Returns:
            APIResponse with updated variable URI
        """
        return self.client.put('/core/variables', data=variable_data)
    
    def delete_variable(self, uri: str) -> APIResponse:
        """
        Delete a variable
        
        Args:
            uri: Variable URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/variables/{uri}')
    
    def get_variable_datatypes(self) -> APIResponse:
        """
        Get available variable data types
        
        Returns:
            APIResponse with list of data types
        """
        return self.client.get('/core/variables/datatypes')
    
    def export_variables_classic(self, uris: List[str]) -> APIResponse:
        """
        Export variables in classic format
        
        Args:
            uris: List of variable URIs to export
            
        Returns:
            APIResponse with CSV export data
        """
        data = {'uris': uris}
        return self.client.post('/core/variables/export_classic_by_uris', data=data)
    
    def export_variables_detailed(self, uris: List[str]) -> APIResponse:
        """
        Export variables in detailed format
        
        Args:
            uris: List of variable URIs to export
            
        Returns:
            APIResponse with detailed CSV export data
        """
        data = {'uris': uris}
        return self.client.post('/core/variables/export_details_by_uris', data=data)
    
    # Entity management methods
    def search_entities(self, params: VariableSearchParams = None) -> APIResponse:
        """
        Search for entities
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of entities
        """
        if params is None:
            params = VariableSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.order_by:
            query_params['order_by'] = params.order_by
        if params.shared_resource_instance:
            query_params['sharedResourceInstance'] = params.shared_resource_instance
        
        return self.client.get('/core/entities', params=query_params)
    
    def create_entity(self, entity_data: EntityCreationData) -> APIResponse:
        """
        Create a new entity
        
        Args:
            entity_data: Entity creation data
            
        Returns:
            APIResponse with created entity URI
        """
        data = {}
        if entity_data.uri:
            data['uri'] = entity_data.uri
        if entity_data.name:
            data['name'] = entity_data.name
        if entity_data.description:
            data['description'] = entity_data.description
        if entity_data.rdf_type:
            data['rdf_type'] = entity_data.rdf_type
        if entity_data.properties:
            data['properties'] = entity_data.properties
        
        return self.client.post('/core/entities', data=data)
    
    def update_entity(self, entity_data: EntityCreationData) -> APIResponse:
        """
        Update an existing entity
        
        Args:
            entity_data: Entity update data
            
        Returns:
            APIResponse with updated entity URI
        """
        data = {}
        if entity_data.uri:
            data['uri'] = entity_data.uri
        if entity_data.name:
            data['name'] = entity_data.name
        if entity_data.description:
            data['description'] = entity_data.description
        if entity_data.rdf_type:
            data['rdf_type'] = entity_data.rdf_type
        if entity_data.properties:
            data['properties'] = entity_data.properties
        
        return self.client.put('/core/entities', data=data)
    
    def get_entities_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple entities by their URIs
        
        Args:
            uris: List of entity URIs
            
        Returns:
            APIResponse with list of entities
        """
        params = {'uris': uris}
        return self.client.get('/core/entities/by_uris', params=params)