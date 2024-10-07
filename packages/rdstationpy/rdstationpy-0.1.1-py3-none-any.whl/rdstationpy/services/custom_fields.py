from rdstationpy.api_client import ApiClient


class CustomFieldsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/custom_fields"

    def get_custom_field(self, custom_field_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{custom_field_id}")

    def get_custom_fields(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_custom_field(self, data):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_custom_field(self, custom_field_id: str, data):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{custom_field_id}", data=data
        )

    def delete_custom_fiels(self, custom_field_id: str):
        return self.api_client.make_request(
            "DELETE",
            f"{self.resource}/{custom_field_id}",
        )
