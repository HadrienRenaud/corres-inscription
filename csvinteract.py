import csv


def extract(file):
    res = []
    reader = csv.reader(file, delimiter=",", quotechar='"')
    for row in reader:
        res.append(row)
    return res
