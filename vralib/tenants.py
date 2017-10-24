import json
import requests
from .classes import Session

class Tenant(Session):
    pass

class BusinessGroup(Tenant):

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



