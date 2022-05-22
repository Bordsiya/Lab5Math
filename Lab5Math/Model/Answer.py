from dataclasses import dataclass


@dataclass
class Answer:
    ok: bool
    message: str
    answer: float

