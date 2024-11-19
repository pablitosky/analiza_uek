# Funkcje
import pandas as pd
from classes import Database


def validate_name(name):
    if name in Database.list_datasets():
        return False
    return True
