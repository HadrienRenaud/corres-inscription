import csv


class ConversionError(Exception):
    pass


def isnumeric(x: str) -> bool:
    return x.replace('.', '', 1).isdigit()


def parse(content: str):
    if isnumeric(content):
        try:
            content = float(content)
        except TypeError as e:
            raise ConversionError from e
        print(content)
        if int(content) == content:
            return content
        return content
    else:
        return content


def extract(file):
    res = []
    with open(file, 'r') as opened_file:
        reader = csv.reader(opened_file, delimiter=",", quotechar='"')
        for row in reader:
            res.append(row)
    return [[parse(cell) for cell in row] for row in res]
