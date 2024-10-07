from dataclasses import dataclass
from itertools import product

from justwatch import details, offers_for_countries, search


@dataclass
class Base:
    base_field_1: int
    base_field_2: int


@dataclass
class Child(Base):
    child_field_1: int


def main():
    obj = Child(1, 2, 3)
    # result = details("ts4")  # Breaking Bad
    # result = details("tss25")  # Breaking Bad S5
    # result = details("tse411")  # Breaking Bad S5E1
    # result = details("tm10")
    # print(result)  # The Matrix
    # result = details("ts20711")  # The Simpsons
    # result = details("tm118477")  # Haker (2002)
    # result = search("The Simpsons")
    result = search("The Matrix", "US", "en", 3, True)
    print(result)
    print()


if __name__ == "__main__":
    main()
