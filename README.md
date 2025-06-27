# SSH Config Setup for OpenSilex

## Overview

The OpenSilex Python client can automatically detect your VM's IP address from your SSH configuration. This is useful when working with development VMs where the IP address might change.

## SSH Config Setup

### 1. Edit your SSH config file

Open your SSH config file (usually located at `~/.ssh/config`):

```bash
nano ~/.ssh/config
```

### 2. Add your OpenSilex VM configuration

Add an entry for your OpenSilex VM:

```
Host opensilex-vm
    HostName 192.168.1.100  # Replace with your VM's IP
    User your-username
    Port 22
    IdentityFile ~/.ssh/id_rsa

# Alternative names (the client will check these too)
Host opensilex
    HostName 192.168.1.100
    User your-username
    Port 22
```

### 3. Test SSH connection

```bash
ssh opensilex-vm
```

## Using with Python Client

### Method 1: Automatic Detection

The client will automatically check for common host names in your SSH config:

```python
from opensilex_client import OpenSilexClient

# Automatically detects from SSH config
# Checks for: 'opensilex', 'opensilex-vm', 'opensilex-dev', 'vm'
client = OpenSilexClient()
```

### Method 2: Specify SSH Host

```python
# Use specific SSH host from config
client = OpenSilexClient.from_ssh_config(ssh_host="opensilex-vm")
```

### Method 3: Custom Configuration

```python
# Mix SSH config with custom credentials
client = OpenSilexClient(
    ssh_host="my-custom-vm",
    username="admin@opensilex.org",
    password="admin123"
)
```

### Method 4: Override with Manual URL

```python
# Bypass SSH config entirely
client = OpenSilexClient(
    base_url="http://192.168.1.100:28081/app/rest",
    use_ssh_config=False
)
```

## URL Format

The client constructs the URL as:
```
http://{vm_ip}:28081/app/rest
```

Where:
- `{vm_ip}` is extracted from SSH config
- Port `28081` is the default OpenSilex port
- `/app/rest` is the API endpoint path

## Troubleshooting

### Check if SSH config is being read:

```python
from opensilex_client import SSHConfigParser

# Parse SSH config
config = SSHConfigParser.parse_ssh_config()
print("Available hosts:", list(config.keys()))

# Get specific host IP
ip = SSHConfigParser.get_host_ip("opensilex-vm")
print(f"OpenSilex VM IP: {ip}")
```

### Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

client = OpenSilexClient()
# Will show detailed logs about SSH config parsing
```

### Common Issues:

1. **SSH config not found**: Make sure `~/.ssh/config` exists
2. **Host not found**: Check that your host name matches exactly
3. **Wrong port**: The client assumes port 28081 - modify if different
4. **Path mismatch**: The client uses `/app/rest` - adjust if your setup differs

## Example: Complete Setup

```python
#!/usr/bin/env python3
"""
Example of using OpenSilex client with SSH config
"""

from opensilex_client import OpenSilexClient
import logging

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)

# Try automatic detection first
print("Attempting automatic detection from SSH config...")
client = OpenSilexClient()

if client.authenticate():
    print(f"✓ Connected to: {client.base_url}")
    
    # Get some data
    experiments = client.get_experiments(page_size=5)
    print(f"✓ Found {len(experiments)} experiments")
else:
    print("✗ Authentication failed")
    print("Check your VM is running and credentials are correct")
```

## Benefits

1. **Dynamic IP handling**: No need to hardcode IPs in your scripts
2. **Environment consistency**: Same SSH config works for both SSH and API access
3. **Easy switching**: Change VMs by just updating SSH config
4. **Team collaboration**: Share scripts without hardcoded IPs