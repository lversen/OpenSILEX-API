"""
OpenSilex API Client - Devices Module
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse

@dataclass
class DeviceCreationData:
    """Data structure for creating devices"""
    uri: Optional[str] = None
    name: str = None
    rdf_type: str = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    description: Optional[str] = None
    relations: Optional[List[Dict[str, Any]]] = None

class DevicesClient:
    """
    Client for managing devices in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Devices client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def create_device(self, device_data: DeviceCreationData) -> APIResponse:
        """
        Create a new device
        
        Args:
            device_data: Device creation data
            
        Returns:
            APIResponse with created device URI
        """
        data = {
            'name': device_data.name,
            'rdf_type': device_data.rdf_type,
            'brand': device_data.brand,
            'model': device_data.model,
            'serial_number': device_data.serial_number,
            'description': device_data.description,
            'relations': device_data.relations
        }
        if device_data.uri:
            data['uri'] = device_data.uri
            
        return self.client.post('/core/devices', data=data)
