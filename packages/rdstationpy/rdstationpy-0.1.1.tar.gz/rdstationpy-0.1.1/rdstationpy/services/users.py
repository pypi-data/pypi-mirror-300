from rdstationpy.api_client import ApiClient


class UsersService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/users"

    def get_user(self, user_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{user_id}")

    def get_users(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)
