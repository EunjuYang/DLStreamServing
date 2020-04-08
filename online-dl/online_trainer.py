"""
This file is not yet completed.
It only contains prototype codes.
"""
from onlinedl.onlinedl import *
from stream_dl_api.dlcep import StreamDLStub

# This is main code for TEST
if __name__ == '__main__':

    # TODO - set parameters
    model_name = os.environ['MODEL_NAME']
    num_ami = int(os.environ['NUM_AMI'])
    cep_id = os.environ['CEP_ID']
    kafka_bk = os.environ['KAFKA_BK']
    stream_bk = os.environ['STREAM_BK']
    batch_size = os.environ['BATCH_SIZE']
    _dtype = os.environ['DTYPE']
    mem_method = os.environ['MEM_METHOD']

    #TODO
    trainer = ContinualDL(model_name, num_ami=num_ami, mem_method=mem_method)
    strstub = StreamDLStub(kafka_bk=kafka_bk,
                           cep_id=cep_id,
                           stream_bk=stream_bk,
                           batch_size=batch_size,
                           dtype=_dtype,
                           adaptive_batch_mode=True)
    stream_generator = strstub.batch_train_generator()


    while True:
        batch_size, x_batch, y_batch, ami_idx = next(stream_generator)
        trainer.consume(x_batch, y_batch, ami_idx)
        trainer.save()
