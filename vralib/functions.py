'''

    A collection of functions to help manage vRealize automation. Depends on the Session() class pretty heavily.

'''
# TODO update docstrings with usage examples
#
#   EVERYTHING IN HERE IS LEGACY AND SHOULD NOT BE USED. ONLY KEEPING AROUND AS FRAME OF REFERENCE
#

import json
import requests
from collections import defaultdict

def get_subtenant_byname(token, cloudurl, tenant, subtenant_name):
    # Probably want this to be a @classmethod for a future Subtenant class
    pass

def get_subtenant_roles(vra_session, subtenant):

    # https://hq-l-lvcac1.kpsc.lan/identity/api/tenants/kpsc/subtenants/06F2C908-792D-41CC-A188-61BDDCC90EB9/roles

    cloudurl = vra_session.cloudurl
    tenant = vra_session.tenant
    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    r = requests.get(
        verify= ssl_verify,
        url='https://' + cloudurl + '/identity/api/tenants/' + tenant + '/subtenants/' + subtenant + '/roles',
        headers={'Authorization': token,
                 'Content-type': 'application/json',
                 'Accept': 'text/plain'}
    )

    roles = json.loads(r.content)
    return roles

def get_tenant_principals(vra_session):
    """

    Collect all users available in vRealize Automation.
    :param token:
    :param cloudurl:
    :param tenant:
    :return:

    """
    cloudurl = vra_session.cloudurl
    tenant = vra_session.tenant
    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    r = requests.get(
        verify=ssl_verify,
        url='https://' + cloudurl + '/identity/api/tenants/' + tenant + '/principals?limit=9999',
        headers={'Authorization': token,
                 'Content-type': 'application/json',
                 'Accept': 'text/plain'}
    )

    principals = json.loads(r.content)
    return principals

def get_business_group_members(token, cloudurl, tenant):
    # https://hq-l-lvcac1.kpsc.lan/identity/api/tenants/kpsc/subtenants/06F2C908-792D-41CC-A188-61BDDCC90EB9/roles
    pass


def get_consumed_resources(vra_session):
    # https://hq-l-lvcac1.kpsc.lan/catalog-service/api/consumer/resources

    cloudurl = vra_session.cloudurl
    tenant = vra_session.tenant
    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    r = requests.get(
        verify=ssl_verify,
        url='https://' + cloudurl + '/catalog-service/api/consumer/resources?limit=9999',
        headers={'Authorization': token,
                 'Content-type': 'application/json',
                 'Accept': 'text/plain'}
    )

    consumed_resources = json.loads(r.content)
    return consumed_resources

def build_vm(vra_session, inputs):
    """
    :rtype : object
    :param buildvminputs:
    :return:


    """
    cloudurl = vra_session.cloudurl
    tenant = vra_session.tenant
    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    try:
        r = requests.post(
            verify=ssl_verify,
            url="https://" + cloudurl + "/catalog-service/api/consumer/requests",
            headers={'Authorization': token,
                     'Content-type': 'application/json',
                     'Accept': 'text/plain'},
            data=json.dumps(inputs))

        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        print('Response HTTP Response Body : {content}'.format(content=r.content))
        print('Virtual Machine queued for build')
        return r.headers['location']
    except requests.RequestException as e:
        print('HTTP Request failed')
        print(e)

def get_request(vra_session, requesturl):
    '''
    Feed this the location from build_vm()

    :param vra_session:
    :param requesturl:
    :return:
    '''

    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    r = requests.get(
        verify=ssl_verify,
        url=requesturl,
        headers={'Authorization': token,
                 'Content-type': 'application/json',
                 'Accept': 'application/json'}
    )
    output = json.loads(r.content)
    return output['id']


def get_resource_detail(vra_session, resourceid):
    '''

    :param vra_session:
    :param resourceid:
    :return:
    '''
    cloudurl = vra_session.cloudurl
    tenant = vra_session.tenant
    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    r = requests.get(
        verify=ssl_verify,
        url="https://" + cloudurl +  "/catalog-service/api/consumer/resources/" + resourceid,
        headers={'Authorization': token,
                 'Content-type': 'application/json',
                 'Accept': 'application/json'}
    )
    output = json.loads(r.content)
    return output

def get_request_detail(vra_session, request_id):
    '''
    Feed this the ID from get_request()
    :param vra_session:
    :param requestid:
    :return:
    '''
    cloudurl = vra_session.cloudurl
    tenant = vra_session.tenant
    token = vra_session.token
    ssl_verify = vra_session.ssl_verify

    testurl = "https://" + cloudurl +  "/catalog-service/api/consumer/resources/?$filter=request/id+eq+%27" + request_id + '%27'

    r = requests.get(
        verify=ssl_verify,
        url="https://" + cloudurl +  "/catalog-service/api/consumer/resources/?$filter=request/id+eq+%27" + request_id + '%27',
        headers={'Authorization': token,
                 'Accept': 'application/json'}
    )

    print request_id
    print ' '
    print testurl

    output = json.loads(r.content)

    print output

    # return output['content']['id']
    # for i in output['content']:
    #     resource_id['resource'] = i['id']
    #
    # return resource_id


# TODO Create generic put/delete functions

# def api_get(vra_session, url, **kwargs):
#     '''
#
#     Generic REST API GET function.
#
#     :param vra_session: session object that includes logged in user, tenant and cloud management platform.
#     :param url: actual API URL to make an HTTP GET to
#     :param kwargs: Placeholder for any addtional arguments that may be required (verbs, etc.)
#     :return: python dictionary of whatever the response is
#     '''
#
#     headers = {'Accept': 'application/json',
#                'Content-type': 'application/json',
#                'Authorization': vra_session.token}
#
#     r = requests.get(url = url,
#                      headers = headers,
#                      verify = vra_session.ssl_verify)
#
#     return json.loads(r.content)

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

# def get_entitledcatalogitems(vra_session):
#     '''
#
#     Retrieves a dictionary of all the currently available catalog items for the logged in user/tenant.
#     This can result in multi-page output so I've added some basic pagination here.
#
#     :param vra_session: session object that includes logged in user, tenant and cloud management platform
#     :return: Python dictionary with the JSON response contents from all pages in result['metadata']['totalPages']
#     '''
#     # TODO update the output dict's page number to reflect a list of page numbers iterated through
#
#     url = 'https://' + vra_session.cloudurl + '/catalog-service/api/consumer/entitledCatalogItems'
#
#     result = api_get(vra_session, url)
#
#     if result['metadata']['totalPages'] != 1:
#         page = 2 # starting on 2 since we've already got page 1's data
#         while page <= result['metadata']['totalPages']:
#             url = 'https://' + vra_session.cloudurl + '/catalog-service/api/consumer/entitledCatalogItems?page=%s' % page
#             next_page = api_get(vra_session, url)
#             for i in next_page['content']:
#                 result['content'].append(i)
#             page += 1
#
#         return result
#
#     return result

# def get_catalogitem_byname(vra_session, name, catalog=False):
#     '''
#
#     Loop through catalog items until you find the one with the specified name
#
#
#     :param vra_session:
#     :param name:
#     :return: Returns a list of dictionaries that contain the catalog item and ID
#     '''
#     # look for catalogdict['content']['catalogItem']['name']; need to work with catalogdict['content']['catalogItem']['id']
#     # TODO determine what other data may be desired in the return output
#
#     if not catalog:
#         catalog = get_entitledcatalogitems(vra_session)
#
#     result = []
#     for i in catalog['content']:
#         target = i['catalogItem']['name']
#         if name.lower() in target.lower():
#             element = {'name': i['catalogItem']['name'], 'id': i['catalogItem']['id']}
#             result.append(element)
#
#     return result


def get_catalogitem_template(vra_session, catalogitem):
    '''

    https://jupiter.kpsc.lan/catalog-service/api/consumer/entitledCatalogItems/15dc50f9-3d3b-4c49-bb84-26b285cac522/requests/template

    :param vra_session:
    :param catalogitem:
    :return:
    '''

    url = 'https://' + vra_session.cloudurl + '/catalog-service/api/consumer/entitledCatalogItems/' + catalogitem + '/requests/template'
    return api_get(vra_session, url)

def get_eventbroker_events(vra_session):
    '''
    pick a page
    https://jupiter.kpsc.lan/event-broker-service/api/events?page=210

    put newest events first in the response
    https://jupiter.kpsc.lan/event-broker-service/api/events?$orderby=timeStamp desc

    API Docs here:
    vrealize-automation-70-rest-api-docs%20/docs/event-broker-server-war/api/docs/resource_Consumer%20APIs.html

    Some examples of stuff to work with:
      "metadata": {
        "size": 20,
        "totalElements": 4193,
        "totalPages": 210,
        "number": 210,
        "offset": 4180
      }
    ?page=1

    :param vra_session:
    :return:
    '''
    # TODO create a handler for the different API verbs this thing needs to support

    url = 'https' + vra_session.cloudurl + '/event-broker-service/api/events'
    return api_get(vra_session, url)

def get_business_groups(vra_session):
    '''

    Will retrieve a list of all vRA business groups for the currently logged in tenant

    :param vra_session: session object that includes logged in user, tenant and cloud management platform
    :return: python dictionary with the JSON response contents.
    '''

    tenant = vra_session.tenant
    url = 'https://' + vra_session.cloudurl + '/identity/api/tenants/' + tenant + '/subtenants'
    return api_get(vra_session, url)

# def api_post(vra_session, url, payload):
#     '''
#
#     Generic REST API POST function
#
#     :param vra_session: session object that includes logged in user, tenant and cloud management platform.
#     :param url: actual API URL to make an HTTP POST to
#     :param payload: Input JSON
#     :return: Content of the API response in a python dictionary
#     '''
#     # TODO add checking to ensure if dictionary is passed in that we convert it to JSON before trying to POST it
#
#     if type(payload) == dict:
#         payload = json.dumps(payload)
#
#     headers = {'Accept': 'application/json',
#                'Content-type': 'application/json',
#                'Authorization': vra_session.token}
#
#     r = requests.post(url = url,
#                       headers = headers,
#                       verify = vra_session.ssl_verify,
#                       data = payload)
#
#     return json.loads(r.content)

