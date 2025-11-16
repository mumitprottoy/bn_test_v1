import os, csv
from .models import BetaTester


def add_testers(file_path: str) -> None:
    file = open(file_path)
    reader = csv.DictReader(file)
    for row in reader:
        BetaTester.create(**row)


def add_batch_1():
    add_testers(f'{os.getcwd()}/beta_testers_1.csv')
