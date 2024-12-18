# S3
import os
import boto3
import pandas as pd
from tempfile import NamedTemporaryFile

class S3Connector:
    """A class to handle interactions with an S3 bucket.
    Attributes:
    -----------
    bucket : str
        The name of the S3 bucket.
    s3 : boto3.client
        The boto3 client for S3.
    s3_resource : boto3.resource
        The boto3 resource for S3.
    Methods:
    --------
    list_objects(prefix: str = '') -> list:
        Lists objects in the S3 bucket with the given prefix.
    load_object(path: str):
        Loads an object from the S3 bucket. Supports .pkl and .csv files.
    upload_object(obj, path: str) -> str:
        Uploads an object to the S3 bucket. Supports pandas DataFrame objects.
    delete_objects(prefix: str = ''):
        Deletes objects in the S3 bucket with the given prefix.
    """
    def __init__(self, bucket:str, creds=None):
        if creds is None:
            creds = dict(
                endpoint_url = 'http://minio:8000',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
            
        self.s3 = boto3.client('s3', 
                                config=boto3.session.Config(signature_version='s3v4'),
                                **creds)
        self.s3_resource = boto3.resource('s3', endpoint_url=creds['endpoint_url'])
        self.bucket = bucket
        
    def list_objects(self, prefix:str=''):
        bucket = self.bucket
        try:
            response = self.s3.list_objects(Bucket=bucket, Prefix=prefix)
            objects = [item['Key'] for item in response['Contents']]
        except KeyError:
            objects = list()
        return objects
    
    def load_object(self, path:str):
        bucket=self.bucket
        try:
            with NamedTemporaryFile() as f:
                self.s3.download_file(bucket, path, f.name)
                if path.endswith('.pkl'):
                    obj = pd.read_pickle(f.name)
                elif path.endswith('.csv'):
                    obj = pd.read_csv(f.name)
            return obj
        except Exception as e:
            return None
    
    def upload_object(self, obj, path:str):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        bucket = self.bucket
        with NamedTemporaryFile() as tmp:
            try:
                if isinstance(obj, pd.DataFrame):
                    obj.to_pickle(tmp.name)
                    suffix = '.pkl' if not path.endswith('.pkl') else ''
                
                object_path = path + suffix
                self.s3.upload_file(tmp.name, bucket, object_path)
            except Exception as e:
                print(e)
                return False
            return object_path
        
    def delete_objects(self, prefix=''):
        bucket = self.bucket
        bucket = self.s3_resource.Bucket(bucket)
        return bucket.objects.filter(Prefix=prefix).delete()