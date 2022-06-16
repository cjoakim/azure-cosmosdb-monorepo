"""
Usage:
    python storage-client.py display_env
    python storage-client.py create_upload_list
    python storage-client.py create_container documents
    python storage-client.py upload_files 0
    python storage-client.py upload_files 99
    python storage-client.py list_blobs books
    python storage-client.py delete_container documents
    python storage-client.py download_blob UPSWEB-800x533.jpg
"""

__author__  = 'Chris Joakim'
__email__   = "chjoakim@microsoft.com"
__license__ = "MIT"
__version__ = "November 2021"


import os
import sys

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from azure.core.exceptions import ResourceExistsError
from azure.core.exceptions import ResourceNotFoundError

from docopt import docopt

from base import BaseClass


class StorageClient(BaseClass):
    """
    This class is executed from the command line to upload documents to Azure Storage
    for indexing by Azure Cognitive Search.  It also creates the list of files to be
    uploaded.  Additionally, it has logic to created and delete storage containers,
    and download blobs.
    """

    def __init__(self):
        BaseClass.__init__(self)
        self.uploads_list_filename = 'data/uploads_list.json'
        self.blob_svc_client = BlobServiceClient.from_connection_string(self.stor_acct_conn_str)

    def display_env(self):
        print('stor_acct_name:      {}'.format(self.stor_acct_name))
        print('stor_acct_key:       {}'.format(self.stor_acct_key))
        print('stor_acct_conn_str:  {}'.format(self.stor_acct_conn_str))
        print('blob_container:      {}'.format(self.blob_container))

    def create_upload_list(self):
        filenames = self.gather_upload_filenames()
        self.write_json_file(filenames, self.uploads_list_filename)

    def upload_files(self, max_count):
        print('upload_files, max_count: {}'.format(max_count))
        filenames = self.load_json_file(self.uploads_list_filename)
        print('upload_files list loaded, count: {}'.format(len(filenames)))

        for idx, fq_name in enumerate(filenames):
            if idx < max_count:
                basename = os.path.basename(fq_name)
                print('uploading file {}: {} => {} {}'.format(
                    idx + 1, fq_name, self.blob_container, basename))
                self.upload_blob(fq_name, self.blob_container, basename)

    def upload_blob(self, local_file_path, cname, blob_name):
        try:
            blob_client = self.blob_svc_client.get_blob_client(container=cname, blob=blob_name)
            print('uploading blob: {} -> {} {}'.format(local_file_path, cname, blob_name))
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data)
            print('uploaded blob:  {} -> {} {}'.format(local_file_path, cname, blob_name))
        except ResourceExistsError as err:
            print("ResourceExistsError: {}".format(e))
        except Exception as e:
            print("Exception: {}".format(e))

    def download_blob(self, blob_name):
        local_file_path = 'tmp/{}'.format(blobname)
        try:
            blob_client = self.blob_svc_client.get_blob_client(
                container=self.blob_container, blob=blob_name)
            print('downloading blob: {}'.format(blob_name))
            with open(local_file_path, "wb") as downloaded_blob:
                blob_data = blob_client.download_blob()
                blob_data.readinto(downloaded_blob)
            print('downloading blob: {}'.format(local_file_path))
        except ResourceExistsError as err:
            print("ResourceExistsError: {}".format(e))
        except Exception as e:
            print("Exception: {}".format(e))

    def list_blobs(self, cname, print_each=True):
        print('list_blobs in container: {}'.format(cname))
        blobs = self.list_container(cname)
        for blob in blobs:
            if print_each:
                print('blob: {}  {}  {}'.format(blob.name, blob.size, blob.last_modified))
        return blobs

    # private methods below

    def gather_upload_filenames(self):
        cwd = os.getcwd()
        print(cwd)
        documents_dir = '{}/documents'.format(cwd)
        print(documents_dir)

        filenames = list() 
        for root, dirs, files in os.walk(documents_dir, topdown=False):
            for name in files:
                if not name.startswith('.'):
                    if len(name) > 7:
                        fq_name = os.path.join(root, name)
                        filenames.append(fq_name)
        return sorted(filenames)

    def create_container(self, cname):
        try:
            container_client = self.blob_svc_client.get_container_client(cname)
            container_client.create_container()
            print('created container: {}'.format(cname))
        except ResourceExistsError as err:
            print('container exists: {}'.format(cname))
        except Exception as e:
            print("Exception: {}".format(e))

    def delete_container(self, cname):
        try:
            container_client = self.blob_svc_client.get_container_client(cname)
            container_client.delete_container()
            print('deleted container: {}'.format(cname))
        except ResourceNotFoundError:
            print('container not found: {}'.format(cname))

    def list_container(self, cname):
        # return a list of 'azure.storage.blob._models.BlobProperties' objects
        try:
            return self.container_client(cname).list_blobs()
        except Exception as e:
            print("Exception: {}".format(e))
            return list()

    def container_client(self, cname):
        return self.blob_svc_client.get_container_client(cname)


def print_options(msg):
    print(msg)
    arguments = docopt(__doc__, version=__version__)
    print(arguments)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        func = sys.argv[1].lower()
        print('func: {}'.format(func))
        client = StorageClient()

        if func == 'display_env':
            client.display_env()

        elif func == 'create_upload_list':
            client.create_upload_list()

        elif func == 'upload_files':
            max_count = int(sys.argv[2])
            client.upload_files(max_count)
            
        elif func == 'list_blobs':
            cname = sys.argv[2]
            client.list_blobs(cname)

        elif func == 'create_container':
            cname = sys.argv[2]
            client.create_container(cname)

        elif func == 'delete_container':
            cname = sys.argv[2]
            client.delete_container(cname)

        elif func == 'download_blob':
            blobname = sys.argv[2]
            client.download_blob(blobname)
            
        else:
            print_options('Error: invalid function: {}'.format(func))
    else:
        print_options('Error: no function argument provided.')
