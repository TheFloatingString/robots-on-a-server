from rich import print
import typer

import time
from halo import Halo


def main():
    spinner = Halo(text="loading...", spinner="bouncingBar")
    spinner.start()
    time.sleep(3)
    spinner.clear()
    print()
    print({"data": 12})


if __name__ == "__main__":
    typer.run(main)
