"""
Fill Website with Mock Data
"""

import os
import sys

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client import OpenSilexClient
from tests.mock import MockClient
from config import get_opensilex_base_url

def main():
    """
    Main function to fill the website with mock data.
    """
    # Get base URL from SSH config
    try:
        base_url = get_opensilex_base_url(non_interactive=False)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error getting base URL: {e}")
        print("Please ensure your SSH config is set up correctly.")
        return

    # Initialize clients
    client = OpenSilexClient(base_url=base_url)
    mock_client = MockClient()

    # Authenticate
    print("Authenticating with default admin credentials...")
    auth_response = client.authenticate(identifier="admin@opensilex.org", password="admin")
    if auth_response.status_code != 200:
        print(f"Authentication failed: {auth_response.data}")
        return

    print("Authentication successful.")

    # Create organizations
    print("\nCreating mock organizations...")
    mock_organizations = mock_client.create_mock_organizations(3)
    for org_data in mock_organizations:
        response = client.organizations.create_organization(org_data)
        if response.status_code == 201:
            print(f"  - Created organization: {org_data.name}")
        else:
            print(f"  - Failed to create organization: {org_data.name} ({response.data})")

    # Create projects, experiments, and scientific objects
    print("\nCreating mock projects, experiments, and scientific objects...")
    mock_projects = mock_client.create_mock_projects(2)
    for project_data in mock_projects:
        # Create project
        project_response = client.projects.create_project(project_data)
        if project_response.status_code == 201:
            project_uri = project_response.data
            print(f"\n- Created project: {project_data.name}")

            # Create experiments for the project
            mock_experiments = mock_client.create_mock_experiments(2, project_uri)
            for exp_data in mock_experiments:
                exp_response = client.projects.create_experiment(exp_data.__dict__)
                if exp_response.status_code == 201:
                    exp_uri = exp_response.data
                    print(f"  - Created experiment: {exp_data.name}")

                    # Create scientific objects for the experiment
                    mock_objects = mock_client.create_mock_scientific_objects(5, exp_uri)
                    for obj_data in mock_objects:
                        obj_response = client.projects.create_scientific_object(obj_data.__dict__)
                        if obj_response.status_code == 201:
                            print(f"    - Created scientific object: {obj_data.name}")
                        else:
                            print(f"    - Failed to create scientific object: {obj_data.name} ({obj_response.data})")
                else:
                    print(f"  - Failed to create experiment: {exp_data.name} ({exp_response.data})")
        else:
            print(f"\n- Failed to create project: {project_data.name} ({project_response.data})")

    # Create devices
    print("\nCreating mock devices...")
    mock_devices = mock_client.create_mock_devices(4)
    for device_data in mock_devices:
        response = client.devices.create_device(device_data)
        if response.status_code == 201:
            print(f"  - Created device: {device_data.name}")
        else:
            print(f"  - Failed to create device: {device_data.name} ({response.data})")

    # Logout
    print("\nLogging out...")
    client.logout()
    print("Done.")

if __name__ == "__main__":
    main()
