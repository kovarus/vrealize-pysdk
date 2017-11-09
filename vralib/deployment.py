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

    def __init__(self, session, deployment, operations, deployment_children):
        """

        :param session:
        :param deployment:
        :param operations:
        :param deployment_children:
        """
        self.session = session
        self.deployment_json = deployment
        self.resource_id = deployment["id"]
        self.resource_type = deployment["resourceTypeRef"]
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

        self.deployment_children = deployment_children

        if "parentResourceRef" in deployment.keys():
            self.parent_resource = deployment["parentResourceRef"]

    @classmethod
    def fromid(cls, session, resource_id):
        """Creates an instance based on the GUID in vRA. If the deployment has children it will attempt to resolve them
        and store them in a list as deployment_children.

        :param session:
        :param resource_id:
        :return:
        """
        # Grab a dict with the given deployment in there and use as input
        deployment = session.get_consumer_resource(resource_id=resource_id)
        # Store operations and deployment children in a list
        operations = []
        deployment_children = []

        for op in deployment["operations"]:
            base_url = f"https://{session.cloudurl}/catalog-service/api/consumer/resources/"
            op_id = op["id"]
            operation = {"name": op["name"],
                         "description": op["description"],
                         "id": op["id"],
                         "template_url": f"{base_url}{resource_id}/actions/{op_id}/requests/template",
                         "request_url": f"{base_url}{resource_id}/actions/{op_id}/requests"}

            operations.append(operation)

        # See if we have children and if we do create an instance of the appropriate class
        if deployment["hasChildren"] == True:
            children = Deployment._get_children(session, resource_id)
            for child in children["content"]:
                if child["resourceType"] == "Infrastructure.Virtual":
                    deployment_children.append(VirtualMachine.fromid(session, child["resourceId"]))
                if child["resourceType"] == "Infrastructure.Network.LoadBalancer.NSX":
                    deployment_children.append(LoadBalancer.fromid(session, child["resourceId"]))
                if child["resourceType"] == "Infrastructure.Network.Gateway.NSX.Edge":
                    deployment_children.append(Edge.fromid(session, child["resourceId"]))
                if child["resourceType"] == "Infrastructure.Network.Network.Existing":
                    deployment_children.append(Network.fromid(session, child["resourceId"]))
                if child["resourceType"] == "composition.resource.type.deployment":
                    deployment_children.append(Deployment.fromid(session, child["resourceId"]))

        return cls(session, deployment, operations, deployment_children)

    @staticmethod
    def _get_children(session, resource_id):
        base_url = f"https://{session.cloudurl}/catalog-service/api/consumer/resourceViews"
        arguments = f"?managedOnly=false&withExtendedData=true&withOperations=true&$filter=parentResource eq '{resource_id}'"
        children = session._request(url=base_url+arguments)
        return children

    def scale_out(self, new_value):
        """Currently this only works with a single tier app. Need to sort out how to make it better

        :return:
        """
        # TODO consider replacing this method with one method that does both based in input value (i.e. out or in)
        # TODO look for a cleaner way to parse the template since there is a possibility of multiple children that might need scaling
        # Maybe create an instance for each child?
        # TODO need to re-write this since we can now have access to individual children
        # TODO maybe make a generic day 2 operation with **kwargs to drive it?

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

    def get_operation_template(self, operation):
        """Used to collect a template for use in the execute_operation() method. The template should be modified before
        sending to the execute_operation() method.

        :param operation: A string that includes the name of an operation. Operations can be found stored in the
        operations attribute

        :return: A Python dictionary that may be modified and used in the execute_operation() method
        """
        for o in self.operations:
            if o["name"] == operation:
                return self.session._request(url=o["template_url"])

    def execute_operation(self, operation, payload):
        for o in self.operations:
            if o["name"] == operation:
                return self.session._request(url=o["request_url"], request_method="POST", payload=payload)


    def destroy(self, force=False):
        """Used to destroy the deployment. The deployment may be force destroyed if it failed previously.

        Basic Usage::
            #>>> deployment = vralib.Deployment.fromid(session=vra, resource_id="28e735b6-04d3-46d1-bf4e-ca7210b2cba4")
            #>>> deployment.destroy()

        Note that if force is set to True it will throw an error 400

        :param force: Boolean, if set to True it will attempt to force the destroy.
                      This should only be invoked if a regular destroy fails
        :return:
        """
        #LOL for some reason forcing a destroy will make the server return an error 400 telling you
        #LOL     that you can only force out a previously failed destroy action
        template = self.get_operation_template(operation="Destroy")
        if force:
            template["data"]["ForceDestroy"] = "True"

        return self.execute_operation(operation="Destroy", payload=template)

    def expire(self):
        """Expires the deployment

        Basic Usage::
            #>>> deployment = vralib.Deployment.fromid(session=vra, resource_id="28e735b6-04d3-46d1-bf4e-ca7210b2cba4")
            #>>> deployment.expire()

        :return: A byte string of the response from the webserver. On success it will be empty.
        """
        template = self.get_operation_template(operation="Expire")
        return self.execute_operation(operation="Expire", payload=template)

    def change_lease(self, expiration_date):
        """Used to change the lease of the deployment.

        Basic Usage::

            #>>> deployment = vralib.Deployment.fromid(session=vra, resource_id="28e735b6-04d3-46d1-bf4e-ca7210b2cba4")
            #>>> deployment.change_lease(expiration_date="2018-12-15T19:31:54.672Z")

        :param expiration_date: String formatted date in ISO 8601 format. For example: "2018-12-15T19:31:54.672Z"
        :return: A byte string of the response from the webserver. On success it will be empty.
        """
        #LOL date needs to include an ISO 8601 timestamp down to the millisecond. Should probably just be ok with date.
        template = self.get_operation_template(operation="Change Lease")
        template["data"]["provider-ExpirationDate"] = expiration_date

        return self.execute_operation(operation="Change Lease", payload=template)



class VirtualMachine(Deployment):
    """
    This class is used to manage VirtualMachine specific deployments. It provides a handful of helpful methods
    specific to virtual machines.

    """

    def power_cycle(self):
        template = self.get_operation_template(operation="Power Cycle")
        return self.execute_operation(operation="Power Cycle", payload=template)

    def power_on(self):
        template = self.get_operation_template(operation="Power On")
        return self.execute_operation(operation="Power On", payload=template)

    def power_off(self):
        template = self.get_operation_template(operation="Power Off")
        return self.execute_operation(operation="Power Off", payload=template)

    def reboot(self):
        template = self.get_operation_template(operation="Reboot")
        return self.execute_operation(operation="Reboot", payload=template)

    def install_tools(self):
        template = self.get_operation_template(operation="Install Tools")
        return self.execute_operation(operation="Install Tools", payload=template)

    def get_reconfigure_template(self):
        pass

    def reconfigure(self):
        pass

    def shutdown(self):
        pass

    def suspend(self):
        pass

    def snapshot(self):
        pass

    def get_snapshots(self):
        pass

    def rollback_snapshot(self):
        pass


class LoadBalancer(Deployment):
    """Waiting to implement this due to bug in the vRA 7.3 API with retrieving template"""
    pass

class Edge(Deployment):
    pass

class Network(Deployment):
    pass
