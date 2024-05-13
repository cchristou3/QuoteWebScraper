from dataclasses import dataclass
from typing import List


@dataclass
class Quote:
    text: str
    author: str
    tags: List[str]

    def to_excel_row(self):
        return {'Quote': self.text, 'Author': self.author, 'Tags': ', '.join(self.tags)}
