import os
import logging
import requests
import argparse
import pandas as pd
import torch
import torchvision
import torchvision.transforms as T
from PIL import Image
import numpy as np

def query(query_url: str, model: str):
    dummy_input = torch.randn(1, 3, 224, 224).numpy()
    dummy_data = dummy_input.tolist()

    data = {
        "inputs": [
            {
                "name": "actual_input",
                "data": dummy_data,
                "datatype": "FP32",
                "shape": list(dummy_input.shape)
            },
        ]
    }
    
    token = os.getenv("TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(query_url, json=data, headers=headers).json()
    logging.info(f"Response from {model} endpoint: {response}")

    prediction = np.asarray(response["outputs"][0]["data"]).argmax() 
    print(prediction)

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