"""
OpenSilex API Client - Sites Module
Handles site management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse
from urllib.parse import quote

@dataclass
class SiteSearchParams:
    """Parameters for site search"""
    name: Optional[str] = None
    organizations: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20

@dataclass
class SiteCreationData:
    """Data structure for creating sites"""
    uri: Optional[str] = None
    name: str = None
    rdf_type: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    organizations: Optional[List[str]] = None
    facilities: Optional[List[str]] = None
    groups: Optional[List[str]] = None
    description: Optional[str] = None
    geometry: Optional[Dict[str, Any]] = None

class SitesClient:
    """
    Client for managing sites in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Sites client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_sites(self, params: SiteSearchParams = None) -> APIResponse:
        """
        Search for sites
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of sites
        """
        if params is None:
            params = SiteSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['pattern'] = params.name
        if params.organizations:
            query_params['organizations'] = params.organizations
        
        return self.client.get('/core/sites', params=query_params)
    
    def get_site_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific site by URI
        
        Args:
            uri: Site URI
            
        Returns:
            APIResponse with site details
        """
        return self.client.get(f'/core/sites/{quote(uri, safe="")}')
    
    def create_site(self, site_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new site
        
        Args:
            site_data: Site creation data
            
        Returns:
            APIResponse with created site URI
        """
        return self.client.post('/core/sites', data=site_data)
    
    def update_site(self, site_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing site
        
        Args:
            site_data: Site update data
            
        Returns:
            APIResponse with updated site URI
        """
        return self.client.put('/core/sites', data=site_data)
    
    def delete_site(self, uri: str) -> APIResponse:
        """
        Delete a site
        
        Args:
            uri: Site URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/sites/{quote(uri, safe="")}')

    def get_sites_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple sites by their URIs
        
        Args:
            uris: List of site URIs
            
        Returns:
            APIResponse with list of sites
        """
        params = {'uris': uris}
        return self.client.get('/core/sites/by_uris', params=params)

    def get_sites_with_location(self) -> APIResponse:
        """
        Get only the list of sites with a location
            
        Returns:
            APIResponse with list of sites
        """
        return self.client.get('/core/sites/with_location')
