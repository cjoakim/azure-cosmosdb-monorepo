__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "May 2022"

import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from azure.core.exceptions import ResourceExistsError
from azure.core.exceptions import ResourceNotFoundError

# https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
# https://github.com/Azure/azure-sdk-for-python/blob/azure-storage-blob_12.11.0/sdk/storage/azure-storage-blob/samples/blob_samples_service.py

class Storage(object):

    def __init__(self):
        # acct_name = os.environ['AZURE_SWIFT_DG_STOR_ACCOUNT']
        # acct_key  = os.environ['AZURE_SWIFT_DG_STOR_KEY']
        acct_name = os.environ['AZURE_STORAGE_ACCOUNT']
        acct_key  = os.environ['AZURE_STORAGE_KEY']
        acct_url  = 'https://{}.blob.core.windows.net/'.format(acct_name)
        print('acct_name: {}'.format(acct_name))
        print('acct_key:  {}'.format(acct_key))
        print('acct_url:  {}'.format(acct_url))

        self.blob_service_client = BlobServiceClient(
            account_url=acct_url, credential=acct_key)

    def account_info(self):
        return self.blob_service_client.get_account_information()

    def list_containers(self):
        clist = list()
        try:
            containers = self.blob_service_client.list_containers(include_metadata=True)
            for container in containers:
                clist.append(container)
                #print('container: ' + str(container))
            return clist
        except ResourceExistsError:
            return clist

    def create_container(self, cname):
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.create_container()
            print('create_container: {}'.format(cname))
        except ResourceExistsError:
            pass

    def delete_container(self, cname):
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            container_client.delete_container()
            print('delete_container: {}'.format(cname))
        except ResourceNotFoundError:
            pass

    def list_container(self, cname):
        try:
            container_client = self.blob_service_client.get_container_client(cname)
            return container_client.list_blobs()
        except ResourceExistsError:
            return list()

    def upload_blob(self, local_file_path, cname, blob_name, overwrite=True):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=overwrite)
            print('upload_blob: {} -> {} {}'.format(local_file_path, cname, blob_name))
            return True
        except ResourceNotFoundError:
            return False

    def download_blob(self, cname, blob_name, local_file_path):
        try:
            blob_client = self.blob_service_client.get_blob_client(container=cname, blob=blob_name)
            with open(local_file_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            print('download_blob: {} {} -> {}'.format(cname, blob_name, local_file_path))
        except ResourceNotFoundError:
            pass

    def connection_string(self):
        name = 'AZURE_SWIFT_DG_STOR_CONN_STRING'
        return os.environ[name]
