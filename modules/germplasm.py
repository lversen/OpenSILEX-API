"""
OpenSilex API Client - Germplasm Module
Handles germplasm management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse
from urllib.parse import quote

@dataclass
class GermplasmSearchParams:
    """Parameters for germplasm search"""
    germplasm_db_id: Optional[str] = None
    germplasm_pui: Optional[str] = None
    germplasm_name: Optional[str] = None
    common_crop_name: Optional[str] = None
    page: int = 0
    page_size: int = 20


@dataclass
class GermplasmCreationData:
    """Data structure for creating germplasm"""
    uri: Optional[str] = None
    name: str = None
    rdf_type: str = None
    synonyms: Optional[List[str]] = None
    code: Optional[str] = None
    production_year: Optional[int] = None
    description: Optional[str] = None
    species: Optional[str] = None
    variety: Optional[str] = None
    accession: Optional[str] = None
    institute: Optional[str] = None
    website: Optional[str] = None
    relations: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None


class GermplasmClient:
    """
    Client for managing germplasm in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Germplasm client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_germplasm(self, params: GermplasmSearchParams = None) -> APIResponse:
        """
        Search for germplasm
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of germplasm
        """
        if params is None:
            params = GermplasmSearchParams()
        
        query_params = {
            'page': params.page,
            'pageSize': params.page_size
        }
        
        if params.germplasm_db_id:
            query_params['germplasmDbId'] = params.germplasm_db_id
        if params.germplasm_pui:
            query_params['germplasmPUI'] = params.germplasm_pui
        if params.germplasm_name:
            query_params['germplasmName'] = params.germplasm_name
        if params.common_crop_name:
            query_params['commonCropName'] = params.common_crop_name
        
        return self.client.get('/brapi/v1/germplasm', params=query_params)
    
    def get_germplasm_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific germplasm by URI
        
        Args:
            uri: Germplasm URI
            
        Returns:
            APIResponse with germplasm details
        """
        return self.client.get(f'/core/germplasm/{quote(uri, safe="")}')
    
    def create_germplasm(self, germplasm_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new germplasm
        
        Args:
            germplasm_data: Germplasm creation data
            
        Returns:
            APIResponse with created germplasm URI
        """
        return self.client.post('/core/germplasm', data=germplasm_data)
    
    def update_germplasm(self, germplasm_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing germplasm
        
        Args:
            germplasm_data: Germplasm update data
            
        Returns:
            APIResponse with updated germplasm URI
        """
        return self.client.put('/core/germplasm', data=germplasm_data)
    
    def delete_germplasm(self, uri: str) -> APIResponse:
        """
        Delete a germplasm
        
        Args:
            uri: Germplasm URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/germplasm/{quote(uri, safe="")}')

    def get_germplasm_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple germplasm by their URIs
        
        Args:
            uris: List of germplasm URIs
            
        Returns:
            APIResponse with list of germplasm
        """
        params = {'uris': uris}
        return self.client.post('/core/germplasm/by_uris', data=params)
