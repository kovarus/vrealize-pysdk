"""

    Python module for interfacing with the vRealize API
    Primarily used for reporting initially.

    This thing is kind of a mess so tread carefully while I piece it back together.

"""
# TODO implement logging


__author__ = 'Russell Pope'

class Deployment(object):
    """
    Manage existing deployments

    probably want to create instances of child classes with individual virtual machines/items that are a part of this deployment

    http://stackoverflow.com/questions/26033726/parent-methods-which-return-child-class-instances



    """

    # def __init__(self, session, resource_id, description, name, request_id, business_group_id, date_created, owners, tenant_id,
    #              costs, costs_to_date, total_cost, lease=None):
    def __init__(self, session, deployment, operations):
        self.session = session
        self.resource_id = deployment["id"]
        self.description = deployment["description"]
        self.name = deployment["name"]
        self.request_id = deployment["requestId"]
        self.business_group_id = deployment["organization"]["subtenantRef"]
        self.business_group_label = deployment["organization"]["subtenantLabel"]
        self.date_created = deployment["dateCreated"]
        self.owners = deployment["owners"]
        self.tenant_id = deployment["organization"]["tenantRef"]

        # self.costs = costs
        # self.costs_to_date = costs_to_date
        # self.total_cost = total_cost

        self.lease = deployment["lease"]
        self.operations = operations

    @classmethod
    def fromid(cls, session, resource_id):
        # Grab a dict with the given deployment in there and use as input
        deployment = session.get_consumer_resource(resource_id=resource_id)

        operations = []

        for op in deployment["operations"]:
            base_url = f"https://{session.cloudurl}/catalog-service/api/consumer/resources/"
            op_id = op["id"]
            operation = {"name": op["name"],
                         "description": op["description"],
                         "id": op["id"],
                         "template_url": f"{base_url}{resource_id}/actions/{op_id}/requests/template",
                         "request_url": f"{base_url}{resource_id}/actions/{op_id}/requests"}

            operations.append(operation)


        # session.get_

        return cls(session, deployment, operations)

    def _get_children(self):
        pass

    def scale_out(self, new_value):
        """

        Currently this only works with a single tier app. Need to sort out how to make it better

        :return:
        """


        template = None

        for operation in self.operations:
            if operation["name"] == "Scale Out":
                template = self.session._request(url=operation["template_url"])
                for key, value in template["data"].items():
                    for inner_key, inner_value in template["data"][key]["data"].items():
                        template["data"][key]["data"][inner_key]["data"]["_cluster"] = new_value

        for o in self.operations:
            if o["name"] == "Scale Out":
                scale_out = self.session._request(url=o["request_url"], request_method="POST", payload=template)
                return scale_out
