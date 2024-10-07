from rdstationpy.api_client import ApiClient
from rdstationpy.services.contacts import ContactsService


class RDStation:
    def __init__(self, api_key, url="https://crm.rdstation.com/api/v1", config=None):
        self.api_client = ApiClient(api_key, url, config)

        self.contacts = ContactsService(self.api_client)
