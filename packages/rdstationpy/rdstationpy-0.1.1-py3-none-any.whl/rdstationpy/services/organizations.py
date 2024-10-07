from rdstationpy.api_client import ApiClient


class OrganizationsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/organizations"

    def get_organization(self, organization_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{organization_id}")

    def get_organizations(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def get_contacts_from_organization(self, organization_id: str):
        return self.api_client.make_request(
            "GET", f"{self.resource}/{organization_id}/contacts"
        )

    def post_organization(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_organization(self, organization_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{organization_id}", data=data
        )
