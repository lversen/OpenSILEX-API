"""
OpenSilex API Client - Projects Module
Handles project management, experiments, and scientific objects
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from .base import BaseAPIClient, APIResponse


@dataclass
class ProjectSearchParams:
    """Parameters for project search"""
    name: Optional[str] = None
    year: Optional[int] = None
    keyword: Optional[str] = None
    order_by: Optional[List[str]] = None
    page: int = 0
    page_size: int = 20


@dataclass
class ProjectCreationData:
    """Data structure for creating projects"""
    uri: Optional[str] = None
    name: str = None
    shortname: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    homepage: Optional[str] = None
    objective: Optional[str] = None
    keywords: Optional[List[str]] = None
    related_projects: Optional[List[str]] = None
    coordinators: Optional[List[str]] = None
    scientific_contacts: Optional[List[str]] = None
    administrative_contacts: Optional[List[str]] = None


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


from urllib.parse import quote

class ProjectsClient:
    """
    Client for managing projects and experiments in OpenSilex
    """
    
    def __init__(self, base_client: BaseAPIClient):
        """
        Initialize Projects client
        
        Args:
            base_client: Authenticated BaseAPIClient instance
        """
        self.client = base_client
    
    def search_projects(self, params: ProjectSearchParams = None) -> APIResponse:
        """
        Search for projects
        
        Args:
            params: Search parameters
            
        Returns:
            APIResponse with list of projects
        """
        if params is None:
            params = ProjectSearchParams()
        
        query_params = {
            'page': params.page,
            'page_size': params.page_size
        }
        
        if params.name:
            query_params['name'] = params.name
        if params.year:
            query_params['year'] = params.year
        if params.keyword:
            query_params['keyword'] = params.keyword
        if params.order_by:
            query_params['order_by'] = params.order_by
        
        return self.client.get('/core/projects', params=query_params)
    
    def get_project_by_uri(self, uri: str) -> APIResponse:
        """
        Get a specific project by URI
        
        Args:
            uri: Project URI
            
        Returns:
            APIResponse with project details
        """
        return self.client.get(f'/core/projects/{quote(uri, safe='')}')
    
    def get_projects_by_uris(self, uris: List[str]) -> APIResponse:
        """
        Get multiple projects by their URIs
        
        Args:
            uris: List of project URIs
            
        Returns:
            APIResponse with list of projects
        """
        params = {'uris': uris}
        return self.client.get('/core/projects/by_uris', params=params)
    
    def create_project(self, project_data: ProjectCreationData) -> APIResponse:
        """
        Create a new project
        
        Args:
            project_data: Project creation data
            
        Returns:
            APIResponse with created project URI
        """
        data = {}
        
        if project_data.uri:
            data['uri'] = project_data.uri
        if project_data.name:
            data['name'] = project_data.name
        if project_data.shortname:
            data['shortname'] = project_data.shortname
        if project_data.description:
            data['description'] = project_data.description
        if project_data.start_date:
            data['start_date'] = project_data.start_date
        if project_data.end_date:
            data['end_date'] = project_data.end_date
        if project_data.homepage:
            data['homepage'] = project_data.homepage
        if project_data.objective:
            data['objective'] = project_data.objective
        if project_data.keywords:
            data['keywords'] = project_data.keywords
        if project_data.related_projects:
            data['related_projects'] = project_data.related_projects
        if project_data.coordinators:
            data['coordinators'] = project_data.coordinators
        if project_data.scientific_contacts:
            data['scientific_contacts'] = project_data.scientific_contacts
        if project_data.administrative_contacts:
            data['administrative_contacts'] = project_data.administrative_contacts
        
        return self.client.post('/core/projects', data=data)
    
    def update_project(self, project_data: ProjectCreationData) -> APIResponse:
        """
        Update an existing project
        
        Args:
            project_data: Project update data
            
        Returns:
            APIResponse with updated project URI
        """
        data = {}
        
        if project_data.uri:
            data['uri'] = project_data.uri
        if project_data.name:
            data['name'] = project_data.name
        if project_data.shortname:
            data['shortname'] = project_data.shortname
        if project_data.description:
            data['description'] = project_data.description
        if project_data.start_date:
            data['start_date'] = project_data.start_date
        if project_data.end_date:
            data['end_date'] = project_data.end_date
        if project_data.homepage:
            data['homepage'] = project_data.homepage
        if project_data.objective:
            data['objective'] = project_data.objective
        if project_data.keywords:
            data['keywords'] = project_data.keywords
        if project_data.related_projects:
            data['related_projects'] = project_data.related_projects
        if project_data.coordinators:
            data['coordinators'] = project_data.coordinators
        if project_data.scientific_contacts:
            data['scientific_contacts'] = project_data.scientific_contacts
        if project_data.administrative_contacts:
            data['administrative_contacts'] = project_data.administrative_contacts
        
        return self.client.put('/core/projects', data=data)
    
    def delete_project(self, uri: str) -> APIResponse:
        """
        Delete a project
        
        Args:
            uri: Project URI to delete
            
        Returns:
            APIResponse confirming deletion
        """
        return self.client.delete(f'/core/projects/{uri}')
    
    # Experiment management methods
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
        return self.client.get(f'/core/experiments/{uri}')
    
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
        return self.client.delete(f'/core/experiments/{uri}')
    
    # Scientific Objects management methods
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
        return self.client.get(f'/core/scientific_objects/{uri}')
    
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
        return self.client.delete(f'/core/scientific_objects/{uri}')
    
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