from rdstationpy.api_client import ApiClient


class ActivitiesService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/activities"

    def get_activities(self, activities_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{activities_id}")

    def post_activitie(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)
