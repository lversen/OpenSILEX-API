#!/usr/bin/env python3
"""
OpenSilex Configuration Helper
Helps set up and test OpenSilex client configuration
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict

try:
    from opensilex_client import OpenSilexClient, SSHConfigParser
except ImportError:
    print("Error: opensilex_client.py not found in current directory")
    sys.exit(1)


class OpenSilexConfigHelper:
    """Helper class for OpenSilex configuration setup and testing."""
    
    def __init__(self):
        self.config_file = Path.home() / ".opensilex" / "config.json"
        self.config_file.parent.mkdir(exist_ok=True)
    
    def save_config(self, config: Dict) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Configuration saved to {self.config_file}")
    
    def load_config(self) -> Optional[Dict]:
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return None
    
    def interactive_setup(self) -> Dict:
        """Interactive setup wizard."""
        print("\n=== OpenSilex Configuration Setup ===\n")
        
        config = {}
        
        # Method selection
        print("How do you want to connect to OpenSilex?")
        print("1. Use SSH config (recommended for VMs)")
        print("2. Direct URL")
        print("3. Use public sandbox")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            # SSH config method
            ssh_config = SSHConfigParser.parse_ssh_config()
            
            if ssh_config:
                print("\nFound SSH hosts:")
                hosts = list(ssh_config.keys())
                for i, host in enumerate(hosts, 1):
                    print(f"{i}. {host}")
                
                host_choice = input("\nSelect host number or enter custom name: ").strip()
                
                if host_choice.isdigit() and 1 <= int(host_choice) <= len(hosts):
                    config['ssh_host'] = hosts[int(host_choice) - 1]
                else:
                    config['ssh_host'] = host_choice
            else:
                config['ssh_host'] = input("Enter SSH host name: ").strip()
            
            config['use_ssh_config'] = True
            
        elif choice == "2":
            # Direct URL
            default_url = "http://localhost:28081/app/rest"
            url = input(f"Enter OpenSilex URL [{default_url}]: ").strip()
            config['base_url'] = url or default_url
            config['use_ssh_config'] = False
            
        else:
            # Public sandbox
            config['base_url'] = "http://opensilex.org/sandbox/rest"
            config['use_ssh_config'] = False
        
        # Credentials
        print("\n=== Authentication ===")
        
        if choice == "3":
            # Sandbox defaults
            config['username'] = "guest@opensilex.org"
            config['password'] = "guest"
            print("Using sandbox credentials (guest/guest)")
        else:
            default_user = "admin@opensilex.org"
            username = input(f"Username [{default_user}]: ").strip()
            config['username'] = username or default_user
            
            import getpass
            config['password'] = getpass.getpass("Password: ")
        
        # Save option
        save = input("\nSave configuration? (y/n): ").strip().lower()
        if save == 'y':
            self.save_config(config)
        
        return config
    
    def test_connection(self, config: Dict = None) -> bool:
        """Test connection with given or saved configuration."""
        if config is None:
            config = self.load_config()
            if config is None:
                print("No saved configuration found. Run setup first.")
                return False
        
        print("\n=== Testing Connection ===")
        
        # Create client based on config
        if config.get('use_ssh_config'):
            client = OpenSilexClient(
                ssh_host=config.get('ssh_host'),
                username=config['username'],
                password=config['password']
            )
        else:
            client = OpenSilexClient(
                base_url=config['base_url'],
                username=config['username'],
                password=config['password'],
                use_ssh_config=False
            )
        
        print(f"Connecting to: {client.base_url}")
        
        # Test authentication
        if client.authenticate():
            print("✓ Authentication successful!")
            
            # Try to get some data
            try:
                experiments = client.get_experiments(page_size=1)
                print(f"✓ API access confirmed - found {len(experiments)} experiment(s)")
                
                if experiments:
                    print(f"  First experiment: {experiments[0].get('name', 'Unknown')}")
                
                return True
            except Exception as e:
                print(f"✗ API error: {str(e)}")
                return False
        else:
            print("✗ Authentication failed!")
            return False
    
    def show_ssh_config_template(self):
        """Show SSH config template."""
        template = """
# Add this to your ~/.ssh/config file:

Host opensilex-vm
    HostName YOUR_VM_IP_HERE  # e.g., 192.168.1.100
    User YOUR_SSH_USER        # e.g., ubuntu
    Port 22
    IdentityFile ~/.ssh/id_rsa

# You can also use an alias:
Host opensilex
    HostName YOUR_VM_IP_HERE
    User YOUR_SSH_USER
    Port 22
"""
        print(template)
    
    def create_client_from_config(self) -> Optional[OpenSilexClient]:
        """Create a client instance from saved configuration."""
        config = self.load_config()
        if config is None:
            print("No saved configuration found. Run setup first.")
            return None
        
        if config.get('use_ssh_config'):
            return OpenSilexClient(
                ssh_host=config.get('ssh_host'),
                username=config['username'],
                password=config['password']
            )
        else:
            return OpenSilexClient(
                base_url=config['base_url'],
                username=config['username'],
                password=config['password'],
                use_ssh_config=False
            )


def main():
    """Main CLI interface."""
    helper = OpenSilexConfigHelper()
    
    print("OpenSilex Configuration Helper")
    print("==============================\n")
    
    while True:
        print("\nOptions:")
        print("1. Setup configuration")
        print("2. Test connection")
        print("3. Show SSH config template")
        print("4. View current configuration")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            config = helper.interactive_setup()
            helper.test_connection(config)
            
        elif choice == "2":
            helper.test_connection()
            
        elif choice == "3":
            helper.show_ssh_config_template()
            
        elif choice == "4":
            config = helper.load_config()
            if config:
                print("\nCurrent configuration:")
                # Hide password when displaying
                display_config = config.copy()
                if 'password' in display_config:
                    display_config['password'] = '***'
                print(json.dumps(display_config, indent=2))
            else:
                print("No saved configuration found.")
                
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()