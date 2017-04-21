import json
import requests

class Tenant(object):
    pass

class BusinessGroup(Tenant):
    def __init__(self):
        pass

    @staticmethod
    def get_businessgroups(session, tenant=None):
        pass



class Reservation(BusinessGroup):


    @classmethod
    def get_fromid(cls, session, id):
        pass

    @classmethod
    def get_fromname(cls, session, name):
        pass

    @staticmethod
    def get_reservations(session):
        pass

    @staticmethod
    def create_reservation():
        pass

    @staticmethod
    def get_reservation_types(session):
        pass



