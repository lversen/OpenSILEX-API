from client import OpenSilexClient
from modules.variables import VariableSearchParams
from modules.projects import ProjectSearchParams
from modules.data import DataSearchParams
from config import get_opensilex_base_url, select_opensilex_host_interactively

def main():
    # Allow user to select host
    host_name = select_opensilex_host_interactively()
    if not host_name:
        return

    # Initialize client
    client = OpenSilexClient(get_opensilex_base_url(host_name))

    # Authenticate
    auth_response = client.authenticate("admin@opensilex.org", "admin")
    if not auth_response.success:
        print(f"Authentication failed: {auth_response.message}")
        return

    print("Authentication successful.")

    # Test Variables Module
    print("\n--- Testing Variables Module ---")
    variables_client = client.variables
    search_response = variables_client.search_variables(VariableSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search variables successful.")
            variable_uri = search_response.data[0]["uri"]
            get_response = variables_client.get_variable_by_uri(variable_uri)
            if get_response.success:
                print(f"Get variable by URI successful: {get_response.data['name']}")
            else:
                print(f"Get variable by URI failed: {get_response.errors}")
        else:
            print("Search variables returned no data, but the call was successful.")
    else:
        print(f"Search variables failed: {search_response.errors}")

    # Test Projects Module
    print("\n--- Testing Projects Module ---")
    projects_client = client.projects
    search_response = projects_client.search_projects(ProjectSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search projects successful.")
            project_uri = search_response.data[0]["uri"]
            get_response = projects_client.get_project_by_uri(project_uri)
            if get_response.success:
                print(f"Get project by URI successful: {get_response.data['name']}")
            else:
                print(f"Get project by URI failed: {get_response.errors}")
        else:
            print("Search projects returned no data, but the call was successful.")
    else:
        print(f"Search projects failed: {search_response.errors}")

    # Test Data Module
    print("\n--- Testing Data Module ---")
    data_client = client.data
    search_response = data_client.search_data(DataSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search data successful.")
            data_uri = search_response.data[0]["uri"]
            get_response = data_client.get_data_by_uri(data_uri)
            if get_response.success:
                print(f"Get data by URI successful: {get_response.data['value']}")
            else:
                print(f"Get data by URI failed: {get_response.errors}")
        else:
            print("Search data returned no data, but the call was successful.")
    else:
        print(f"Search data failed: {search_response.errors}")

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()



