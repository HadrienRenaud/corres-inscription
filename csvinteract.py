import csv
from typing import List

__all__ = ["extract", "ConversionError"]


class ConversionError(Exception):
    """Base conversion error. Should never happen."""
    pass


def isnumeric(x: str) -> bool:
    """Check if a string can be converted into a float/int."""
    return x.replace('.', '', 1).isdigit()


def parse_cell(content: str):
    """convert a string into the best format possible."""
    if isnumeric(content):
        try:
            content = float(content)
        except TypeError as e:
            raise ConversionError from e
        if int(content) == content:
            return content
        return content
    else:
        return content


def extract(file: str) -> List[List]:
    """Extract from a csv file the good data."""
    res = []
    with open(file, 'r') as opened_file:
        reader = csv.reader(opened_file, delimiter=",", quotechar='"')
        for row in reader:
            res.append(row)
    return [[parse_cell(cell) for cell in row] for row in res]
