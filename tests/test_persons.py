from client import OpenSilexClient
from modules.persons import PersonSearchParams
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

    # Test Persons Module
    print("\n--- Testing Persons Module ---")
    persons_client = client.persons
    search_response = persons_client.search_persons(PersonSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search persons successful.")
            person_uri = search_response.data[0]["uri"]
            get_response = persons_client.get_person_by_uri(person_uri)
            if get_response.success:
                print(f"Get person by URI successful: {get_response.data['first_name']}")
            else:
                print(f"Get person by URI failed: {get_response.errors}")
        else:
            print("Search persons returned no data, but the call was successful.")
    else:
        print(f"Search persons failed: {search_response.errors}")

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()
