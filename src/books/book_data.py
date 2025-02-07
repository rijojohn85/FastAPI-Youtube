from typing import List

from .models import Book

books:List[Book] = [
    Book(
    id=1,
        title="Think Python",
        author= "Allen B. Downey",
        publisher= "O'Reilly Media",
        published_date= "2021-01-01",
        page_count= 1234,
        language= "English",
    ),
    Book(
        id= 2,
        title= "Django By Example",
        author= "Antonio Mele",
        publisher= "Packt Publishing Ltd",
        published_date= "2022-01-19",
        page_count= 1023,
        language= "English",
    ),
    Book(
        id= 3,
        title= "The web socket handbook",
        author= "Alex Diaconu",
        publisher= "Xinyu Wang",
        published_date= "2021-01-01",
        page_count= 3677,
        language= "English",
    ),
    Book(
        id= 4,
        title= "Head first Javascript",
        author= "Hellen Smith",
        publisher= "Oreilly Media",
        published_date= "2021-01-01",
        page_count= 540,
        language= "English",
    ),
    Book(
        id= 5,
        title= "Algorithms and Data Structures In Python",
        author= "Kent Lee",
        publisher= "Springer, Inc",
        published_date= "2021-01-01",
        page_count= 9282,
        language= "English",
    ),
    Book(
        id= 6,
        title= "Head First HTML5 Programming",
        author= "Eric T Freeman",
        publisher= "O'Reilly Media",
        published_date= "2011-21-01",
        page_count= 3006,
        language= "English",
    ),
]
