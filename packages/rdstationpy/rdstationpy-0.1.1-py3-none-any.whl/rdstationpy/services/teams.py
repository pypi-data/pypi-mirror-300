from rdstationpy.api_client import ApiClient


class TeamsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/teams"

    def get_team(self, team_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{team_id}")

    def get_teams(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)
