# Klasy
import os
import pandas as pd


class Dataset:
    def __init__(self, df, name):
        self.df = df
        self.name = name


class Database:
    DATABASE_PATH = "datasets"

    @staticmethod
    def add_to_database(df, name):
        df.to_pickle(f"{Database.DATABASE_PATH}/{name}.pkl")

    @staticmethod
    def list_datasets():
        existing_names = [
            name.replace(".pkl", "") for name in os.listdir(Database.DATABASE_PATH)
        ]
        return existing_names

    @staticmethod
    def list_info(): ...

    @staticmethod
    def load_dataset(name: str) -> Dataset:
        # safe check
        name = name + ".pkl" if not name.endswith(".pkl") else name
        df = pd.read_pickle(f"{Database.DATABASE_PATH}/{name}")
        dataset = Dataset(df, name)
        return dataset

    @staticmethod
    def remove_dataset(): ...
