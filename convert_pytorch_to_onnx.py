import os
import argparse

from download_s3_folder import download_s3_folder

def main(s3_folder: str, local_dir: str, model_name: str):
    download_s3_folder(s3_folder, local_dir)
    # TODO


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--s3_folder",
        type=str,
        required=True,
        help="S3 folder of model",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="Model file name",
    )
    parser.add_argument(
        "--local_dir",
        type=str,
        required=True,
        help="Local dir for storing model",
    )
    args = parser.parse_args()

    main(args.s3_folder, args.local_dir, args.model_name)