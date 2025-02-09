import uuid
from typing import List
import datetime

from .schemas import Book

books: List[Book] = [
    Book(
        uid=uuid.uuid4(),
        title="Think Python",
        author="Allen B. Downey",
        publisher="O'Reilly Media",
        published_date="2020-01-01",
        page_count=1234,
        language="English",
        created_at=datetime.datetime(2020, 1, 1),
        updated_at=datetime.datetime(2020, 1, 1),
    ),
    Book(
        uid=uuid.uuid4(),
        title="Django By Example",
        author="Antonio Mele",
        publisher="Packt Publishing Ltd",
        published_date="2020-01-01",
        page_count=1023,
        language="English",
        created_at=datetime.datetime(2020, 1, 1),
        updated_at=datetime.datetime(2020, 1, 1),
    ),
    Book(
        uid=uuid.uuid4(),
        title="The web socket handbook",
        author="Alex Diaconu",
        publisher="Xinyu Wang",
        published_date="2020-01-01",
        page_count=3677,
        language="English",
        created_at=datetime.datetime(2021, 1, 1),
        updated_at=datetime.datetime(2021, 1, 1),
    ),
    Book(
        uid=uuid.uuid4(),
        title="Head first Javascript",
        author="Hellen Smith",
        publisher="Oreilly Media",
        published_date="2020-01-01",
        page_count=540,
        language="English",
        created_at=datetime.datetime(2021, 1, 1),
        updated_at=datetime.datetime(2021, 1, 1),
    ),
    Book(
        uid=uuid.uuid4(),
        title="Algorithms and Data Structures In Python",
        author="Kent Lee",
        publisher="Springer, Inc",
        published_date="2020-01-01",
        page_count=9282,
        language="English",
        created_at=datetime.datetime(2021, 1, 1),
        updated_at=datetime.datetime(2021, 1, 1),
    ),
    Book(
        uid=uuid.uuid4(),
        title="Head First HTML5 Programming",
        author="Eric T Freeman",
        publisher="O'Reilly Media",
        published_date="2020-01-01",
        page_count=3006,
        language="English",
        created_at=datetime.datetime(2021, 1, 1),
        updated_at=datetime.datetime(2021, 1, 1),
    ),
]
