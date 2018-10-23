import csv
from typing import List, Tuple, Union

Number = Union[int, float]
Converted = Union[Number, str]


class ConversionError(Exception):
    """Base conversion error. Should never happen."""
    pass


def _isnumeric(x: str) -> bool:
    """Check if a string can be converted into a float/int."""
    try:
        _ = float(x)
    except ValueError:
        return False
    return True


def _parse_cell(content: str) -> Converted:
    """convert a string into the best format possible."""
    if _isnumeric(content):
        try:
            content = float(content)
        except ValueError as e:
            raise ConversionError from e
        if int(content) == content:
            return content
        return content
    else:
        return content


def extract(file: str) -> Tuple[List[List[Converted]], List[str]]:
    """Extract from a csv file the good data."""
    res = []
    with open(file, 'r') as opened_file:
        reader = csv.reader(opened_file, delimiter=",", quotechar='"')
        for row in reader:
            res.append(row)
    return [[_parse_cell(cell) for cell in row] for row in res[1:]], res[0]
