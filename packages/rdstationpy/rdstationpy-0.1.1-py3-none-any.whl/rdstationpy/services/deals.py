from rdstationpy.api_client import ApiClient


class DealsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/deals"

    def get_deal(self, deal_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{deal_id}")

    def get_deals(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def get_contacts_from_deal(self, deal_id: str):
        return self.api_client.make_request(
            "GET", f"{self.resource}/{deal_id}/contacts"
        )

    def post_deal(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_deal(self, deal_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{deal_id}", data=data
        )

    def get_products_from_deal(self, deal_id: str):
        return self.api_client.make_request(
            "GET", f"{self.resource}/{deal_id}/deal_products"
        )

    def post_product_in_deal(self, deal_id: str, data: dict):
        return self.api_client.make_request(
            "POST", f"{self.resource}/{deal_id}/deal_products", data=data
        )

    def post_products_bactch_in_deal(self, deal_id: str, data: dict):
        return self.api_client.make_request(
            "POST", f"{self.resource}/{deal_id}/deal_products/batch", data=data
        )

    def put_product_in_deal(self, deal_id: str, product_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{deal_id}/deal_products/{product_id}", data=data
        )

    def patch_products_batch_in_deal(self, deal_id: str, data: dict):
        return self.api_client.make_request(
            "PATCH", f"{self.resource}/{deal_id}/deal_products/batch/update", data=data
        )

    def delete_product_in_deal(self, deal_id: str, product_id: str):
        return self.api_client.make_request(
            "DELETE", f"{self.resource}/{deal_id}/deal_products/{product_id}"
        )

    def delete_product_batch_in_deal(self, deal_id: str):
        return self.api_client.make_request(
            "DELETE", f"{self.resource}/{deal_id}/deal_products/batch/destroy"
        )
