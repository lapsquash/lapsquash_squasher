import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Env:
    BARD_API_KEY: str


def getEnv() -> Env:
    bardApiKey = os.environ["BARD_API_KEY"]
    if len(bardApiKey) == 0:
        raise Exception("BARD_API_KEY is not set in .env")

    return Env(
        BARD_API_KEY=bardApiKey,
    )
