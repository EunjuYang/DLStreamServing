"""
This file is not yet completed.
It only contains prototype codes.
"""
import os

from inferencedl.inferencedl import *
from stream_dl_api.dlcep import *

if __name__ == '__main__':

    model_name = os.environ['MODEL_NAME']
    model_repo_addr = os.environ['MODEL_REPO_ADDR']
    mongo_result_addr = os.environ['RESULT_ADDR']

    cep_id = os.environ['CEP_ID']
    kafka_bk = os.environ['KAFKA_BK']
    stream_bk = os.environ['STREAM_BK']
    batch_size = int(float(os.environ['BATCH_SIZE']))
    _dtype = os.environ['DTYPE']
    lb_size = int(os.environ['LB_SIZE'])
    lf_size = None
    prefix = os.environ['PREFIX']

    # Not yet determine to make InferenceDL
    inferencer = InferenceDL(model_name=model_name,
                             repo_addr=model_repo_addr,
                             result_addr=mongo_result_addr)
    strstub = StreamDLStub(kafka_bk=kafka_bk,
                           cep_id=cep_id,
                           stream_bk=stream_bk,
                           batch_size=batch_size,
                           is_train=False,
                           dtype=_dtype,
                           lb_size=lb_size,
                           lf_size=lf_size,
                           prefix=prefix)
    stream_generator = strstub.batch_generator()
    while True:
        # you need to add id information and parse it and submit it into mongodb
        _, x_batch, id_batch = next(stream_generator)
        inferencer.consume(x_batch, id_batch)
