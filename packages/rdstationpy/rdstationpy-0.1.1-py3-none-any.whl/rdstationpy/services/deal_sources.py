from rdstationpy.api_client import ApiClient


class DealSourcesService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/deal_sources"

    def get_deal_source(self, deal_source_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{deal_source_id}")

    def get_deal_sources(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_deal_source(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_deal_source(self, deal_source_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{deal_source_id}", data=data
        )
