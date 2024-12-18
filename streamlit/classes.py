# Klasy
import os
import pandas as pd
import streamlit as st
from abc import ABC, abstractmethod
from utils import S3Connector


class Dataset:
    """
    A class used to represent a Dataset.

    Attributes
    ----------
    df : pandas.DataFrame
        The dataframe containing the dataset.
    name : str
        The name of the dataset.

    Methods
    -------
    __init__(self, df, name)
        Initializes the Dataset with a dataframe and a name.
    """
    def __init__(self, df:pd.DataFrame, name:str):
        self.df = df
        self.name = name

class DatabaseInterface(ABC):
    @abstractmethod
    def load_df(self, name):
        pass

    @abstractmethod
    def add_to_database(self, df, name):
        pass

    @abstractmethod
    def list_datasets(self):
        pass

    @abstractmethod
    def load_dataset(self, name):
        pass

    @abstractmethod
    def remove_dataset(self, name):
        pass

class Database(DatabaseInterface):
    """
    A class to handle database operations for datasets.

    Attributes:
    ----------
    DATABASE_PATH : str
        The path to the directory where datasets are stored.

    Methods:
    -------
    load_df(name: str) -> pd.DataFrame
        Loads a DataFrame from a pickle file.

    add_to_database(df: pd.DataFrame, name: str) -> None
        Saves a DataFrame to a pickle file in the database.

    list_datasets() -> List[str]
        Lists all dataset names in the database.

    load_dataset(name: str) -> Dataset
        Loads a dataset by name and returns a Dataset object.

    remove_dataset(name: str) -> bool
        Removes a dataset from the database by name.
    """
    """"""
    # FILE STATIC DATABASE
    DATABASE_PATH = "../datasets"

    @st.cache_data
    @staticmethod
    def load_df(name:str):
        return pd.read_pickle(f"{Database.DATABASE_PATH}/{name}")

    @staticmethod
    def add_to_database(df:pd.DataFrame, name:str):
        df.to_pickle(f"{Database.DATABASE_PATH}/{name}.pkl")

    @staticmethod
    def list_datasets():
        existing_names = [
            name.replace(".pkl", "") for name in os.listdir(Database.DATABASE_PATH)
        ]
        return existing_names

    @staticmethod
    def load_dataset(name: str) -> Dataset:
        # safe check
        name = name + ".pkl" if not name.endswith(".pkl") else name
        df = Database.load_df(name)
        dataset = Dataset(df, name)
        return dataset

    @staticmethod
    def remove_dataset(name:str):
        try:
            os.remove(f"{Database.DATABASE_PATH}/{name}.pkl")
            return True
        except Exception as e:
            st.warning(f"Error: {e}")
            return False
    @staticmethod 
    def validate_name(name):
        if name in Database.list_datasets():
            return False
        return True
        

class Minio(DatabaseInterface):
    """
    A class to interact with a MinIO database using an S3 connector.

    Attributes
    ----------
    bucket_name : str
        The name of the bucket to interact with in the MinIO database.
    s3 : S3Connector
        An instance of the S3Connector to handle S3 operations.

    Methods
    -------
    __init__(bucket_name='data')
        Initializes the Minio class with a specified bucket name.
    load_df(name)
        Loads a DataFrame from the MinIO database.
    add_to_database(df, name)
        Adds a DataFrame to the MinIO database.
    list_datasets()
        Lists all datasets in the MinIO database.
    load_dataset(name)
        Loads a dataset from the MinIO database and returns it as a Dataset object.
    remove_dataset(name)
        Removes a dataset from the MinIO database.
    """
    # MINIO DATABASE
    def __init__(self, bucket_name:str='data'):
        self.bucket_name = bucket_name
        self.s3 = S3Connector(bucket=bucket_name)

    def load_df(self, name:str):
        return self.s3.load_object(name)

    def add_to_database(self, df:pd.DataFrame, name:str):
        return self.s3.upload_object(df, name)

    def list_datasets(self):
        datasets = [name.replace(".pkl", "") for name in self.s3.list_objects()]
        return datasets

    def load_dataset(self, name:str):
        df = self.load_df(f'{name}.pkl')
        dataset = Dataset(df, name)
        return dataset

    def remove_dataset(self, name:str):
        return self.s3.delete_objects(name)
    
    def validate_name(self,name):
        if name in self.list_datasets():
            return False
        return True



