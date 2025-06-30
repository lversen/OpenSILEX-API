#!/usr/bin/env python3
"""
Example for connecting to phis-prod using SSH config
"""

from opensilex_client import OpenSilexClient
import logging

# Enable logging to see connection details
logging.basicConfig(level=logging.INFO)

print("=== Connecting to phis-prod ===\n")

# Method 1: Specify your SSH host directly
print("Method 1: Using SSH host 'phis-prod'")
client = OpenSilexClient.from_ssh_config(ssh_host="phis-prod")
print(f"Base URL: {client.base_url}")
print(f"Expected: http://20.4.208.154:28081/app/rest\n")

# Method 2: Direct connection with IP
print("Method 2: Direct connection")
client2 = OpenSilexClient(
    base_url="http://20.4.208.154:28081/app/rest",
    use_ssh_config=False
)
print(f"Base URL: {client2.base_url}\n")

# Test connection
print("Testing authentication...")
if client.authenticate():
    print("✓ Authentication successful!")
    
    # Get some basic info
    experiments = client.get_experiments(page_size=5)
    print(f"\nFound {len(experiments)} experiments:")
    for exp in experiments:
        print(f"  - {exp.get('name', 'Unknown')}")
else:
    print("✗ Authentication failed!")
    print("\nPossible issues:")
    print("1. Check if the VM is running and accessible")
    print("2. Verify the port (28081) is correct")
    print("3. Check your credentials (default: guest@opensilex.org / guest)")
    print("4. The path might be different (e.g., /rest instead of /app/rest)")

# Debug SSH config parsing
print("\n=== SSH Config Debug ===")
from opensilex_client import SSHConfigParser

config = SSHConfigParser.parse_ssh_config()
print(f"Found {len(config)} hosts in SSH config:")
for host, details in config.items():
    print(f"\nHost: {host}")
    for key, value in details.items():
        print(f"  {key}: {value}")