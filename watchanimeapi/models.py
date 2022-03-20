from typing import List, Tuple


class Episode:
    def __init__(self, title: str, number: int, is_filer: str, link: str):
        self.title = title
        self.number = number
        self.is_filler = is_filer
        self.link = link

    def get_summary(self) -> Tuple[int, str, str]:
        return self.number, self.title, self.is_filler


class AnimeModel:
    def __init__(self, url: str, title: str, description: str, kind: str):
        self.url = url
        self.title = title
        self.description = description
        self.type = kind

    def get_short_info(self) -> Tuple:
        return self.title, self.type

    def __str__(self) -> str:
        summary = f"{self.title}    {self.type}\n" \
                  f"Opis: {self.description}"
        return summary
