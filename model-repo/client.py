from modelrepo.lib import *
import os


if __name__ == '__main__':

    client = Client('localhost:8888')
    in_file_name = '/tmp/uploaded_file'
    out_file_name = '/tmp/downloaded_file'

    # demo for file uploading
    client.upload_model('/tmp/uploaded_file', "hello_model")
    client.download_model("hello_model", "/tmp/downloaded_file")

    os.system('sha1sum %s'%in_file_name)
    os.system('sha1sum %s'%out_file_name)