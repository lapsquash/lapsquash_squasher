from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Env:
    # lapsquash_squasher からみた相対パス
    INSPECT_TARGET_OUT_DIR: str
    INSPECT_TRUE_OUT_DIR: str


def getEnv() -> Env:
    raise NotImplementedError("getEnv is not implemented")
