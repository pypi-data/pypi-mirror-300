from rdstationpy.api_client import ApiClient


class DealLostReasonsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/deal_lost_reasons"

    def get_deal_lost_reason(self, deal_lost_reason_id: str):
        return self.api_client.make_request(
            "GET", f"{self.resource}/{deal_lost_reason_id}"
        )

    def get_deal_lost_reasons(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_deal_lost_reason(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_deal_lost_reason(self, deal_lost_reason_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{deal_lost_reason_id}", data=data
        )
