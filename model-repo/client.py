from modelrepo.lib import *
import os


if __name__ == '__main__':

    client = Client('localhost:8888')

    # demo for file uploading
    in_file_name = '/tmp/large_file_in'
    client.upload(in_file_name, '/tmp/uploaded_file')

    # demo for file downloading:
    out_file_name = '/tmp/large_file_out'
    if os.path.exists(out_file_name):
        os.remove(out_file_name)
    client.download('/tmp/uploaded_file', out_file_name)
    os.system('sha1sum %s'%in_file_name)
    os.system('sha1sum %s'%out_file_name)