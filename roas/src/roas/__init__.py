import time
from dotenv import load_dotenv

import requests

from halo import Halo
from rich import print
import argparse

import os

load_dotenv()

BASE_URL = os.environ.get("ROAS_URI")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env")
    args = parser.parse_args()

    USER_ENV = args.env
    if USER_ENV is None:
        USER_ENV = input("Name of robot environment: ")

    POLICY = input("Name of RL policy: ")
    N_TRAINING_EPOCHS = input("Number of training epochs: ")

    spinner = Halo(text="loading...", spinner="bouncingBar")
    spinner.start()
    resp = requests.post(
        BASE_URL + "/api/dev/run",
        json={
            "environment": USER_ENV,
            "policy": POLICY,
            "n_training_epochs": N_TRAINING_EPOCHS,
        },
    )
    spinner.clear()
    print()
    print(resp.json())


# if __name__ == "__main__":
#     typer.run(main)
