from client import OpenSilexClient
from modules.scientific_objects import ScientificObjectSearchParams
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

    # Test Scientific Objects Module
    print("\n--- Testing Scientific Objects Module ---")
    scientific_objects_client = client.scientific_objects
    search_response = scientific_objects_client.search_scientific_objects(ScientificObjectSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search scientific objects successful.")
            scientific_object_uri = search_response.data[0]["uri"]
            get_response = scientific_objects_client.get_scientific_object_by_uri(scientific_object_uri)
            if get_response.success:
                print(f"Get scientific object by URI successful: {get_response.data['name']}")
            else:
                print(f"Get scientific object by URI failed: {get_response.errors}")
        else:
            print("Search scientific objects returned no data, but the call was successful.")
    else:
        print(f"Search scientific objects failed: {search_response.errors}")

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()
