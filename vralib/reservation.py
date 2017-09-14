"""

    Python module for interfacing with the vRealize API
    Primarily used for reporting initially.

    This thing is kind of a mess so tread carefully while I piece it back together.

"""
# TODO Add values for Network, Storage, Computer to object. Multiple nested Arrays. Do it based on index? 
# TODO Create reporting functionality off of reservation object. Pretty tables?  


__author__ = 'Cody De Arkland'

class Reservation(object):
    """
    Manage existing reservations

    """
    def __init__(self, session, reservation):
        self.session = session
        self.reservation_json = reservation
        self.reservation_id = reservation['id']
        self.name = reservation['name']
        self.created_date = reservation['createdDate']
        self.tenantId = reservation['tenantId']
        self.subTenantId = reservation['subTenantId']
        self.enabled = reservation['enabled']

    @classmethod
    def fromid(cls, session, reservation_id):
        reservation = session.get_reservation(reservation_id=reservation_id)

        return cls(session, reservation)