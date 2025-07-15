from client import OpenSilexClient
from modules.sites import SiteSearchParams
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

    # Test Sites Module
    print("\n--- Testing Sites Module ---")
    sites_client = client.sites
    search_response = sites_client.search_sites(SiteSearchParams(page_size=1))
    if search_response.success:
        if search_response.data:
            print("Search sites successful.")
            site_uri = search_response.data[0]["uri"]
            get_response = sites_client.get_site_by_uri(site_uri)
            if get_response.success:
                print(f"Get site by URI successful: {get_response.data['name']}")
            else:
                print(f"Get site by URI failed: {get_response.errors}")
        else:
            print("Search sites returned no data, but the call was successful.")
    else:
        print(f"Search sites failed: {search_response.errors}")

    # Logout
    client.logout()
    print("\nLogout successful.")

if __name__ == "__main__":
    main()
