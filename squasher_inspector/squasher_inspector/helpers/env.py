from dataclasses import dataclass
from os import environ

from dotenv import find_dotenv, load_dotenv


@dataclass
class Env:
    # lapsquash_squasher からみた相対パス
    INSPECT_TARGET_OUT_DIR: str
    INSPECT_TRUE_OUT_DIR: str


def getEnv() -> Env:
    load_dotenv(find_dotenv())
    return Env(
        INSPECT_TARGET_OUT_DIR=environ["INSPECT_TARGET_OUT_DIR"],
        INSPECT_TRUE_OUT_DIR=environ["INSPECT_TRUE_OUT_DIR"],
    )
