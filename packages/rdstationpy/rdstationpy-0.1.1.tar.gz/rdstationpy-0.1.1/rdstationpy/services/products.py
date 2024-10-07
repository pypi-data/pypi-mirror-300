from rdstationpy.api_client import ApiClient


class ProductsService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/products"

    def get_product(self, product_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{product_id}")

    def get_products(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_product(self, data):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_product(self, product_id, data):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{product_id}", data=data
        )
