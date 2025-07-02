"""
OpenSilex API Client - Experiments Module
Handles experiment management
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse
from urllib.parse import quote

@dataclass
class ExperimentSearchParams:
    """Parameters for experiment search"""
    name: Optional[str] = None
    year: Optional[int] = None
    project: Optional[str] = None
    is_public: Optional[bool] = None
    order_by: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20


@dataclass
class ExperimentCreationData:
    """Data structure for creating experiments"""
    uri: Optional[str] = None
    name: str = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    objective: Optional[str] = None
    project: Optional[str] = None
    is_public: bool = False
    contacts: Optional[List[Dict[str, Any]]] = None
    technical_supervisors: Optional[List[str]] = None
    scientific_supervisors: Optional[List[str]] = None
    groups: Optional[List[str]] = None


class ExperimentsClient:
    """
    Client for managing experiments in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Experiments client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_experiments(self, params: ExperimentSearchParams = None) -> APIResponse:
        """
        Search for experiments
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of experiments
        """
        if params is None:
            params = ExperimentSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.year:
            query_params['year'] = params.year
        if params.project:
            query_params['project'] = params.project
        if params.is_public is not None:
            query_params['is_public'] = params.is_public
        if params.order_by:
            query_params['order_by'] = params.order_by
        
        return self.client.get('/core/experiments', params=query_params)
    
    def get_experiment_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific experiment by URI
        
        Args:
            uri: Experiment URI
            
        Returns:
            APIResponse with experiment details
        """
        return self.client.get(f'/core/experiments/{quote(uri, safe="")}')
    
    def create_experiment(self, experiment_data: Dict[str, Any]) -> APIResponse:
        """
        Create a new experiment
        
        Args:
            experiment_data: Experiment creation data
            
        Returns:
            APIResponse with created experiment URI
        """
        return self.client.post('/core/experiments', data=experiment_data)
    
    def update_experiment(self, experiment_data: Dict[str, Any]) -> APIResponse:
        """
        Update an existing experiment
        
        Args:
            experiment_data: Experiment update data
            
        Returns:
            APIResponse with updated experiment URI
        """
        return self.client.put('/core/experiments', data=experiment_data)
    
    def delete_experiment(self, uri: str) -> APIResponse:
        """
        Delete an experiment
        
        Args:
            uri: Experiment URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/experiments/{quote(uri, safe="")}')