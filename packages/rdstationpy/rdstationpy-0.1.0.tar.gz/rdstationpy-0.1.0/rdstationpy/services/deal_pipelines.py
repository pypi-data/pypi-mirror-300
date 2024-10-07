from rdstationpy.api_client import ApiClient


class DealPipelines:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/deal_pipelines"

    def get_deal_pipeline(self, deal_pipeline_id: str):
        return self.api_client.make_request(
            "GET", f"{self.resource}/{deal_pipeline_id}"
        )

    def get_deal_pipelines(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_deal_pipeline(self, data):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_deal_pipeline(self, deal_pipeline_id: str, data):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{deal_pipeline_id}", data=data
        )
