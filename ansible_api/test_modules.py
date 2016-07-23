#!/usr/bin/python 
import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import json

# the fastest way to set up the inventory

# hosts list
# hosts = ["localhost"]
# set up the inventory, if no group is defined then 'all' group is used by default
#example_inventory = ansible.inventory.Inventory(hosts)

host_list = "/root/ops/ansible_api/hosts.py"

pm = ansible.runner.Runner(
    host_list = host_list,
    module_name = 'command',
    module_args = 'uname -a',
    timeout = 5,
    subset = 'codis' # name of the hosts group 
    #inventory = example_inventory,
    )

out = pm.run()

print json.dumps(out, sort_keys=True, indent=4, separators=(',', ': '))
