"""
OpenSilex API Client - Configuration and Usage Examples
Provides configuration management and example usage patterns
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from get_host import SSHConfigParser

def get_opensilex_base_url(host_name: Optional[str] = None, non_interactive: bool = False) -> str:
    """
    Retrieves the OpenSilex base URL from SSH config.
    If host_name is not provided or not found, it interactively prompts the user to select a host.
    """
    ssh_parser = SSHConfigParser()
    selected_host_name = host_name

    if selected_host_name:
        host_config = ssh_parser.get_host(selected_host_name)
        if not host_config:
            print(f"Host '{selected_host_name}' not found in SSH config. Prompting for interactive selection.")
            selected_host_name = select_opensilex_host_interactively(non_interactive=non_interactive)
    else:
        selected_host_name = select_opensilex_host_interactively(non_interactive=non_interactive)

    if not selected_host_name:
        raise ValueError("No host selected. Exiting.")

    host_config = ssh_parser.get_host(selected_host_name)
    if not host_config:
        # This case should ideally not be reached if select_opensilex_host_interactively works correctly
        raise ValueError(f"Selected host '{selected_host_name}' not found in SSH config.")

    hostname = host_config.get('hostname', selected_host_name)
    port = host_config.get('port', '28081')
    # Assuming the OpenSilex API is at /rest or /sandbox/rest
    # Adjust this path based on your OpenSilex instance's configuration
    return f"http://{hostname}:{port}/rest"

def select_opensilex_host_interactively(non_interactive: bool = False) -> str:
    """
    Interactively prompts the user to select an OpenSilex host from SSH config.
    """
    ssh_parser = SSHConfigParser()
    hosts = ssh_parser.get_all_hosts()

    if not hosts:
        raise ValueError("No hosts found in SSH config. Please configure them in ~/.ssh/config")

    if non_interactive:
        return list(hosts.keys())[0]

    print("\nAvailable OpenSilex hosts from SSH config:")
    print("=" * 50)

    host_list = list(hosts.keys())
    for i, host_name in enumerate(host_list, 1):
        host_config = hosts[host_name]
        hostname = host_config.get('hostname', host_name)
        port = host_config.get('port', '28081')
        print(f"{i}. {host_name}")
        print(f"   Hostname: {hostname}")
        print(f"   Port: {port}")
        print()

    while True:
        try:
            choice = input(f"Select host (1-{len(host_list)}) or 'q' to quit: ").strip()

            if choice.lower() == 'q':
                print("Exiting...")
                exit(0)

            choice_num = int(choice)
            if 1 <= choice_num <= len(host_list):
                selected_host = host_list[choice_num - 1]
                return selected_host
            else:
                print(f"Please enter a number between 1 and {len(host_list)}")

        except ValueError:
            print("Please enter a valid number or 'q' to quit")
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)
class OpenSilexConfig:
    """Configuration class for OpenSilex API client"""
    base_url: str
    username: str = None
    password: str = None
    timeout: int = 30
    log_level: str = "INFO"
    verify_ssl: bool = True
    
    @classmethod
    def from_file(cls, config_path: str) -> 'OpenSilexConfig':
        """
        Load configuration from JSON file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            OpenSilexConfig instance
        """
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        return cls(**config_data)
    
    @classmethod
    def from_env(cls) -> 'OpenSilexConfig':
        """
        Load configuration from environment variables
        
        Returns:
            OpenSilexConfig instance
        """
        return cls(
            base_url=os.getenv('OPENSILEX_BASE_URL'),
            username=os.getenv('OPENSILEX_USERNAME'),
            password=os.getenv('OPENSILEX_PASSWORD'),
            timeout=int(os.getenv('OPENSILEX_TIMEOUT', '30')),
            log_level=os.getenv('OPENSILEX_LOG_LEVEL', 'INFO'),
            verify_ssl=os.getenv('OPENSILEX_VERIFY_SSL', 'True').lower() == 'true'
        )
    
    def save_to_file(self, config_path: str, exclude_password: bool = True):
        """
        Save configuration to JSON file
        
        Args:
            config_path: Path to save configuration
            exclude_password: Whether to exclude password from saved config
        """
        config_dict = asdict(self)
        if exclude_password:
            config_dict.pop('password', None)
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)


def setup_logging(log_level: str = "INFO"):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('opensilex_client.log')
        ]
    )


# Example usage patterns
def example_basic_usage():
    """
    Example: Basic authentication and system info
    """
    from client import OpenSilexClient
    
    # Initialize client
    client = OpenSilexClient(get_opensilex_base_url())
    
    try:
        # Authenticate
        auth_response = client.authenticate("admin@opensilex.org", "admin")
        if auth_response.success:
            print("Authentication successful!")
            
            # Get system info
            system_info = client.get_system_info()
            if system_info.success:
                print(f"System info: {system_info.data}")
            
            # Get version info
            version_info = client.get_version_info()
            if version_info.success:
                print(f"Version: {version_info.data}")
        
        else:
            print(f"Authentication failed: {auth_response.errors}")
    
    finally:
        client.logout()


def example_data_management():
    """
    Example: Working with scientific data
    """
    from client import OpenSilexClient
    from modules.data import DataSearchParams, DataPoint
    
    client = OpenSilexClient(get_opensilex_base_url())
    
    try:
        # Authenticate
        client.authenticate("admin@opensilex.org", "admin")
        
        # Search for data
        search_params = DataSearchParams(
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z",
            page_size=50
        )
        
        data_response = client.data.search_data(search_params)
        if data_response.success:
            print(f"Found {len(data_response.data)} data points")
            
            # Process data points
            for data_point in data_response.data:
                print(f"Target: {data_point.get('target')}, "
                      f"Variable: {data_point.get('variable')}, "
                      f"Value: {data_point.get('value')}")
        
        # Create new data points
        new_data = [
            DataPoint(
                target="http://example.com/plant1",
                variable="http://example.com/height",
                date="2024-06-30T12:00:00Z",
                value=25.5,
                confidence=0.95
            )
        ]
        
        create_response = client.data.create_data(new_data)
        if create_response.success:
            print("Data points created successfully")
    
    finally:
        client.logout()


def example_project_management():
    """
    Example: Working with projects and experiments
    """
    from client import OpenSilexClient
    from modules.projects import ProjectCreationData, ProjectSearchParams
    
    client = OpenSilexClient(get_opensilex_base_url())
    
    try:
        # Authenticate and CHECK if successful
        auth_response = client.authenticate("admin@opensilex.org", "admin")
        
        if not auth_response.success:
            print(f"Authentication failed: {auth_response.message}")
            print(f"Errors: {auth_response.errors}")
            return
        
        print("Authentication successful!")
        
        # Search for projects
        search_params = ProjectSearchParams(
            name="wheat",
            year=2024,
            page_size=20
        )
        
        projects_response = client.projects.search_projects(search_params)
        if projects_response.success:
            print(f"Found {len(projects_response.data)} projects")
            
            for project in projects_response.data:
                print(f"Project: {project.get('name')}")
        else:
            print(f"Project search failed: {projects_response.message}")
        
        # Create a new project
        new_project = ProjectCreationData(
            name="Wheat Growth Study 2024",
            shortname="WGS2024",
            description="Study of wheat growth under various conditions",
            start_date="2024-01-01",
            end_date="2024-12-31",
            keywords=["wheat", "growth", "agriculture"]
        )
        
        create_response = client.projects.create_project(new_project)
        if create_response.success:
            print(f"Project created with URI: {create_response.data}")
        else:
            print(f"Failed to create project: {create_response.message}")
    
    finally:
        client.logout()


def example_variable_management():
    """
    Example: Working with variables and entities
    """
    from client import OpenSilexClient
    from modules.variables import VariableSearchParams, EntityCreationData
    
    client = OpenSilexClient(get_opensilex_base_url())
    
    try:
        # Authenticate and CHECK if successful
        auth_response = client.authenticate("admin@opensilex.org", "admin")
        
        if not auth_response.success:
            print(f"Authentication failed: {auth_response.message}")
            print(f"Errors: {auth_response.errors}")
            return
        
        print("Authentication successful!")
        
        # Search for variables
        search_params = VariableSearchParams(
            name="height",
            page_size=20
        )
        
        variables_response = client.variables.search_variables(search_params)
        if variables_response.success:
            print(f"Found {len(variables_response.data)} variables")
            
            for variable in variables_response.data:
                print(f"Variable: {variable.get('name')}")
        else:
            print(f"Variable search failed: {variables_response.message}")
        
        # Get variable data types
        datatypes_response = client.variables.get_variable_datatypes()
        if datatypes_response.success:
            print(f"Available data types: {datatypes_response.data}")
        
        # Create a new entity
        new_entity = EntityCreationData(
            name="Plant Height Measurement",
            description="Height measurement of plant specimens",
            rdf_type="http://purl.obolibrary.org/obo/NCIT_C25349"
        )
        
        create_response = client.variables.create_entity(new_entity)
        if create_response.success:
            print(f"Entity created with URI: {create_response.data}")
        else:
            print(f"Failed to create entity: {create_response.message}")
    
    finally:
        client.logout()


def example_context_manager():
    """
    Example: Using the client as a context manager
    """
    from client import OpenSilexClient
    
    # Using context manager ensures proper cleanup
    with OpenSilexClient("http://20.4.208.154:28081/rest") as client:
        # Authenticate
        auth_response = client.authenticate("admin@opensilex.org", "admin")
        
        if auth_response.success:
            # Do work here
            system_info = client.get_system_info()
            print(f"System info: {system_info.data}")
            
            # Logout is automatically called when exiting the context


def example_error_handling():
    """
    Example: Proper error handling
    """
    from client import OpenSilexClient
    from modules.base import APIException
    
    client = OpenSilexClient(get_opensilex_base_url())
    
    try:
        # Attempt authentication
        auth_response = client.authenticate("wrong_user", "wrong_password")
        
        if not auth_response.success:
            print(f"Authentication failed: {auth_response.errors}")
            return
        
        # Attempt to get system info
        system_response = client.get_system_info()
        
        if not system_response.success:
            print(f"Failed to get system info: {system_response.errors}")
            print(f"Status code: {system_response.status_code}")
    
    except APIException as e:
        print(f"API Exception: {e}")
        if e.status_code:
            print(f"Status code: {e.status_code}")
        if e.response_data:
            print(f"Response data: {e.response_data}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        # Always cleanup
        if client.is_authenticated():
            client.logout()


if __name__ == "__main__":
    # Setup logging
    setup_logging("INFO")
    
    #Run examples (uncomment to test)
    #example_basic_usage()
    #example_data_management()
    #example_project_management()
    #example_variable_management()
    #example_context_manager()
    #example_error_handling()
    
    #print("OpenSilex API Client examples ready to run!")
    #print("Uncomment the example functions in __main__ to test them.")