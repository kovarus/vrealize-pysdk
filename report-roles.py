#!/usr/bin/env python

"""

    Pulls a report of all the users and assigned roles in a given tenant.

"""

# TODO Allow for specification of output file
# TODO support dynamic subtenant by name or ID
# TODO output data to prettytable

__version__ = "$Revision$"
# $Source$

import getpass
import argparse
import vralib
import csv


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server',
                        required=True,
                        action='store',
                        help='FQDN of vRealize Automation.')
    parser.add_argument('-u', '--username',
                        required=False,
                        action='store',
                        help='Username to access the cloud provider')
    parser.add_argument('-t', '--tenant',
                        required=True,
                        action='store',
                        help='vRealize tenant')
    parser.add_argument('-c', '--csv',
                        required=True,
                        action='store',
                        help='Filename to output CSV report to.')
    parser.add_argument('-b', '--businessgroup',
                        required=False,
                        action='store',
                        help='Business group to retrieve roles from')
    args = parser.parse_args()
    return args

def main():

    args = getargs()
    cloudurl = args.server
    username = args.username
    tenant = args.tenant
    outfile = args.csv


    if not username:
        username = raw_input("vRA Username (user@domain):")
    else:
        pass

    password = getpass.getpass("vRA Password:")

    vra = vralib.Session.login(username, password, cloudurl, tenant, ssl_verify=False)

    subtenant = 'f41a35f5-040e-42e0-a5c2-6ca4e7bf328b'
    subtenantroles = vra.get_subtenant_roles(token, cloudurl, tenant, subtenant)

    with open(outfile, "w") as f:
        csv_file = csv.writer(f)
        csv_file.writerow(['user', 'domain', 'type', 'id', 'role', 'scope'])
        for i,val in enumerate(subtenantroles['content']):
            if val['name'] == 'Basic User':
                scoperole = val['scopeRoleRef']
                attype = val['@type']
                role_name = val['name']
                role_id = val['id']
                for user in val['principalId']:
                    csv_file.writerow([user['name'],
                                       user['domain'],
                                       attype,
                                       role_id,
                                       role_name,
                                       scoperole])
            elif val['name'] == 'Business Group Manager':
                scoperole = val['scopeRoleRef']
                attype = val['@type']
                role_name = val['name']
                role_id = val['id']
                for user in val['principalId']:
                    csv_file.writerow([user['name'],
                                       user['domain'],
                                       attype,
                                       role_id,
                                       role_name,
                                       scoperole])
            elif val['name'] == 'Support User':
                scoperole = val['scopeRoleRef']
                attype = val['@type']
                role_name = val['name']
                role_id = val['id']
                for user in val['principalId']:
                    csv_file.writerow([user['name'],
                                       user['domain'],
                                       attype,
                                       role_id,
                                       role_name,
                                       scoperole])



if __name__ == '__main__':
    main()


