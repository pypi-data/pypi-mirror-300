import argparse
import os
import math
from typing import Optional
from dotenv import load_dotenv
from cloud_storage_size import get_bucket_objects_count_and_bytes
import json
from rsize import __version__


def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as f:
        return json.load(f)


def format_size(size_bytes: int, human_readable: bool) -> str:
    if not human_readable:
        return str(size_bytes)

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def main():
    parser = argparse.ArgumentParser(description='Calculate the size of files in Cloud Storage')
    parser.add_argument('bucket', type=str, help='GCS bucket path (e.g., gs://bucket_name)')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-c', '--config', type=str, help='Path to config file')
    parser.add_argument('-e', '--env-file', type=str, help='Path to .env file')
    parser.add_argument('-H', '--human-readable', action='store_true', help='Display sizes in human-readable format')

    args = parser.parse_args()

    # Load configuration
    if args.config:
        config = load_config(args.config)
        for key, value in config.items():
            os.environ[key] = value
    elif args.env_file:
        load_dotenv(args.env_file)
    else:
        load_dotenv()  # Load default .env file

    bucket_name = args.bucket

    # Call the cloud_storage_size function
    result = get_bucket_objects_count_and_bytes(bucket_name)
    count = result["count"]
    total_bytes = result["bytes"]

    # Display results
    if args.human_readable:
        total_size = format_size(total_bytes, True)
        print(f"Total objects: {count}")
        print(f"Total size: {total_size}")
    else:
        print(f"Total objects: {count}")
        print(f"Total size in bytes: {total_bytes}")

if __name__ == "__main__":
    main()
