# OpenSilex API Client Setup and Installation Guide

## Requirements (requirements.txt)
```
requests>=2.25.0
urllib3>=1.26.0
typing-extensions>=4.0.0
```

## Installation

### Option 1: Direct Installation
1. Save all the module files in a directory structure like this:
```
opensilex_client/
├── __init__.py
├── base.py
├── variables.py
├── data.py
├── projects.py
├── client.py
└── config.py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Package Installation (setup.py)
```python
from setuptools import setup, find_packages

setup(
    name="opensilex-client",
    version="1.0.0",
    description="Python client for OpenSilex API",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "urllib3>=1.26.0",
        "typing-extensions>=4.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
```

## __init__.py file
```python
"""
OpenSilex API Client
A modular Python client for interacting with OpenSilex APIs
"""

from .client import OpenSilexClient
from .base import BaseAPIClient, APIResponse, APIException
from .variables import VariablesClient, VariableSearchParams, EntityCreationData
from .data import DataClient, DataSearchParams, DataPoint, ProvenanceSearchParams
from .projects import ProjectsClient, ProjectSearchParams, ProjectCreationData, ExperimentSearchParams, ScientificObjectSearchParams
from .config import OpenSilexConfig, setup_logging

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    "OpenSilexClient",
    "BaseAPIClient", 
    "APIResponse", 
    "APIException",
    "VariablesClient", 
    "VariableSearchParams", 
    "EntityCreationData",
    "DataClient", 
    "DataSearchParams", 
    "DataPoint", 
    "ProvenanceSearchParams",
    "ProjectsClient", 
    "ProjectSearchParams", 
    "ProjectCreationData", 
    "ExperimentSearchParams", 
    "ScientificObjectSearchParams",
    "OpenSilexConfig", 
    "setup_logging"
]
```

## Quick Start Guide

### 1. Basic Usage
```python
from opensilex_client import OpenSilexClient

# Initialize client
client = OpenSilexClient("https://your-opensilex-instance.com/api")

# Authenticate
response = client.authenticate("username", "password")
if response.success:
    print("Connected successfully!")
    
    # Get system information
    info = client.get_system_info()
    print(f"System: {info.data}")
    
    # Logout
    client.logout()
```

### 2. Using Configuration
```python
from opensilex_client import OpenSilexClient, OpenSilexConfig

# Load config from file
config = OpenSilexConfig.from_file("config.json")

# Or from environment variables
config = OpenSilexConfig.from_env()

# Initialize client with config
client = OpenSilexClient(config.base_url, timeout=config.timeout)
```

### 3. Working with Data
```python
from opensilex_client import OpenSilexClient
from opensilex_client.data import DataSearchParams

client = OpenSilexClient("https://your-opensilex-instance.com/api")
client.authenticate("username", "password")

# Search for data
params = DataSearchParams(
    start_date="2024-01-01T00:00:00Z",
    end_date="2024-12-31T23:59:59Z",
    page_size=100
)

response = client.data.search_data(params)
if response.success:
    for data_point in response.data:
        print(f"Target: {data_point['target']}, Value: {data_point['value']}")

client.logout()
```

### 4. Managing Projects
```python
from opensilex_client import OpenSilexClient
from opensilex_client.projects import ProjectSearchParams, ProjectCreationData

client = OpenSilexClient("https://your-opensilex-instance.com/api")
client.authenticate("username", "password")

# Search projects
search_params = ProjectSearchParams(name="wheat", year=2024)
projects = client.projects.search_projects(search_params)

# Create new project
new_project = ProjectCreationData(
    name="New Research Project",
    description="Description of the project",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

result = client.projects.create_project(new_project)
print(f"Created project: {result.data}")

client.logout()
```

### 5. Context Manager Usage
```python
from opensilex_client import OpenSilexClient

# Automatic cleanup with context manager
with OpenSilexClient("https://your-opensilex-instance.com/api") as client:
    client.authenticate("username", "password")
    
    # Do your work here
    system_info = client.get_system_info()
    print(system_info.data)
    
    # Logout is automatic when exiting the context
```

## Configuration File Example (config.json)
```json
{
    "base_url": "https://your-opensilex-instance.com/api",
    "username": "your_username",
    "timeout": 30,
    "log_level": "INFO",
    "verify_ssl": true
}
```

## Environment Variables
```bash
export OPENSILEX_BASE_URL="https://your-opensilex-instance.com/api"
export OPENSILEX_USERNAME="your_username"
export OPENSILEX_PASSWORD="your_password"
export OPENSILEX_TIMEOUT="30"
export OPENSILEX_LOG_LEVEL="INFO"
export OPENSILEX_VERIFY_SSL="true"
```

## Features

### Core Features
- **Modular Design**: Separate modules for different API sections
- **Authentication Management**: Automatic token handling
- **Error Handling**: Comprehensive error handling and logging
- **Type Safety**: Full type hints and data classes
- **Context Manager**: Automatic resource cleanup
- **Configuration**: File and environment-based configuration

### API Coverage
- **Variables & Entities**: Full CRUD operations for variables and entities
- **Data Management**: Scientific data storage and retrieval
- **Projects & Experiments**: Project and experiment management
- **Organizations**: Organization management
- **Devices**: Device registration and management
- **Ontology**: Concept and ontology management
- **Documents**: Document upload and management
- **Events**: Event tracking and management
- **BRAPI**: Breeding API compatibility

### Data Classes and Parameters
- **Search Parameters**: Structured search parameters for all endpoints
- **Creation Data**: Type-safe data structures for creating resources
- **Response Handling**: Consistent response format across all operations

## Best Practices

1. **Always use authentication**: Most endpoints require authentication
2. **Handle errors gracefully**: Check response.success before using data
3. **Use context managers**: Ensures proper cleanup
4. **Configure logging**: Enable logging for debugging
5. **Use pagination**: Handle large datasets with pagination parameters
6. **Type checking**: Use the provided data classes for type safety

## Troubleshooting

### Common Issues
1. **Authentication failures**: Check credentials and API URL
2. **SSL certificate errors**: Set verify_ssl=False in config if needed
3. **Timeout issues**: Increase timeout value in configuration
4. **Permission errors**: Ensure user has required permissions

### Logging
Enable debug logging to see detailed API calls:
```python
from opensilex_client.config import setup_logging
setup_logging("DEBUG")
```

## API Documentation
For complete API documentation, refer to your OpenSilex instance's Swagger documentation at:
`https://your-opensilex-instance.com/api/swagger-ui.html`