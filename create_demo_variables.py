#!/usr/bin/env python3
"""
OpenSilex Smart Demo Variables Creator - SSH Config Only

This script creates demo ontology concepts (entities, characteristics, methods, units)
and variables in your OpenSilex system. It exclusively uses SSH config for host management
via get_host.py.

Fixed Issue: The original script was passing JSON objects to VariableCreationDTO.entity
instead of URI strings, causing "Cannot deserialize value of type java.net.URI" errors.

Usage:
    python create_demo_variables.py
    
The script will:
1. List available SSH config hosts
2. Prompt you to select one
3. Connect and create demo variables
    
SSH Config Example:
    Host my-opensilex-dev
        HostName 192.168.1.100
        Port 28081
        
    Host my-opensilex-prod
        HostName opensilex.company.com
        Port 8080
"""

import opensilexClientToolsPython
from opensilexClientToolsPython.models.variable_creation_dto import VariableCreationDTO
from opensilexClientToolsPython.models.entity_creation_dto import EntityCreationDTO
from opensilexClientToolsPython.models.characteristic_creation_dto import CharacteristicCreationDTO
from opensilexClientToolsPython.models.method_creation_dto import MethodCreationDTO
from opensilexClientToolsPython.models.unit_creation_dto import UnitCreationDTO
import sys
from config import get_opensilex_base_url, select_opensilex_host_interactively, select_opensilex_host_interactively





def get_credentials():
    """Get OpenSilex credentials from user"""
    print("\n🔐 OpenSilex Authentication:")
    print("-" * 30)
    
    identifier = input("Enter identifier (default: admin@opensilex.org): ").strip()
    if not identifier:
        identifier = "admin@opensilex.org"
    
    password = input("Enter password (default: admin): ").strip()
    if not password:
        password = "admin"
    
    return identifier, password

def connect_to_opensilex(host, identifier, password):
    """Connect to OpenSilex instance and return authenticated client"""
    try:
        pythonClient = opensilexClientToolsPython.ApiClient()
        pythonClient.connect_to_opensilex_ws(
            identifier=identifier,
            password=password,
            host=host
        )
        print(f"✓ Successfully connected to OpenSilex at {host}")
        return pythonClient
    except Exception as e:
        print(f"✗ Failed to connect to OpenSilex: {e}")
        return None

def get_existing_concepts(variables_api):
    """Retrieve all existing concepts (entities, characteristics, methods, units) and their URIs."""
    existing_concepts = {
        'entities': [],
        'characteristics': [],
        'methods': [],
        'units': []
    }

    try:
        for entity in variables_api.search_entities(page_size=1000):
            if hasattr(entity, 'uri') and hasattr(entity, 'name'):
                existing_concepts['entities'].append({'name': entity.name, 'uri': entity.uri})
    except Exception as e:
        print(f"  Could not retrieve existing entities: {e}")

    try:
        for char in variables_api.search_characteristics(page_size=1000):
            if hasattr(char, 'uri') and hasattr(char, 'name'):
                existing_concepts['characteristics'].append({'name': char.name, 'uri': char.uri})
    except Exception as e:
        print(f"  Could not retrieve existing characteristics: {e}")

    try:
        for method in variables_api.search_methods(page_size=1000):
            if hasattr(method, 'uri') and hasattr(method, 'name'):
                existing_concepts['methods'].append({'name': method.name, 'uri': method.uri})
    except Exception as e:
        print(f"  Could not retrieve existing methods: {e}")

    try:
        for unit in variables_api.search_units(page_size=1000):
            if hasattr(unit, 'uri') and hasattr(unit, 'name'):
                existing_concepts['units'].append({'name': unit.name, 'uri': unit.uri})
    except Exception as e:
        print(f"  Could not retrieve existing units: {e}")

    # Check if any concepts were found
    if any(existing_concepts.values()):
        return existing_concepts
    else:
        return {}

def extract_uri_from_response(response):
    """Extract URI string from API response (handles various response formats)"""
    
    # Handle dictionary response with 'result' key (the format your API is returning)
    if isinstance(response, dict):
        if 'result' in response and isinstance(response['result'], list):
            if len(response['result']) > 0:
                return response['result'][0]  # Return the first URI in the result list
        elif 'uri' in response:
            return response['uri']
    
    # Handle string response
    elif isinstance(response, str):
        return response
    
    # Handle object with uri attribute
    elif hasattr(response, 'uri'):
        return response.uri
    
    # Handle object with __dict__
    elif hasattr(response, '__dict__'):
        response_dict = response.__dict__
        if 'uri' in response_dict:
            return response_dict['uri']
        # Sometimes the response might have other patterns
        for key, value in response_dict.items():
            if 'uri' in key.lower() and isinstance(value, str):
                return value
    
    # If we still haven't found it, convert to string and see if it looks like a URI
    response_str = str(response)
    if response_str.startswith('http') or response_str.startswith('opensilex'):
        return response_str
    else:
        print(f"Warning: Could not extract URI from response: {response} (type: {type(response)})")
        return None

def list_existing_concepts(variables_api):
    """List existing concepts in the system"""
    print("\n🔍 Existing concepts in the system:")
    
    try:
        # List entities
        entities_response = variables_api.search_entities(page_size=50)
        if entities_response:
            entities_list = list(entities_response) if hasattr(entities_response, '__iter__') else []
            if entities_list:
                print(f"\n📦 Entities ({len(entities_list)}):")
                for entity in entities_list[:10]:  # Show first 10
                    name = entity.name if hasattr(entity, 'name') else 'Unknown'
                    uri = entity.uri if hasattr(entity, 'uri') else 'No URI'
                    print(f"  - {name} ({uri})")
                if len(entities_list) > 10:
                    print(f"  ... and {len(entities_list) - 10} more")
    except Exception as e:
        print(f"  Could not list entities: {e}")
    
    try:
        # List characteristics
        chars_response = variables_api.search_characteristics(page_size=50)
        if chars_response:
            chars_list = list(chars_response) if hasattr(chars_response, '__iter__') else []
            if chars_list:
                print(f"\n🔬 Characteristics ({len(chars_list)}):")
                for char in chars_list[:10]:  # Show first 10
                    name = char.name if hasattr(char, 'name') else 'Unknown'
                    uri = char.uri if hasattr(char, 'uri') else 'No URI'
                    print(f"  - {name} ({uri})")
                if len(chars_list) > 10:
                    print(f"  ... and {len(chars_list) - 10} more")
    except Exception as e:
        print(f"  Could not list characteristics: {e}")
    
    try:
        # List methods
        methods_response = variables_api.search_methods(page_size=50)
        if methods_response:
            methods_list = list(methods_response) if hasattr(methods_response, '__iter__') else []
            if methods_list:
                print(f"\n⚙️ Methods ({len(methods_list)}):")
                for method in methods_list[:10]:  # Show first 10
                    name = method.name if hasattr(method, 'name') else 'Unknown'
                    uri = method.uri if hasattr(method, 'uri') else 'No URI'
                    print(f"  - {name} ({uri})")
                if len(methods_list) > 10:
                    print(f"  ... and {len(methods_list) - 10} more")
    except Exception as e:
        print(f"  Could not list methods: {e}")
    
    try:
        # List units
        units_response = variables_api.search_units(page_size=50)
        if units_response:
            units_list = list(units_response) if hasattr(units_response, '__iter__') else []
            if units_list:
                print(f"\n📏 Units ({len(units_list)}):")
                for unit in units_list[:10]:  # Show first 10
                    name = unit.name if hasattr(unit, 'name') else 'Unknown'
                    uri = unit.uri if hasattr(unit, 'uri') else 'No URI'
                    print(f"  - {name} ({uri})")
                if len(units_list) > 10:
                    print(f"  ... and {len(units_list) - 10} more")
    except Exception as e:
        print(f"  Could not list units: {e}")

def create_basic_concepts(variables_api, existing_concepts=None):
    """Create basic demo concepts and return their URIs, reusing existing ones if available."""
    print(f"\n🛠️ Creating basic demo concepts...")
    print("-" * 60)

    if existing_concepts is None:
        existing_concepts = {
            'entities': [],
            'characteristics': [],
            'methods': [],
            'units': []
        }

    created_concepts = {
        'entities': [],
        'characteristics': [],
        'methods': [],
        'units': []
    }

    # Helper to find existing concept by name
    def find_existing_concept(concept_list, name):
        for concept in concept_list:
            if concept['name'].lower() == name.lower():
                return concept['uri']
        return None

    # Basic entities to create
    basic_entities = [
        {
            'name': 'Plant',
            'description': 'Living plant organism',
            'exact_match': []
        },
        {
            'name': 'Leaf',
            'description': 'Plant leaf structure',
            'exact_match': []
        },
        {
            'name': 'Stem',
            'description': 'Plant stem structure',
            'exact_match': []
        }
    ]

    # Basic characteristics to create
    basic_characteristics = [
        {
            'name': 'Height',
            'description': 'Vertical measurement from base to top',
            'exact_match': []
        },
        {
            'name': 'Width',
            'description': 'Horizontal measurement',
            'exact_match': []
        },
        {
            'name': 'Temperature',
            'description': 'Thermal measurement',
            'exact_match': []
        }
    ]

    # Basic methods to create
    basic_methods = [
        {
            'name': 'Manual Measurement',
            'description': 'Measurement taken manually with tools',
            'exact_match': []
        },
        {
            'name': 'Sensor Reading',
            'description': 'Automated measurement via sensors',
            'exact_match': []
        }
    ]

    # Basic units to create
    basic_units = [
        {
            'name': 'Centimeter',
            'description': 'Unit of length measurement',
            'exact_match': [],
            'symbol': 'cm'
        },
        {
            'name': 'Celsius',
            'description': 'Unit of temperature measurement',
            'exact_match': [],
            'symbol': '°C'
        }
    ]

    # Create entities
    print("\n📦 Creating entities...")
    for entity_data in basic_entities:
        existing_uri = find_existing_concept(existing_concepts.get('entities', []), entity_data['name'])
        if existing_uri:
            created_concepts['entities'].append({'name': entity_data['name'], 'uri': existing_uri})
            print(f"  ✓ Reusing existing entity: {entity_data['name']} -> {existing_uri}")
        else:
            try:
                entity = EntityCreationDTO(**entity_data)
                result = variables_api.create_entity(body=entity)
                uri = extract_uri_from_response(result)
                if uri:
                    created_concepts['entities'].append({'name': entity_data['name'], 'uri': uri})
                    print(f"  ✓ Created entity: {entity_data['name']} -> {uri}")
                else:
                    print(f"  ✗ Failed to extract URI for entity {entity_data['name']}")
            except Exception as e:
                print(f"  ✗ Failed to create entity {entity_data['name']}: {e}")

    # Create characteristics
    print("\n🔬 Creating characteristics...")
    for char_data in basic_characteristics:
        existing_uri = find_existing_concept(existing_concepts.get('characteristics', []), char_data['name'])
        if existing_uri:
            created_concepts['characteristics'].append({'name': char_data['name'], 'uri': existing_uri})
            print(f"  ✓ Reusing existing characteristic: {char_data['name']} -> {existing_uri}")
        else:
            try:
                characteristic = CharacteristicCreationDTO(**char_data)
                result = variables_api.create_characteristic(body=characteristic)
                uri = extract_uri_from_response(result)
                if uri:
                    created_concepts['characteristics'].append({'name': char_data['name'], 'uri': uri})
                    print(f"  ✓ Created characteristic: {char_data['name']} -> {uri}")
                else:
                    print(f"  ✗ Failed to extract URI for characteristic {char_data['name']}")
            except Exception as e:
                print(f"  ✗ Failed to create characteristic {char_data['name']}: {e}")

    # Create methods
    print("\n⚙️ Creating methods...")
    for method_data in basic_methods:
        existing_uri = find_existing_concept(existing_concepts.get('methods', []), method_data['name'])
        if existing_uri:
            created_concepts['methods'].append({'name': method_data['name'], 'uri': existing_uri})
            print(f"  ✓ Reusing existing method: {method_data['name']} -> {existing_uri}")
        else:
            try:
                method = MethodCreationDTO(**method_data)
                result = variables_api.create_method(body=method)
                uri = extract_uri_from_response(result)
                if uri:
                    created_concepts['methods'].append({'name': method_data['name'], 'uri': uri})
                    print(f"  ✓ Created method: {method_data['name']} -> {uri}")
                else:
                    print(f"  ✗ Failed to extract URI for method {method_data['name']}")
            except Exception as e:
                print(f"  ✗ Failed to create method {method_data['name']}: {e}")

    # Create units
    print("\n📏 Creating units...")
    for unit_data in basic_units:
        existing_uri = find_existing_concept(existing_concepts.get('units', []), unit_data['name'])
        if existing_uri:
            created_concepts['units'].append({'name': unit_data['name'], 'uri': existing_uri})
            print(f"  ✓ Reusing existing unit: {unit_data['name']} -> {existing_uri}")
        else:
            try:
                unit = UnitCreationDTO(**unit_data)
                result = variables_api.create_unit(body=unit)
                uri = extract_uri_from_response(result)
                if uri:
                    created_concepts['units'].append({'name': unit_data['name'], 'uri': uri})
                    print(f"  ✓ Created unit: {unit_data['name']} -> {uri}")
                else:
                    print(f"  ✗ Failed to extract URI for unit {unit_data['name']}")
            except Exception as e:
                print(f"  ✗ Failed to create unit {unit_data['name']}: {e}")

    # Debug: Print summary of created concepts
    print(f"\n🔍 Debug - Created concept summary:")
    print(f"   Entities: {len(created_concepts['entities'])}")
    for entity in created_concepts['entities']:
        print(f"     - {entity['name']}: {entity['uri']}")
    print(f"   Characteristics: {len(created_concepts['characteristics'])}")
    for char in created_concepts['characteristics']:
        print(f"     - {char['name']}: {char['uri']}")
    print(f"   Methods: {len(created_concepts['methods'])}")
    for method in created_concepts['methods']:
        print(f"     - {method['name']}: {method['uri']}")
    print(f"   Units: {len(created_concepts['units'])}")
    for unit in created_concepts['units']:
        print(f"     - {unit['name']}: {unit['uri']}")

    return created_concepts

def create_demo_variables(variables_api, created_concepts):
    """Create demo variables using the created concepts"""
    print(f"\n🛠️ Creating demo variables using created concepts...")
    print("-" * 60)
    
    created_variables = []
    failed_variables = []
    
    # Helper function to find concept URI by name
    def find_concept_uri(concepts_list, name_contains):
        for concept in concepts_list:
            if name_contains.lower() in concept['name'].lower():
                return concept['uri']
        return None
    
    # Validate that we have enough concepts to create variables
    if not created_concepts['entities'] or not created_concepts['characteristics'] or not created_concepts['methods'] or not created_concepts['units']:
        print("⚠️ Not enough concepts were created successfully. Cannot create variables.")
        return [], []
    
    # Define demo variables using created concepts
    demo_variables = []
    
    # Try to create Plant Height variable
    plant_uri = find_concept_uri(created_concepts['entities'], 'plant')
    height_uri = find_concept_uri(created_concepts['characteristics'], 'height')
    manual_uri = find_concept_uri(created_concepts['methods'], 'manual')
    cm_uri = find_concept_uri(created_concepts['units'], 'centimeter')
    
    if plant_uri and height_uri and manual_uri and cm_uri:
        demo_variables.append({
            'name': 'Mock Variable for Import',
            'description': 'Plant height measured manually',
            'entity': plant_uri,
            'characteristic': height_uri,
            'method': manual_uri,
            'unit': cm_uri,
            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
            'exact_match': []
        })
    
    # Try to create Leaf Width variable
    leaf_uri = find_concept_uri(created_concepts['entities'], 'leaf')
    width_uri = find_concept_uri(created_concepts['characteristics'], 'width')
    
    if leaf_uri and width_uri and manual_uri and cm_uri:
        demo_variables.append({
            'name': 'Leaf Width Manual',
            'description': 'Leaf width measured manually',
            'entity': leaf_uri,
            'characteristic': width_uri,
            'method': manual_uri,
            'unit': cm_uri,
            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
            'exact_match': []
        })
    
    # Try to create Temperature Sensor variable
    temp_uri = find_concept_uri(created_concepts['characteristics'], 'temperature')
    sensor_uri = find_concept_uri(created_concepts['methods'], 'sensor')
    celsius_uri = find_concept_uri(created_concepts['units'], 'celsius')
    
    if plant_uri and temp_uri and sensor_uri and celsius_uri:
        demo_variables.append({
            'name': 'Plant Temperature Sensor',
            'description': 'Plant temperature measured by sensor',
            'entity': plant_uri,
            'characteristic': temp_uri,
            'method': sensor_uri,
            'unit': celsius_uri,
            'datatype': 'http://www.w3.org/2001/XMLSchema#decimal',
            'exact_match': []
        })
    
    if len(demo_variables) == 0:
        print("⚠️ No variables can be created - insufficient concepts available.")
        return [], []
    
    # Create variables
    for var_data in demo_variables:
        try:
            variable = VariableCreationDTO(**var_data)
            result = variables_api.create_variable(body=variable)
            uri = extract_uri_from_response(result)
            if uri:
                created_variables.append({'name': var_data['name'], 'uri': uri})
                print(f"  ✓ Created variable: {var_data['name']} -> {uri}")
            else:
                created_variables.append({'name': var_data['name'], 'uri': 'URI extraction failed'})
                print(f"  ✓ Created variable: {var_data['name']} (but URI extraction failed)")
        except Exception as e:
            failed_variables.append({'name': var_data['name'], 'error': str(e)})
            print(f"  ✗ Failed to create variable {var_data['name']}: {e}")
    
    return created_variables, failed_variables

def main():
    """Main function to orchestrate the demo setup"""
    print("OpenSilex Smart Demo Variables Creator - SSH Config Only")
    print("=" * 60)
    
    # Select host from SSH config
    host_name = select_opensilex_host_interactively()
    
    # Construct OpenSilex API URL
    api_url = get_opensilex_base_url(host_name)
    
    # Get credentials
    identifier = "admin@opensilex.org"
    password = "admin"
    
    print(f"\n🚀 Connecting to OpenSilex...")
    print(f"Host: {host_name}")
    print(f"API URL: {api_url}")
    print(f"User: {identifier}")
    
    # Connect to OpenSilex
    client = connect_to_opensilex(api_url, identifier, password)
    if not client:
        sys.exit(1)
    
    # Create API instance
    variables_api = opensilexClientToolsPython.VariablesApi(client)
    
    # Get existing concepts
    print("\n🔍 Checking for existing concepts...")
    existing_concepts = get_existing_concepts(variables_api)

    # Create basic concepts (reusing existing ones if found)
    created_concepts = create_basic_concepts(variables_api, existing_concepts)
    
    # Create demo variables
    created_vars, failed_vars = create_demo_variables(variables_api, created_concepts)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"✓ Successfully created {len(created_vars)} variables")
    
    if created_vars:
        print("\nCreated variables:")
        for var in created_vars:
            print(f"  - {var['name']}")
    
    if failed_vars:
        print(f"\n✗ Failed to create {len(failed_vars)} variables")
        print("\nFailed variables:")
        for var in failed_vars:
            print(f"  - {var['name']}: {var['error']}")
    
    print("\n✨ Demo setup complete!")
    print(f"\nConnected to: {host_name} ({api_url})")
    print("\nYou can now:")
    print("  1. View these variables in the OpenSilex web interface")
    print("  2. Use them to create data entries")
    print("  3. Create additional variables using the web interface or API")

if __name__ == "__main__":
    main()