import os
import logging
import requests
import argparse
import pandas as pd

from get_example_data_token import get_data

def query(query_url: str, model: str):
    data = get_data()
    
    token = os.getenv("TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(query_url, json=data, headers=headers)
    logging.info(f"Response from {model} endpoint: {response.json()}")


def model_ready(url, model):
    token = os.getenv("TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}/v2/health/live", headers=headers)
    response = requests.get(f"{url}/v2/health/ready", headers=headers)
    response = requests.get(f"{url}/v2/models/{model}/ready", headers=headers)

    response = requests.get(f"{url}/v2/models/{model}", headers=headers)
    logging.info(f"\nResponse from {model} endpoint: {response.json()}")

def main(url, query_url, model):
    model_ready(url, model)
    query(query_url, model)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Inference endpoint url",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name",
    )
    args = parser.parse_args()

    endpoint = f"/v2/models/{args.model}/infer"
    query_url = f"{args.url}{endpoint}"

    main(args.url, query_url, args.model)