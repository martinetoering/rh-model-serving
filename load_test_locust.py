import os

from dotenv import load_dotenv
from locust import HttpUser, task, between, constant

load_dotenv()
token_string = os.getenv('TOKEN')


class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.post("/api/v0/Users/login", json={"email": "user@testuser.com", "password": "password"})

    @task
    def test_find_one(self):
        self.client.get("/api/v0/Properties/findOne", headers={"authorization": "Bearer " + token_string})

    @task
    def test_find(self):
        params = {
            "filter": '{"limit": 100}'
        }
        self.client.get("/api/v0/Properties", headers={"authorization": "Bearer " + token_string}, params=params)