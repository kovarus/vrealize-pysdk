#!/usr/bin/env python

"""

    vRA Request Tool. A tool I use to build VMs for the purposes of running some tests. 

"""

__version__ = "$Revision"

import getpass
import argparse
import vralib
import json
import time

def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',
                        required=True,
                        action='store',
                        help='FQDN of the Cloud Provider.')
    parser.add_argument('-u', '--username',
                        required=False,
                        action='store',
                        help='Username to access the cloud provider')
    parser.add_argument('-t', '--tenant',
                        required=True,
                        action='store',
                        help='vRealize tenant')
    parser.add_argument('-c', '--catalogitem',
                        required=True,
                        action='store',
                        help='The partial or full name of the catalog item you want the ID for')
    parser.add_argument('-r', '--reasons',
                        required=True,
                        action='store',
                        help='The reason for the requested item. Enclose in quotes.')
    parser.add_argument('-d', '--description',
                        required=False,
                        action='store',
                        help='An optional description for the requested resource. Enclose in quotes.')
    args = parser.parse_args()
    return args

def main():
    args = getargs()
    cloudurl = args.server
    username = args.username
    tenant = args.tenant
    if not username:
        username = raw_input("vRA Username (user@domain):")

    password = getpass.getpass("vRA Password:")
    vra = vralib.Session.login(username, password, cloudurl,
                               tenant, ssl_verify=False)

    request_template = vra.get_request_template(catalogitem=args.catalogitem)

    request_template['description'] = args.description
    request_template['reasons'] = args.reasons

    # TODO add some logic to query for options here.
    # TODO should be noted that this only changes one custom property. Need to design some logic to extend this
    # request_template['data']['Linux_vSphere_VM']['data']['Puppet.RoleClass'] = "role::linux_mysql_database"

    build_vm = vra.request_item(catalogitem=args.catalogitem,
                                payload=request_template)

    request_id = build_vm['id']
    provisioned_state = vra.get_requests(id=request_id)

    while 'SUCCESSFUL' not in provisioned_state['state']:
        provisioned_state = vra.get_requests(id=request_id)
        print('Current provisioning state is:', provisioned_state['stateName'],
              'Current phase is:', provisioned_state['phase'])
        if provisioned_state['state'] == 'PROVIDER_FAILED':
            raise Exception('Request provider failed! Dumping JSON output of request',
                            json.dumps(provisioned_state, indent=4))
        if provisioned_state['state'] == 'FAILED':
            raise Exception('Failed inside of vRA! Dumping JSON output of request',
                            json.dumps(provisioned_state, indent=4))
        time.sleep(5)

    print "#" * 80
    print json.dumps(provisioned_state)

if __name__ == '__main__':
    main()
