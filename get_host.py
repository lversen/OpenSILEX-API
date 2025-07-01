import os
import re

class SSHConfigParser:
    def __init__(self, config_file='~/.ssh/config'):
        self.config_file = os.path.expanduser(config_file)
        self.hosts = {}
        self._parse()

    def _parse(self):
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

    def get_all_hosts(self):
        return self.hosts

    def get_host(self, name):
        return self.hosts.get(name)
