"""
OpenSilex API Client - Organizations Module
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse

@dataclass
class OrganizationCreationData:
    """Data structure for creating organizations"""
    uri: Optional[str] = None
    name: str = None
    rdf_type: str = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    relations: Optional[List[Dict[str, Any]]] = None

class OrganizationsClient:
    """
    Client for managing organizations in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Organizations client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def create_organization(self, organization_data: OrganizationCreationData) -> APIResponse:
        """
        Create a new organization
        
        Args:
            organization_data: Organization creation data
            
        Returns:
            APIResponse with created organization URI
        """
        data = {
            'name': organization_data.name,
            'rdf_type': organization_data.rdf_type,
            'address': organization_data.address,
            'phone': organization_data.phone,
            'email': organization_data.email,
            'website': organization_data.website,
            'description': organization_data.description,
            'relations': organization_data.relations
        }
        if organization_data.uri:
            data['uri'] = organization_data.uri
            
        return self.client.post('/core/organisations', data=data)
