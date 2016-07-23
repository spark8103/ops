#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, json
import json, time, threading, argparse

proj_path = "/root/ops"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ops.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from cmdb.models import *


def lists():
    r = {}
    hostvars = {}
    for item in SERVICE_TYPES:
        service_type = item[0]
        host_list = Host.objects.filter(service_type=service_type)
        h = [ host.name for host in host_list ]
        hosts = {'hosts': h, 'vars': {"ansible_ssh_user": "root", "ansible_ssh_private_key_file": "/root/.ssh/id_rsa"}}
        for host in host_list:
           hostvars[host.name] = {"ansible_ssh_host": host.mip}
        r[service_type] = hosts
    r['_meta'] = {'hostvars': hostvars}
    return json.dumps(r, indent=4)

def hosts(name):

    #host = Host.objects.get(name=name)
    #r = {'ansible_ssh_host': host.mip}
    #inventory = dict(r.items())

    inventory = {'_meta': {'hostvars': {}}}
    return json.dumps(inventory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='hosts list', action='store_true')
    parser.add_argument('-H', '--host', help='hosts vars')
    args = vars(parser.parse_args())


    if args['list']:
        print lists()
    elif args['host']:
        print hosts(args['host'])
    else:
        parser.print_help()
