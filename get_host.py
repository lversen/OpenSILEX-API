import os
import re

class SSHConfigParser:
    def __init__(self, config_file='~/.ssh/config'):
        self.config_file = os.path.expanduser(config_file)
        self.hosts = {}
        self._parse()

    def _parse(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                host_entry = None
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    if line.lower().startswith('host '):
                        host_entry = line.split()[1]
                        self.hosts[host_entry] = {}
                    elif host_entry:
                        key, value = re.split(r'\s+', line, 1)
                        self.hosts[host_entry][key.lower()] = value
        except UnicodeDecodeError as e:
            print(f"Warning: Could not decode {self.config_file} with UTF-8 encoding: {e}")
            # Fallback to default encoding
            try:
                with open(self.config_file, 'r') as f:
                    host_entry = None
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue

                        if line.lower().startswith('host '):
                            host_entry = line.split()[1]
                            self.hosts[host_entry] = {}
                        elif host_entry:
                            key, value = re.split(r'\s+', line, 1)
                            self.hosts[host_entry][key.lower()] = value
            except Exception as e:
                print(f"Error parsing SSH config file: {e}")

    def get_all_hosts(self):
        return self.hosts

    def get_host(self, name):
        return self.hosts.get(name)

    def select_host_ip(self):
        host_names = list(self.hosts.keys())
        if not host_names:
            print("No SSH hosts found in your config file.")
            return None

        print("Available SSH Hosts:")
        for i, name in enumerate(host_names):
            print(f"{i + 1}. {name}")

        while True:
            try:
                choice = int(input("Select a host by number: ")) - 1
                if 0 <= choice < len(host_names):
                    selected_host_name = host_names[choice]
                    selected_host = self.hosts[selected_host_name]
                    hostname = selected_host.get('hostname')
                    if hostname:
                        print(f"Selected host: {selected_host_name} (IP: {hostname})")
                        return hostname
                    else:
                        print(f"Host '{selected_host_name}' does not have a 'Hostname' defined.")
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
