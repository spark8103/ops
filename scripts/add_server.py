#!/root/ops/venv/bin/python
# -*- coding: utf-8 -*-
#
#hostname,idc_name,mip,service_type,

import os, sys, csv
import json, time, threading, argparse

proj_path = "/root/ops"
import_list = "/root/ops/data/qa_server.txt"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ops.settings")
sys.path.append(proj_path)

os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from cmdb.models import *
def host_add(name, idc, mip, service_type):
    Host.objects.create(name=name, idc=IDC.objects.get(name=idc), mip=mip, service_type=service_type)


def main():
    if os.path.exists(import_list):
        with open(import_list) as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            for row in f_csv:
                if row[0].find('#') == -1:
                    #print row[0], row[1], row[2], row[3]
                    print "add host: ", row[0]
                    host_add(row[0], row[1], row[2], row[3])
    else:
        print "file: " + import_list + " is not exist!"

if __name__ == "__main__":
    main()

#############################################################################################################
#host_list = [ host.name for host in Host.objects.all() ]
#idc = IDC.objects.all()
#
#idc = IDC.objects.filter(name="SHW1")[0]
#idc = IDC.objects.filter(name="SLB1")[0]
#ss = Host.objects.create(idc=idc, name="bb", service_type="ngin") 
#
#ss = Host(idc=idc[0], name="aa", service_type="nginx" )
#ss.save()
