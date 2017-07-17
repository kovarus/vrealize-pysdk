#!/usr/bin/env python

"""

    Useful tool for collecting the API URLs with JSON templates to assist in API integration


"""

import argparse
import getpass
import json
import vralib

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
    parser.add_argument('-i', '--id',
                        required=True,
                        action='store',
                        help='The partial or full name of the catalog item you want API information for')
    args = parser.parse_args()
    return args

def main():
    args = getargs()
    cloudurl = args.server
    username = args.username
    tenant = args.tenant
    catalog_id = args.id

    if not username:
        username = input("vRA Username: ")

    password = getpass.getpass("vRA Password:")

    vra = vralib.Session.login(username=username, password=password, cloudurl=cloudurl,tenant=tenant, ssl_verify=False)

    catalog_item = vra.get_catalogitem_byid(catalog_id)

    catalog_name = (catalog_item["content"][0]["catalogItem"]["name"])

    print(f"Catalog Item Name: {catalog_name}")
    print(f"Catalog Item ID: {catalog_id}")

    print(f"Request Template is at the following URL: https://{vra.cloudurl}/catalog-service/api/consumer/entitledCatalogItems/{catalog_id}/requests/template ")
    request_template = vra.get_request_template(catalogitem=catalog_id)
    print(json.dumps(request_template, indent=4))
    print(f"POST Template to the following URL: https://{vra.cloudurl}/catalog-service/api/consumer/entitledCatalogItems/{catalog_id}/requests")

if __name__ == '__main__':
    main()