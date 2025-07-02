from client import OpenSilexClient
from modules.experiments import ExperimentSearchParams
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

    # Test Experiments Module
    print("\n--- Testing Experiments Module ---")
    experiments_client = client.experiments
    search_response = experiments_client.search_experiments(ExperimentSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search experiments successful.")
            experiment_uri = search_response.data[0]["uri"]
            get_response = experiments_client.get_experiment_by_uri(experiment_uri)
            if get_response.success:
                print(f"Get experiment by URI successful: {get_response.data['name']}")
            else:
                print(f"Get experiment by URI failed: {get_response.errors}")
        else:
            print("Search experiments returned no data, but the call was successful.")
    else:
        print(f"Search experiments failed: {search_response.errors}")

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()
