from client import OpenSilexClient
from modules.variables import VariableSearchParams
from config import get_opensilex_base_url

def main():
    # Allow user to select host
    base_url = get_opensilex_base_url(non_interactive=True)
    if not base_url:
        return

    # Initialize client
    client = OpenSilexClient(base_url)

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

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()
