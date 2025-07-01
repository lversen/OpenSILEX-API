import csv
from client import OpenSilexClient
from modules.data import DataPoint
from modules.variables import VariableSearchParams
from modules.projects import ScientificObjectSearchParams

def import_csv_data(client: OpenSilexClient, file_path: str):
    # Fetch a valid scientific object URI
    scientific_objects_response = client.projects.search_scientific_objects(ScientificObjectSearchParams(page_size=1))
    if not scientific_objects_response.success or not scientific_objects_response.data:
        print("Could not fetch a scientific object. Please ensure there is at least one scientific object in the system.")
        return
    valid_target_uri = scientific_objects_response.data[0]['uri']
    print(f"Using scientific object URI: {valid_target_uri}")

    # Fetch or create a valid variable URI
    variables_response = client.variables.search_variables(VariableSearchParams(page_size=1))
    if not variables_response.success or not variables_response.data:
        print("No variables found. Attempting to create a mock variable...")
        
        mock_variable_data = {
            "uri": "http://www.opensilex.org/id/variables/mock_variable_for_import",
            "name": "Mock Variable for Import",
            "method": "http://www.opensilex.org/id/methods/mock_method",
            "unit": "http://www.opensilex.org/id/units/mock_unit",
            "entity": "http://www.opensilex.org/id/entities/mock_entity",
            "dataType": "http://www.w3.org/2001/XMLSchema#integer",
            "characteristic": "http://www.opensilex.org/id/characteristics/mock_characteristic"
        }
        create_var_response = client.variables.create_variable(mock_variable_data)
        if create_var_response.success:
            valid_variable_uri = mock_variable_data['uri']
            print(f"Mock variable created: {valid_variable_uri}")
        else:
            print(f"Failed to create mock variable: {create_var_response.errors}. Full response: {create_var_response.data}")
            return
    else:
        valid_variable_uri = variables_response.data[0]['uri']
        print(f"Using variable URI: {valid_variable_uri}")

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
                target = valid_target_uri
                date = row[3]
                variable = valid_variable_uri
                value = row[4]
                
                data_points.append(DataPoint(
                    target=target,
                    variable=variable,
                    date=date,
                    value=value
                ))
            except IndexError as e:
                print(f"Error parsing row: {row} - {e}")
                continue

    if not data_points:
        print("No data points to import.")
        return

    print(f"Attempting to import {len(data_points)} data points...")
    response = client.data.create_data(data_points)

    if response.success:
        print("Data imported successfully!")
    else:
        print(f"Data import failed: {response.message}")
        if response.errors:
            print(f"Errors: {response.errors}")

def main():
    client = OpenSilexClient("http://20.4.208.154:28081/rest")

    auth_response = client.authenticate("admin@opensilex.org", "admin")
    if not auth_response.success:
        print(f"Authentication failed: {auth_response.message}")
        return

    print("Authentication successful.")

    import_csv_data(client, "C:/Users/siv017/Documents/GitHub/OpenSILEX-API/example_data.csv")

    client.logout()
    print("Logout successful.")

if __name__ == "__main__":
    main()