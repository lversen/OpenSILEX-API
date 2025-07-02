from client import OpenSilexClient
from modules.facilities import FacilitySearchParams
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

    # Test Facilities Module
    print("\n--- Testing Facilities Module ---")
    facilities_client = client.facilities
    search_response = facilities_client.search_facilities(FacilitySearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search facilities successful.")
            facility_uri = search_response.data[0]["uri"]
            get_response = facilities_client.get_facility_by_uri(facility_uri)
            if get_response.success:
                print(f"Get facility by URI successful: {get_response.data['name']}")
            else:
                print(f"Get facility by URI failed: {get_response.errors}")
        else:
            print("Search facilities returned no data, but the call was successful.")
    else:
        print(f"Search facilities failed: {search_response.errors}")

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()
