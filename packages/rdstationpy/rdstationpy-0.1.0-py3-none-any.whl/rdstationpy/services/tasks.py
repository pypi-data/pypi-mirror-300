from rdstationpy.api_client import ApiClient


class TasksService:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client
        self.resource = "/tasks"

    def get_task(self, task_id: str):
        return self.api_client.make_request("GET", f"{self.resource}/{task_id}")

    def get_tasks(self, **kwargs) -> (int, bool, list):
        return self.api_client.make_request("GET", f"{self.resource}", **kwargs)

    def post_task(self, data: dict):
        return self.api_client.make_request("POST", f"{self.resource}", data=data)

    def put_task(self, task_id: str, data: dict):
        return self.api_client.make_request(
            "PUT", f"{self.resource}/{task_id}", data=data
        )
