# type: ignore

from dataclasses import dataclass
from typing import Callable

from bardapi import Bard


@dataclass
class TBardResponse:
    content: str
    conversation_id: str
    response_id: str
    factuality_queries: list
    text_query: str
    choices: list
    links: list
    images: set
    program_lang: str
    code: str
    status_code: int


class TBard:
    def __init__(self, bard: Bard) -> None:
        self.bard = bard

    def getAnswer(self) -> Callable[[str], TBardResponse]:
        return self.bard.get_answer

    def askAboutImage(
        self,
    ) -> Callable[[str, bytes, str], dict[TBardResponse]]:
        return self.bard.ask_about_image
