from rdstationpy.api_client import ApiClient


class ContactsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/contacts"

    def get_contact(self, contact_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{contact_id}")

    def get_contacts(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_contact(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_contact(self, contact_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{contact_id}", data=data
        )
