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
    # Check for --dry-run flag
    dry_run = "--dry-run" in sys.argv

    # Get base URL from SSH config
    if not dry_run:
        try:
            base_url = get_opensilex_base_url(non_interactive=True)
        except (ValueError, FileNotFoundError) as e:
            print(f"Error getting base URL: {e}")
            print("Please ensure your SSH config is set up correctly.")
            return
    else:
        base_url = "http://localhost:8080/opensilex/rest/"  # Dummy URL for dry run

    # Initialize clients
    client = OpenSilexClient(base_url=base_url)
    mock_client = MockClient()

    # Authenticate
    if not dry_run:
        print("Authenticating with default admin credentials...")
        auth_response = client.authenticate(identifier="admin@opensilex.org", password="admin")
        if auth_response.status_code != 200:
            print(f"Authentication failed: {auth_response.data}")
            return
        print("Authentication successful.")
    else:
        print("DRY RUN: Skipping authentication.")

    # Create organizations
    print("Creating mock organizations...")
    mock_organizations = mock_client.create_mock_organizations(3)
    organization_uris = []
    for org_data in mock_organizations:
        if not dry_run:
            response = client.organizations.create_organization(org_data)
            if response.status_code == 201:
                org_uri = response.data
                organization_uris.append(org_uri)
                print(f"  - Created organization: {org_data.name} (URI: {org_uri})")
            else:
                print(f"  - Failed to create organization: {org_data.name} ({response.data})")
        else:
            print(f"  - (Dry Run) Would create organization: {org_data.name}")

    # Create projects, experiments, and scientific objects
    print("\nCreating mock projects, experiments, and scientific objects...")
    mock_projects = mock_client.create_mock_projects(2)
    for project_data in mock_projects:
        project_uri = f"http://example.com/project/{project_data.name.replace(' ', '_')}"
        if not dry_run:
            # Create project
            project_response = client.projects.create_project(project_data)
            if project_response.status_code == 201:
                project_uri = project_response.data
                print(f"\n- Created project: {project_data.name}")
            else:
                print(f"\n- Failed to create project: {project_data.name} ({project_response.data})")
                continue
        else:
            print(f"\n- (Dry Run) Would create project: {project_data.name}")

        # Create experiments for the project
        mock_experiments = mock_client.create_mock_experiments(2, project_uri)
        for exp_data in mock_experiments:
            exp_uri = f"http://example.com/experiment/{exp_data.name.replace(' ', '_')}"
            if not dry_run:
                exp_response = client.experiments.create_experiment(exp_data)
                if exp_response.status_code == 201:
                    exp_uri = exp_response.data
                    print(f"  - Created experiment: {exp_data.name}")
                else:
                    print(f"  - Failed to create experiment: {exp_data.name} ({exp_response.data})")
                    continue
            else:
                print(f"  - (Dry Run) Would create experiment: {exp_data.name}")

            # Create scientific objects for the experiment
            mock_objects = mock_client.create_mock_scientific_objects(5, exp_uri)
            for obj_data in mock_objects:
                if not dry_run:
                    obj_response = client.scientific_objects.create_scientific_object(obj_data)
                    if obj_response.status_code == 201:
                        print(f"    - Created scientific object: {obj_data.name}")
                    else:
                        print(f"    - Failed to create scientific object: {obj_data.name} ({obj_response.data})")
                else:
                    print(f"    - (Dry Run) Would create scientific object: {obj_data.name}")

    # Create devices
    print("\nCreating mock devices...")
    mock_devices = mock_client.create_mock_devices(4)
    for device_data in mock_devices:
        if not dry_run:
            response = client.devices.create_device(device_data)
            if response.status_code == 201:
                print(f"  - Created device: {device_data.name}")
            else:
                print(f"  - Failed to create device: {device_data.name} ({response.data})")
        else:
            print(f"  - (Dry Run) Would create device: {device_data.name}")

    # Create persons
    print("\nCreating mock persons...")
    mock_persons = mock_client.create_mock_persons(5)
    for person_data in mock_persons:
        if not dry_run:
            response = client.persons.create_person(person_data)
            if response.status_code == 201:
                print(f"  - Created person: {person_data.first_name} {person_data.last_name}")
            else:
                print(f"  - Failed to create person: {person_data.first_name} {person_data.last_name} ({response.data})")
        else:
            print(f"  - (Dry Run) Would create person: {person_data.first_name} {person_data.last_name}")

    # Create sites
    print("\nCreating mock sites...")
    mock_sites = mock_client.create_mock_sites(3, organization_uris)
    for site_data in mock_sites:
        if not dry_run:
            response = client.sites.create_site(site_data)
            if response.status_code == 201:
                print(f"  - Created site: {site_data.name}")
            else:
                print(f"  - Failed to create site: {site_data.name} ({response.data})")
        else:
            print(f"  - (Dry Run) Would create site: {site_data.name}")

    # Create facilities
    print("\nCreating mock facilities...")
    mock_facilities = mock_client.create_mock_facilities(2)
    for facility_data in mock_facilities:
        if not dry_run:
            response = client.facilities.create_facility(facility_data)
            if response.status_code == 201:
                print(f"  - Created facility: {facility_data.name}")
            else:
                print(f"  - Failed to create facility: {facility_data.name} ({response.data})")
        else:
            print(f"  - (Dry Run) Would create facility: {facility_data.name}")

    # Create variables
    print("\nCreating mock variables...")
    mock_variables = mock_client.create_mock_variables(10)
    for var_data in mock_variables:
        if not dry_run:
            response = client.variables.create_variable(var_data)
            if response.status_code == 201:
                print(f"  - Created variable: {var_data.name}")
            else:
                print(f"  - Failed to create variable: {var_data.name} ({response.data})")
        else:
            print(f"  - (Dry Run) Would create variable: {var_data.name}")

    # Logout
    if not dry_run:
        print("\nLogging out...")
        client.logout()
    print("Done.")

if __name__ == "__main__":
    main()
