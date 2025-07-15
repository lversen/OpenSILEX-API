"""
OpenSilex API Client - Main Unified Client
Brings together all modules for comprehensive OpenSilex API access
"""

from typing import Dict, Any, Optional
from modules.base import BaseAPIClient, APIResponse
from modules.variables import VariablesClient
from modules.data import DataClient
from modules.projects import ProjectsClient
from modules.devices import DevicesClient
from modules.organizations import OrganizationsClient
from modules.experiments import ExperimentsClient
from modules.facilities import FacilitiesClient
from modules.sites import SitesClient
from modules.persons import PersonsClient
from modules.scientific_objects import ScientificObjectsClient
from modules.germplasm import GermplasmClient


class OpenSilexClient:
    """
    Main OpenSilex API client that provides access to all API modules
    """
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize the OpenSilex client
        
        Args:
            base_url: Base URL of the OpenSilex API (e.g., 'https://your-opensilex.com/rest')
            timeout: Request timeout in seconds
        """
        # Initialize base client
        self.base_client = BaseAPIClient(base_url, timeout)
        
        # Initialize module clients
        self.variables = VariablesClient(self.base_client)
        self.data = DataClient(self.base_client)
        self.projects = ProjectsClient(self.base_client)
        self.devices = DevicesClient(self.base_client)
        self.organizations = OrganizationsClient(self.base_client)
        self.experiments = ExperimentsClient(self.base_client)
        self.facilities = FacilitiesClient(self.base_client)
        self.sites = SitesClient(self.base_client)
        self.persons = PersonsClient(self.base_client)
        self.scientific_objects = ScientificObjectsClient(self.base_client)
        self.germplasm = GermplasmClient(self.base_client)
    
    def authenticate(self, identifier: str, password: str) -> APIResponse:
        """
        Authenticate with the OpenSilex API
        
        Args:
            identifier: User identifier (email/username)
            password: User password
            
        Returns:
            APIResponse with authentication status
        """
        return self.base_client.authenticate(identifier, password)
    
    def logout(self) -> APIResponse:
        """
        Logout from the OpenSilex API
        
        Returns:
            APIResponse with logout status
        """
        return self.base_client.logout()
    
    def is_authenticated(self) -> bool:
        """
        Check if client is authenticated
        
        Returns:
            True if authenticated, False otherwise
        """
        return self.base_client.is_authenticated()
    
    # System information methods
    def get_system_info(self) -> APIResponse:
        """
        Get system information
        
        Returns:
            APIResponse with system info
        """
        return self.base_client.get('/core/system/info')
    
    def get_version_info(self) -> APIResponse:
        """
        Get version information
        
        Returns:
            APIResponse with version info
        """
        return self.base_client.get('/core/system/version')
    
    def health_check(self) -> APIResponse:
        """
        Perform health check
        
        Returns:
            APIResponse with health status
        """
        return self.base_client.get('/core/system/health')
    
    # Organization methods
    def search_organizations(self, name: str = None, page: int = 0, page_size: int = 20) -> APIResponse:
        """
        Search for organizations
        
        Args:
            name: Organization name filter
            page: Page number
            page_size: Page size
            
        Returns:
            APIResponse with list of organizations
        """
        params = {'page': page, 'page_size': page_size}
        if name:
            params['name'] = name
        
        return self.base_client.get('/core/organisations', params=params)
    
    def get_organization_by_uri(self, uri: str) -> APIResponse:
        """
        Get organization by URI
        
        Args:
            uri: Organization URI
            
        Returns:
            APIResponse with organization details
        """
        return self.base_client.get(f'/core/organisations/{uri}')
    
    def create_organization(self, organization_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new organization
        
        Args:
            organization_data: Organization creation data
            
        Returns:
            APIResponse with created organization URI
        """
        return self.base_client.post('/core/organisations', data=organization_data)
    
    # Device methods
    def search_devices(self, name: str = None, rdf_type: str = None, 
                      include_subtypes: bool = True, page: int = 0, page_size: int = 20) -> APIResponse:
        """
        Search for devices
        
        Args:
            name: Device name filter
            rdf_type: RDF type filter
            include_subtypes: Include subtypes in search
            page: Page number
            page_size: Page size
            
        Returns:
            APIResponse with list of devices
        """
        params = {
            'page': page,
            'page_size': page_size,
            'include_subtypes': include_subtypes
        }
        if name:
            params['name'] = name
        if rdf_type:
            params['rdf_type'] = rdf_type
        
        return self.base_client.get('/core/devices', params=params)
    
    def get_device_by_uri(self, uri: str) -> APIResponse:
        """
        Get device by URI
        
        Args:
            uri: Device URI
            
        Returns:
            APIResponse with device details
        """
        return self.base_client.get(f'/core/devices/{uri}')
    
    def create_device(self, device_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new device
        
        Args:
            device_data: Device creation data
            
        Returns:
            APIResponse with created device URI
        """
        return self.base_client.post('/core/devices', data=device_data)
    
    # Ontology methods
    def search_concepts(self, name: str = None, parent: str = None, 
                       page: int = 0, page_size: int = 20) -> APIResponse:
        """
        Search for ontology concepts
        
        Args:
            name: Concept name filter
            parent: Parent concept URI
            page: Page number
            page_size: Page size
            
        Returns:
            APIResponse with list of concepts
        """
        params = {'page': page, 'page_size': page_size}
        if name:
            params['name'] = name
        if parent:
            params['parent'] = parent
        
        return self.base_client.get('/core/ontology/concepts', params=params)
    
    def get_concept_by_uri(self, uri: str) -> APIResponse:
        """
        Get concept by URI
        
        Args:
            uri: Concept URI
            
        Returns:
            APIResponse with concept details
        """
        return self.base_client.get(f'/core/ontology/concepts/{uri}')
    
    # Document methods
    def search_documents(self, name: str = None, page: int = 0, page_size: int = 20) -> APIResponse:
        """
        Search for documents
        
        Args:
            name: Document name filter
            page: Page number
            page_size: Page size
            
        Returns:
            APIResponse with list of documents
        """
        params = {'page': page, 'page_size': page_size}
        if name:
            params['name'] = name
        
        return self.base_client.get('/core/documents', params=params)
    
    def get_document_by_uri(self, uri: str) -> APIResponse:
        """
        Get document by URI
        
        Args:
            uri: Document URI
            
        Returns:
            APIResponse with document details
        """
        return self.base_client.get(f'/core/documents/{uri}')
    
    def upload_document(self, file_path: str, description: str = None, 
                       targets: list = None) -> APIResponse:
        """
        Upload a document
        
        Args:
            file_path: Path to the file to upload
            description: Document description
            targets: List of target URIs to associate with the document
            
        Returns:
            APIResponse with uploaded document URI
        """
        # Note: This would need file upload handling
        # Implementation depends on the specific file upload requirements
        raise NotImplementedError("File upload needs to be implemented based on specific requirements")
    
    # Event methods
    def search_events(self, target: str = None, page: int = 0, page_size: int = 20) -> APIResponse:
        """
        Search for events
        
        Args:
            target: Target URI filter
            page: Page number
            page_size: Page size
            
        Returns:
            APIResponse with list of events
        """
        params = {'page': page, 'page_size': page_size}
        if target:
            params['target'] = target
        
        return self.base_client.get('/core/events', params=params)
    
    def create_event(self, event_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new event
        
        Args:
            event_data: Event creation data
            
        Returns:
            APIResponse with created event URI
        """
        return self.base_client.post('/core/events', data=event_data)
    
    # BRAPI methods (Breeding API compatibility)
    def get_brapi_calls(self) -> APIResponse:
        """
        Get available BRAPI calls
        
        Returns:
            APIResponse with list of BRAPI calls
        """
        return self.base_client.get('/brapi/v1/calls')
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.is_authenticated():
            self.logout()