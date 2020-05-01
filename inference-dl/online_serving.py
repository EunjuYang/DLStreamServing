"""
This file is not yet completed.
It only contains prototype codes.
"""
import os

from onlinedl.onlinedl import *
from stream_dl_api.dlcep import *

if __name__ == '__main__':

    model_name = os.environ['MODEL_NAME']
    model_repo_addr = os.environ['MODEL_REPO_ADDR']

    cep_id = os.environ['CEP_ID']
    kafka_bk = os.environ['KAFKA_BK']
    stream_bk = os.environ['STREAM_BK']
    is_adaptive = bool(os.environ['IS_ADAPTIVE'])
    batch_size = int(os.environ['BATCH_SIZE'])
    _dtype = os.environ['DTYPE']

    # Not yet determine to make InferenceDL
    inferencer = InferenceDL(model_name=model_name,
                             repo_addr=model_repo_addr)
    strstub = StreamDLStub(kafka_bk=kafka_bk,
                           cep_id=cep_id,
                           stream_bk=stream_bk,
                           batch_size=batch_size,
                           dtype=_dtype,
                           adaptive_batch_mode=is_adaptive)
    stream_generator = strstub.batch_train_generator()
    while True:
        _, x_batch, y_batch, _ = next(stream_generator)
        inferencer.consume(x_batch, y_batch)
