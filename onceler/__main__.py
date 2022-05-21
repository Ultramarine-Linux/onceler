import os
from .log import get_logger

logger = get_logger(__name__)

if not os.path.isfile("onceler.toml"):
        logger.fatal("onceler.toml not found!")
        exit(1)

from .lorax import Onceler

import typer

def main(variant: str):
    """Builds a variant defined in onceler.toml"""
    onceler = Onceler()
    onceler.build(variant)

if __name__ == "__main__":
    typer.run(main)