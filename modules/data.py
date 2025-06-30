"""
OpenSilex API Client - Data Module
Handles scientific data management, measurements, and data series
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from .base import BaseAPIClient, APIResponse


@dataclass
class DataSearchParams:
    """Parameters for data search"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    timezone: Optional[str] = None
    experiments: Optional[List[str]] = None
    targets: Optional[List[str]] = None
    variables: Optional[List[str]] = None
    devices: Optional[List[str]] = None
    min_confidence: Optional[float] = None
    max_confidence: Optional[float] = None
    provenance: Optional[List[str]] = None
    metadata: Optional[str] = None
    operators: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20


@dataclass
class DataPoint:
    """Single data point structure"""
    target: str
    variable: str
    date: str
    value: Any
    confidence: Optional[float] = None
    provenance: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ProvenanceSearchParams:
    """Parameters for provenance search"""
    name: Optional[str] = None
    description: Optional[str] = None
    activity: Optional[str] = None
    activity_type: Optional[str] = None
    agent: Optional[List[str]] = None
    order_by: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20


class DataClient:
    """
    Client for managing scientific data in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Data client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_data(self, params: DataSearchParams = None) -> APIResponse:
        """
        Search for data with various filters
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of data points
        """
        if params is None:
            params = DataSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        # Add optional parameters
        if params.start_date:
            query_params['start_date'] = params.start_date
        if params.end_date:
            query_params['end_date'] = params.end_date
        if params.timezone:
            query_params['timezone'] = params.timezone
        if params.experiments:
            query_params['experiments'] = params.experiments
        if params.targets:
            query_params['targets'] = params.targets
        if params.variables:
            query_params['variables'] = params.variables
        if params.devices:
            query_params['devices'] = params.devices
        if params.min_confidence is not None:
            query_params['min_confidence'] = params.min_confidence
        if params.max_confidence is not None:
            query_params['max_confidence'] = params.max_confidence
        if params.provenance:
            query_params['provenance'] = params.provenance
        if params.metadata:
            query_params['metadata'] = params.metadata
        if params.operators:
            query_params['operators'] = params.operators
        
        return self.client.get('/core/data', params=query_params)
    
    def search_data_optimized(self, targets: List[str], variables: List[str] = None, 
                            start_date: str = None, end_date: str = None) -> APIResponse:
        """
        Optimized search for large list of targets
        
        Args:
            targets: List of target URIs
            variables: List of variable URIs
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            APIResponse with optimized search results
        """
        data = {'targets': targets}
        
        if variables:
            data['variables'] = variables
        if start_date:
            data['start_date'] = start_date
        if end_date:
            data['end_date'] = end_date
        
        return self.client.post('/core/data/search', data=data)
    
    def create_data(self, data_points: List[DataPoint]) -> APIResponse:
        """
        Create new data points
        
        Args:
            data_points: List of data points to create
            
        Returns:
            APIResponse confirming data creation
        """
        data_list = []
        for point in data_points:
            point_data = {
                'target': point.target,
                'variable': point.variable,
                'date': point.date,
                'value': point.value
            }
            if point.confidence is not None:
                point_data['confidence'] = point.confidence
            if point.provenance:
                point_data['provenance'] = point.provenance
            if point.metadata:
                point_data['metadata'] = point.metadata
            
            data_list.append(point_data)
        
        return self.client.post('/core/data', data={'data': data_list})
    
    def update_data_confidence(self, uri: str, confidence: float) -> APIResponse:
        """
        Update confidence value for a data point
        
        Args:
            uri: Data point URI
            confidence: New confidence value
            
        Returns:
            APIResponse confirming update
        """
        data = {'confidence': confidence}
        return self.client.put(f'/core/data/{uri}/confidence', data=data)
    
    def delete_data(self, uri: str) -> APIResponse:
        """
        Delete a data point
        
        Args:
            uri: Data point URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/data/{uri}')
    
    def get_data_by_uri(self, uri: str) -> APIResponse:
        """
        Get specific data point by URI
        
        Args:
            uri: Data point URI
            
        Returns:
            APIResponse with data point details
        """
        return self.client.get(f'/core/data/{uri}')
    
    def get_data_series_by_facility(self, variable: str, target: str, 
                                  start_date: str = None, end_date: str = None,
                                  calculated_only: bool = False) -> APIResponse:
        """
        Get data series associated with a facility
        
        Args:
            variable: Variable URI
            target: Target URI
            start_date: Start date filter
            end_date: End date filter
            calculated_only: Whether to retrieve calculated series only
            
        Returns:
            APIResponse with data series
        """
        params = {
            'variable': variable,
            'target': target,
            'calculated_only': calculated_only
        }
        
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        return self.client.get('/core/data/data_serie/facility', params=params)
    
    def get_mathematical_operators(self) -> APIResponse:
        """
        Get available mathematical operators
        
        Returns:
            APIResponse with list of mathematical operators
        """
        return self.client.get('/core/data/mathematicalOperators')
    
    def export_data(self, uris: List[str], export_format: str = 'csv') -> APIResponse:
        """
        Export data points
        
        Args:
            uris: List of data URIs to export
            export_format: Export format (csv, json, etc.)
            
        Returns:
            APIResponse with exported data
        """
        data = {
            'uris': uris,
            'format': export_format
        }
        return self.client.post('/core/data/export', data=data)
    
    # Provenance management methods
    def search_provenances(self, params: ProvenanceSearchParams = None) -> APIResponse:
        """
        Search for provenances
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of provenances
        """
        if params is None:
            params = ProvenanceSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.description:
            query_params['description'] = params.description
        if params.activity:
            query_params['activity'] = params.activity
        if params.activity_type:
            query_params['activity_type'] = params.activity_type
        if params.agent:
            query_params['agent'] = params.agent
        if params.order_by:
            query_params['order_by'] = params.order_by
        
        return self.client.get('/core/provenances', params=query_params)
    
    def get_provenance_by_uri(self, uri: str) -> APIResponse:
        """
        Get specific provenance by URI
        
        Args:
            uri: Provenance URI
            
        Returns:
            APIResponse with provenance details
        """
        return self.client.get(f'/core/provenances/{uri}')
    
    def create_provenance(self, provenance_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new provenance record
        
        Args:
            provenance_data: Provenance creation data
            
        Returns:
            APIResponse with created provenance URI
        """
        return self.client.post('/core/provenances', data=provenance_data)
    
    def update_provenance(self, provenance_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing provenance record
        
        Args:
            provenance_data: Provenance update data
            
        Returns:
            APIResponse with updated provenance URI
        """
        return self.client.put('/core/provenances', data=provenance_data)
    
    def delete_provenance(self, uri: str) -> APIResponse:
        """
        Delete a provenance record
        
        Args:
            uri: Provenance URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/provenances/{uri}')
    
    def get_provenances_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple provenances by their URIs
        
        Args:
            uris: List of provenance URIs
            
        Returns:
            APIResponse with list of provenances
        """
        params = {'uris': uris}
        return self.client.get('/core/provenances/by_uris', params=params)