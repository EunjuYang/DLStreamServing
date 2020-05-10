from modelrepo.lib import *
import os
from datetime import datetime


if __name__ == '__main__':

    client = Client('localhost:8888')
    in_file_name = '/tmp/uploaded_file'
    out_file_name = '/tmp/downloaded_file'
    model_name = 'hello-model'
    loss = 1.0

    # demo for file uploading
    client.upload_model(in_file_name, model_name, loss)
    client.download_model(model_name, out_file_name)

    os.system('sha1sum %s'%in_file_name)
    os.system('sha1sum %s'%out_file_name)

    response = client.get_model_info(model_name)
    print(response)
    print(datetime.fromtimestamp(float(response.update_time)).strftime('%Y-%m-%d %H:%M'))