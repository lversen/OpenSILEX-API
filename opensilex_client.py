"""
OpenSilex API Python Client
A comprehensive Python implementation for interacting with the OpenSilex API
"""

import requests
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import os
from pathlib import Path
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SSHConfigParser:
    """
    Parser for SSH config files to extract host information.
    """
    
    @staticmethod
    def parse_ssh_config(config_path: str = None) -> Dict[str, Dict[str, str]]:
        """
        Parse SSH config file and return host configurations.
        
        Args:
            config_path: Path to SSH config file (defaults to ~/.ssh/config)
            
        Returns:
            Dictionary mapping host names to their configurations
        """
        if config_path is None:
            # Handle both Unix and Windows paths
            ssh_dir = Path.home() / ".ssh"
            config_path = ssh_dir / "config"
            
            # On Windows, also check without dot
            if not config_path.exists() and os.name == 'nt':
                ssh_dir = Path.home() / "ssh"
                config_path = ssh_dir / "config"
        
        hosts = {}
        current_host = None
        
        try:
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse host declaration
                    if line.lower().startswith('host '):
                        current_host = line.split()[1]
                        hosts[current_host] = {}
                    
                    # Parse host attributes
                    elif current_host and ' ' in line:
                        parts = line.split(None, 1)
                        if len(parts) == 2:
                            key, value = parts
                            hosts[current_host][key.lower()] = value.strip()
        
        except FileNotFoundError:
            logger.warning(f"SSH config file not found: {config_path}")
        except Exception as e:
            logger.error(f"Error parsing SSH config: {str(e)}")
        
        return hosts
    
    @staticmethod
    def get_host_ip(host_name: str, ssh_config: Dict[str, Dict[str, str]] = None) -> Optional[str]:
        """
        Get IP address for a host from SSH config.
        
        Args:
            host_name: Name of the host in SSH config
            ssh_config: Pre-parsed SSH config (optional)
            
        Returns:
            IP address or hostname if found, None otherwise
        """
        if ssh_config is None:
            ssh_config = SSHConfigParser.parse_ssh_config()
        
        if host_name in ssh_config:
            return ssh_config[host_name].get('hostname', ssh_config[host_name].get('host'))
        
        return None


class OpenSilexClient:
    """
    A Python client for interacting with the OpenSilex API.
    
    This client handles authentication, token management, and provides methods
    for common API operations.
    """
    
    def __init__(self, base_url: str = None, 
                 username: str = "admin@opensilex.org", 
                 password: str = "admin",
                 ssh_host: str = None,
                 use_ssh_config: bool = True):
        """
        Initialize the OpenSilex client.
        
        Args:
            base_url: The base URL of the OpenSilex API (if None, will try SSH config)
            username: Username for authentication
            password: Password for authentication
            ssh_host: SSH host name to look up in SSH config
            use_ssh_config: Whether to check SSH config for base URL
        """
        # Try to get base URL from SSH config if not provided
        if base_url is None and use_ssh_config:
            base_url = self._get_base_url_from_ssh(ssh_host)
        
        # Fall back to default if still None
        if base_url is None:
            base_url = "http://opensilex.org/sandbox/rest"
            logger.info(f"Using default base URL: {base_url}")
        
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.headers = {"Content-Type": "application/json"}
        
        logger.info(f"OpenSilex client initialized with base URL: {self.base_url}")
    
    def _get_base_url_from_ssh(self, ssh_host: str = None) -> Optional[str]:
        """
        Get base URL from SSH config.
        
        Args:
            ssh_host: SSH host name to look up (if None, tries common names)
            
        Returns:
            Base URL constructed from SSH config, or None if not found
        """
        ssh_config = SSHConfigParser.parse_ssh_config()
        
        # If no specific host given, try common names
        if ssh_host is None:
            common_hosts = [
                'opensilex', 'opensilex-vm', 'opensilex-dev', 'vm',
                'phis', 'phis-vm', 'phis-dev', 'phis-prod', 'phis-test'
            ]
            for host in common_hosts:
                if host in ssh_config:
                    ssh_host = host
                    logger.info(f"Found SSH host '{host}' in config")
                    break
        
        if ssh_host and ssh_host in ssh_config:
            vm_ip = SSHConfigParser.get_host_ip(ssh_host, ssh_config)
            if vm_ip:
                base_url = f"http://{vm_ip}:28081/rest"
                logger.info(f"Found VM IP from SSH config: {vm_ip}")
                return base_url
        
        if ssh_config:
            available_hosts = list(ssh_config.keys())
            logger.warning(f"Could not find VM configuration in SSH config. Available hosts: {available_hosts}")
        else:
            logger.warning("No SSH config found or empty config file")
        return None
    
    @classmethod
    def from_ssh_config(cls, ssh_host: str = None, username: str = None, password: str = None):
        """
        Create an OpenSilexClient instance using SSH config for the base URL.
        
        Args:
            ssh_host: SSH host name to look up in config
            username: Username for authentication (optional)
            password: Password for authentication (optional)
            
        Returns:
            OpenSilexClient instance
        """
        return cls(
            base_url=None,
            username=username or "admin@opensilex.org",
            password=password or "admin",
            ssh_host=ssh_host,
            use_ssh_config=True
        )
        
    def authenticate(self) -> bool:
        """
        Authenticate with the OpenSilex API and obtain an access token.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            auth_data = {
                "identifier": self.username,
                "password": self.password
            }
            
            response = requests.post(
                f"{self.base_url}/security/authenticate",
                json=auth_data,
                headers=self.headers
            )
            
            if response.status_code == 200:
                result = response.json()
                self.token = result["result"]["token"]
                self.headers["Authorization"] = f"Bearer {self.token}"
                logger.info("Authentication successful")
                return True
            else:
                logger.error(f"Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                      data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the API with automatic token refresh if needed.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            Response data as dictionary or None if error
        """
        if not self.token:
            if not self.authenticate():
                return None
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )
            
            # If unauthorized, try to re-authenticate
            if response.status_code == 401:
                logger.info("Token expired, re-authenticating...")
                if self.authenticate():
                    response = requests.request(
                        method=method,
                        url=url,
                        headers=self.headers,
                        params=params,
                        json=data
                    )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Request error: {str(e)}")
            return None
    
    # === Experiments Methods ===
    
    def get_experiments(self, page: int = 0, page_size: int = 20) -> Optional[List[Dict]]:
        """
        Get list of experiments.
        
        Args:
            page: Page number (0-indexed)
            page_size: Number of items per page
            
        Returns:
            List of experiments or None if error
        """
        params = {"page": page, "page_size": page_size}
        result = self._make_request("GET", "/core/experiments", params=params)
        return result.get("result", []) if result else None
    
    def get_experiment(self, uri: str) -> Optional[Dict]:
        """
        Get details of a specific experiment.
        
        Args:
            uri: URI of the experiment
            
        Returns:
            Experiment details or None if error
        """
        params = {"uri": uri}
        result = self._make_request("GET", "/core/experiments", params=params)
        return result.get("result", [{}])[0] if result and result.get("result") else None
    
    # === Scientific Objects Methods ===
    
    def get_scientific_objects(self, experiment_uri: Optional[str] = None, 
                              rdf_type: Optional[str] = None,
                              page: int = 0, page_size: int = 20) -> Optional[List[Dict]]:
        """
        Get scientific objects (plants, plots, etc.).
        
        Args:
            experiment_uri: Filter by experiment
            rdf_type: Filter by type (e.g., "vocabulary:Plant")
            page: Page number
            page_size: Number of items per page
            
        Returns:
            List of scientific objects or None if error
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if experiment_uri:
            params["experiment"] = experiment_uri
        if rdf_type:
            params["rdf_type"] = rdf_type
            
        result = self._make_request("GET", "/core/scientific_objects", params=params)
        return result.get("result", []) if result else None
    
    # === Variables Methods ===
    
    def get_variables(self, page: int = 0, page_size: int = 20) -> Optional[List[Dict]]:
        """
        Get list of variables (measurement types).
        
        Args:
            page: Page number
            page_size: Number of items per page
            
        Returns:
            List of variables or None if error
        """
        params = {"page": page, "page_size": page_size}
        result = self._make_request("GET", "/core/variables", params=params)
        return result.get("result", []) if result else None
    
    # === Data Methods ===
    
    def get_data(self, experiment_uri: Optional[str] = None,
                 variable_uri: Optional[str] = None,
                 scientific_object_uri: Optional[str] = None,
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None,
                 page: int = 0, page_size: int = 20) -> Optional[List[Dict]]:
        """
        Get measurement data.
        
        Args:
            experiment_uri: Filter by experiment
            variable_uri: Filter by variable
            scientific_object_uri: Filter by scientific object
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            page: Page number
            page_size: Number of items per page
            
        Returns:
            List of data points or None if error
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if experiment_uri:
            params["experiment"] = experiment_uri
        if variable_uri:
            params["variable"] = variable_uri
        if scientific_object_uri:
            params["scientific_object"] = scientific_object_uri
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        result = self._make_request("GET", "/core/data", params=params)
        return result.get("result", []) if result else None
    
    def post_data(self, data_list: List[Dict]) -> bool:
        """
        Post new measurement data.
        
        Args:
            data_list: List of data points to post
            
        Example data format:
            [{
                "date": "2024-01-15T10:30:00Z",
                "variable": "http://opensilex.org/id/variables/plant_height",
                "value": 25.5,
                "scientific_object": "http://opensilex.org/id/plants/plant001"
            }]
            
        Returns:
            True if successful, False otherwise
        """
        result = self._make_request("POST", "/core/data", data=data_list)
        return result is not None
    
    # === Devices Methods ===
    
    def get_devices(self, page: int = 0, page_size: int = 20) -> Optional[List[Dict]]:
        """
        Get list of devices (sensors, cameras, etc.).
        
        Args:
            page: Page number
            page_size: Number of items per page
            
        Returns:
            List of devices or None if error
        """
        params = {"page": page, "page_size": page_size}
        result = self._make_request("GET", "/core/devices", params=params)
        return result.get("result", []) if result else None
    
    # === Events Methods ===
    
    def get_events(self, experiment_uri: Optional[str] = None,
                   page: int = 0, page_size: int = 20) -> Optional[List[Dict]]:
        """
        Get events (irrigation, treatments, etc.).
        
        Args:
            experiment_uri: Filter by experiment
            page: Page number
            page_size: Number of items per page
            
        Returns:
            List of events or None if error
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if experiment_uri:
            params["experiment"] = experiment_uri
            
        result = self._make_request("GET", "/core/events", params=params)
        return result.get("result", []) if result else None
    
    # === Utility Methods ===
    
    def get_all_pages(self, method_name: str, **kwargs) -> List[Dict]:
        """
        Get all pages of data from a paginated endpoint.
        
        Args:
            method_name: Name of the method to call
            **kwargs: Arguments to pass to the method
            
        Returns:
            Combined list of all results
        """
        all_results = []
        page = 0
        page_size = 50  # Larger page size for efficiency
        
        method = getattr(self, method_name)
        
        while True:
            kwargs['page'] = page
            kwargs['page_size'] = page_size
            
            results = method(**kwargs)
            
            if not results:
                break
                
            all_results.extend(results)
            
            if len(results) < page_size:
                break
                
            page += 1
            
        return all_results


# === Example Usage Functions ===

def example_basic_usage():
    """Example of basic API usage."""
    # Initialize client (will automatically check SSH config)
    client = OpenSilexClient()
    
    # Authenticate
    if not client.authenticate():
        print("Authentication failed!")
        return
    
    # Get experiments
    print("\n=== Experiments ===")
    experiments = client.get_experiments()
    if experiments:
        for exp in experiments[:3]:  # Show first 3
            print(f"- {exp.get('name', 'N/A')} ({exp.get('uri', 'N/A')})")
    
    # Get variables
    print("\n=== Variables ===")
    variables = client.get_variables()
    if variables:
        for var in variables[:5]:  # Show first 5
            print(f"- {var.get('name', 'N/A')} ({var.get('uri', 'N/A')})")


def example_data_retrieval():
    """Example of retrieving experimental data."""
    client = OpenSilexClient()
    
    if not client.authenticate():
        print("Authentication failed!")
        return
    
    # Get first experiment
    experiments = client.get_experiments(page_size=1)
    if not experiments:
        print("No experiments found")
        return
    
    experiment_uri = experiments[0]['uri']
    print(f"Working with experiment: {experiments[0]['name']}")
    
    # Get scientific objects in this experiment
    print("\n=== Scientific Objects ===")
    objects = client.get_scientific_objects(experiment_uri=experiment_uri)
    if objects:
        for obj in objects[:5]:
            print(f"- {obj.get('name', 'N/A')} (Type: {obj.get('rdf_type', 'N/A')})")
    
    # Get data for the experiment
    print("\n=== Measurement Data ===")
    data = client.get_data(experiment_uri=experiment_uri, page_size=10)
    if data:
        for d in data[:5]:
            print(f"- Date: {d.get('date', 'N/A')}, "
                  f"Variable: {d.get('variable', 'N/A')}, "
                  f"Value: {d.get('value', 'N/A')}")


def example_data_export():
    """Example of exporting data to CSV."""
    import csv
    
    client = OpenSilexClient()
    
    if not client.authenticate():
        print("Authentication failed!")
        return
    
    # Get all data for a specific timeframe
    print("Fetching data...")
    data = client.get_all_pages(
        'get_data',
        start_date="2017-01-01T00:00:00Z",
        end_date="2017-12-31T23:59:59Z"
    )
    
    if not data:
        print("No data found")
        return
    
    # Export to CSV
    filename = "opensilex_data_export.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'variable', 'value', 'scientific_object', 'experiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for d in data:
            writer.writerow({
                'date': d.get('date', ''),
                'variable': d.get('variable', ''),
                'value': d.get('value', ''),
                'scientific_object': d.get('scientific_object', ''),
                'experiment': d.get('experiment', '')
            })
    
    print(f"Data exported to {filename} ({len(data)} records)")


if __name__ == "__main__":
    # Example 1: Using SSH config (automatic detection)
    print("=== Example 1: Auto-detect from SSH config ===")
    client1 = OpenSilexClient()
    print(f"Base URL: {client1.base_url}")
    
    # Example 2: Using specific SSH host (e.g., phis-prod)
    print("\n=== Example 2: Specific SSH host ===")
    # For your case, use:
    client2 = OpenSilexClient.from_ssh_config(ssh_host="phis-prod")
    print(f"Base URL: {client2.base_url}")
    
    # Example 3: Manual URL (bypassing SSH config)
    print("\n=== Example 3: Manual URL ===")
    client3 = OpenSilexClient(
        base_url="http://20.4.208.154:28081/rest",
        use_ssh_config=False
    )
    print(f"Base URL: {client3.base_url}")
    
    # Run examples
    print("\n\n=== Basic Usage Example ===")
    example_basic_usage()
    
    print("\n\n=== Data Retrieval Example ===")
    example_data_retrieval()
    
    print("\n\n=== Data Export Example ===")
    example_data_export()