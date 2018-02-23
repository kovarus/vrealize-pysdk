#!/usr/bin/env python

"""

    Retrieves vRealize provisioned items that match the value passed into '-n'

"""

# TODO set an environment variable that stores the auth token
# TODO create a check for auth token env variable. If present don't prompt for password

__version__ = "$Revision$"
# $Source$

import getpass
import argparse
import vralib
from prettytable import PrettyTable


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
    parser.add_argument('-n', '--name',
                        required=False,
                        action='store',
                        help='The partial or full name of the catalog item you want the ID for')
    args = parser.parse_args()
    return args

def main():

    args = getargs()
    cloudurl = args.server
    username = args.username
    tenant = args.tenant
    name = args.name

    if not username:
        username = input("vRA Username (user@domain):")

    password = getpass.getpass("vRA Password:")

    vra = vralib.Session.login(username, password, cloudurl, tenant, ssl_verify=False)

    items = vra.get_consumer_resources()

    out = PrettyTable(['Name', 'ID'])
    out.align['Name'] = 'l'
    out.padding_width = 1
    # TODO VMware doesn't appear to use the same format for data it gets back from the API
    # TODO will need to check for this and deal with it somehow.
    # TODO I think I need to determine what the item is first then based on that find the label
    for i in items['content']:

        out.add_row((i['name'], i['id']))
        # print i['id']
        # print i['parentResourceRef']
        #
    print(out)

if __name__ == '__main__':
    main()