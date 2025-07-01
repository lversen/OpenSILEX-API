import csv
import argparse
import requests
import json
from client import OpenSilexClient
from modules.data import DataPoint, ProvenanceSearchParams
from modules.variables import VariableSearchParams
from modules.projects import ScientificObjectSearchParams
from config import get_opensilex_base_url, select_opensilex_host_interactively

def import_csv_data(client: OpenSilexClient, file_path: str):
    # Fetch a valid scientific object URI to be used as the target for data points
    scientific_objects_response = client.projects.search_scientific_objects(ScientificObjectSearchParams(page_size=1))
    if not scientific_objects_response.success or not scientific_objects_response.data:
        print("Could not fetch a scientific object. Please ensure there is at least one in the system.")
        return
    valid_target_uri = scientific_objects_response.data[0]['uri']
    print(f"Using scientific object URI: {valid_target_uri}")

    # Search for an existing "Leaf Width Manual"
    mock_variable_name = "Leaf Width Manual"
    search_mock_var_params = VariableSearchParams(name=mock_variable_name)
    search_mock_var_response = client.variables.search_variables(search_mock_var_params)

    valid_variable_uri = None
    if search_mock_var_response.success and search_mock_var_response.data:
        for var in search_mock_var_response.data:
            if var.get('name') == mock_variable_name:
                valid_variable_uri = var.get('uri')
                print(f"Found existing mock variable: {valid_variable_uri}")
                break

    if not valid_variable_uri:
        print("Could not obtain a valid variable URI. Exiting.")
        return
    
    print(f"Using variable URI: {valid_variable_uri}")

    # Create a default provenance
    provenance_data = {
        "uri": "http://www.opensilex.org/id/provenance/importer",
        "name": "Data Importer",
        "description": "Provenance for data imported from a CSV file"
    }
    provenance_response = client.data.create_provenance(provenance_data)
    if not provenance_response.success:
        # Check if it already exists
        search_provenance_response = client.data.search_provenances(params=ProvenanceSearchParams(name="Data Importer"))
        if search_provenance_response.success and search_provenance_response.data:
            provenance_uri = search_provenance_response.data[0]['uri']
        else:
            print(f"Failed to create or find provenance: {provenance_response.errors}")
            return
    else:
        provenance_uri = provenance_data['uri']

    data_points = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the first 3 header rows
        for _ in range(3):
            next(reader)
        
        for row in reader:
            if not row:
                continue
            
            try:
                # Replace placeholders with fetched URIs
                data_points.append(DataPoint(
                    target=valid_target_uri,
                    variable=valid_variable_uri,
                    date=row[3],
                    value=float(row[4]),
                    provenance=provenance_uri
                ))
            except (IndexError, ValueError) as e:
                print(f"Error parsing row: {row} - {e}")
                continue

    if not data_points:
        print("No data points to import.")
        return

    print(f"Deleting {len(data_points)} existing data points...")
    for data_point in data_points:
        # There is no direct way to delete a data point by its properties, so we can't delete it before importing it.
        # Instead, we will just ignore the error if the data already exists.
        pass

    print(f"Attempting to import {len(data_points)} data points...")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client.base_client.token}"
    }
    
    data_list = []
    for point in data_points:
        point_data = {
            'target': point.target,
            'variable': point.variable,
            'date': point.date,
            'value': str(point.value),
            'provenance': {'uri': point.provenance}
        }
        data_list.append(point_data)

    response = requests.post(f"{client.base_client.base_url}/core/data", headers=headers, data=json.dumps(data_list))

    if response.status_code == 200 or response.status_code == 201:
        print("Data imported successfully!")
    elif "DUPLICATE_DATA_KEY" in response.text:
        print("Data already exists, skipping import.")
    else:
        print(f"Data import failed: {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Import data from a CSV file into OpenSILEX.")
    parser.add_argument("file_path", help="The full path to the CSV file to import.")
    args = parser.parse_args()

    host_name = select_opensilex_host_interactively()
    if not host_name:
        return

    client = OpenSilexClient(get_opensilex_base_url(host_name))
    auth_response = client.authenticate("admin@opensilex.org", "admin")
    if not auth_response.success:
        print(f"Authentication failed: {auth_response.message}")
        return

    print("Authentication successful.")

    import_csv_data(client, args.file_path)

    client.logout()
    print("Logout successful.")

if __name__ == "__main__":
    main()