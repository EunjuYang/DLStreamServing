"""
This file is not yet completed.
It only contains prototype codes.
"""
import os

from onlinedl.onlinedl import *
from stream_dl_api.dlcep import *

# This is main code for TEST
if __name__ == '__main__':

    # TODO - set parameters
    model_name = os.environ['MODEL_NAME']
    online_method = os.environ['ONLINE_METHOD']
    framework = os.environ['FRAMEWORK'] # 현재 keras 만 사용중
    save_weights = bool(os.environ['SAVEWEIGHT'])
    if online_method == 'cont':
        mem_method = os.environ['MEM_METHOD'] # ringbuffer or cossim
        num_ami = int(os.environ['NUM_AMI']) # There is no default value. So it is required.
        episodic_mem_size = int(os.environ['EPISODIC_MEM_SIZE'])
        if mem_method == 'cossim':
            is_schedule = bool(os.environ['IS_SCHEDULE'])
        else:
            is_schedule = False
    model_repo_addr = os.environ['MODEL_REPO_ADDR']

    cep_id = os.environ['CEP_ID']
    kafka_bk = os.environ['KAFKA_BK']
    stream_bk = os.environ['STREAM_BK']
    batch_size = os.environ['BATCH_SIZE']
    _dtype = os.environ['DTYPE']
    is_adaptive = bool(os.environ['IS_ADAPTIVE']) # optional for ContinualDL, Not used for Incremental

    if online_method == 'inc':
        trainer = IncrementalDL(model_name=model_name,
                                online_method=online_method,
                                framework=framework,
                                repo_addr=model_repo_addr)
        beta, beta1 = trainer.profile()
        strstub = IncStreamDLStub(kafka_bk=kafka_bk,
                               cep_id=cep_id,
                               stream_bk=stream_bk,
                               batch_size=batch_size,
                               dtype=_dtype,
                               adaptive_batch_mode=True) # always adaptive
        strstub.set_beta_for_incremental(beta, beta1)
        test_error = 0.3 # from seong-hwan's origin code.
        while True:
            x_batch, y_batch, scailed_epoch = strstub.batch_train_generator(test_error)
            test_error = trainer.consume(x_batch, y_batch, scailed_epoch)
            if save_weights:
                trainer.save()

    elif online_method == 'cont':
        trainer = ContinualDL(model_name=model_name,
                              online_method=online_method,
                              framework=framework,
                              mem_method=mem_method,
                              num_ami=num_ami,
                              episodic_mem_size=episodic_mem_size,
                              is_schedule=is_schedule,
                              repo_addr=model_repo_addr)
        strstub = StreamDLStub(kafka_bk=kafka_bk,
                               cep_id=cep_id,
                               stream_bk=stream_bk,
                               batch_size=batch_size,
                               dtype=_dtype,
                               adaptive_batch_mode=is_adaptive)
        stream_generator = strstub.batch_train_generator()
        while True:
            _, x_batch, y_batch, id_batch = next(stream_generator)
            trainer.consume(x_batch, y_batch, id_batch)
            if save_weights:
                trainer.save()

    else:
        raise ValueError('ONLINE_METHOD value is wrong. (only support "inc" and "cont")')