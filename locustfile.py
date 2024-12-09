import os

from dotenv import load_dotenv
from locust import HttpUser, task, between, constant

load_dotenv()
token_string = os.getenv('TOKEN')

from get_example_data_token import get_data

class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.get("/v2/models/onnx-gliner", headers={"Authorization": f"Bearer {token_string}"})

    @task
    def test_model_query(self):
        data = get_data()
        self.client.post("/v2/models/onnx-gliner/infer", json=data, headers={"Authorization": f"Bearer {token_string}"})