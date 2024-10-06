from orkestr8.clients.data_lake_client import DataLakeClient
import os

AWS_BUCKET_NAME = os.environ['AWS_BUCKET_NAME']
PROJECT_LOCATION = os.environ['PROJECT_LOCATION']

def run():
    """Pulls down data from repo"""
    DataLakeClient("s3",AWS_BUCKET_NAME)