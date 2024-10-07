from rdstationpy.api_client import ApiClient


class WebhooksService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/webhooks"

    def get_webhook(self, webhook_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{webhook_id}")

    def get_webhooks(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_webhook(self, data):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_webhook(self, webhook_id: str, data):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{webhook_id}", data=data
        )

    def delete_custom_fiels(self, webhook_id: str):
        return self.api_client.make_request(
            "DELETE",
            f"{self.resource}/{webhook_id}",
        )
