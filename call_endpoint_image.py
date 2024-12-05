import os
import logging
import requests
import argparse
import pandas as pd

def query(query_url: str, model: str, filename: str, filepath: str, height: int, width: int):
    # TODO data input must be different
    with open(filepath, "rb") as f:
        data = f.read()
    
    token = os.getenv("TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(query_url, data=data, headers=headers)
    logging.info(f"Response from {model} endpoint: {response.json()}")

def prepare_data(data_dir, data_list):
    # Ensure the data directory exists
    if not os.path.exists(data_dir):
        raise ValueError("data dir not found")

    # Load as pandas
    df = pd.read_csv(data_list, sep='|')
    df["filepath"] = [os.path.join(data_dir,f) for f in df.iloc[:, 0]]

    files = [os.path.join(data_dir,f) for f in df.iloc[:, 0] if os.path.isfile(os.path.join(data_dir,f))]
    if len(files) == 0:
        raise ValueError("data files not found")

    return df

def model_ready(url, model):
    token = os.getenv("TOKEN")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}/v2/health/live", headers=headers)
    response = requests.get(f"{url}/v2/health/ready", headers=headers)
    response = requests.get(f"{url}/v2/models/{model}/ready", headers=headers)

    response = requests.get(f"{url}/v2/models/{model}", headers=headers)
    logging.info(f"Response from {model} endpoint: {response.json()}")

def main(url, query_url, model, data_dir, data_list):
    model_ready(url, model)
    df = prepare_data(data_dir, data_list)

    for name, height, width, filepath in zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, -1]):
        output = query(query_url, model, name, filepath, height, width)
        break

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
    parser.add_argument(
        "--data_dir",
        type=str,
        help="Data directory",
        default="datasets/mini_coco/data"
    )
    parser.add_argument(
        "--data_list",
        type=str,
        help="Data csv",
        default="datasets/mini_coco/img_data.psv"
    )
    args = parser.parse_args()

    endpoint = f"/v2/models/{args.model}/infer"
    query_url = f"{args.url}{endpoint}"

    main(args.url, query_url, args.model, args.data_dir, args.data_list)