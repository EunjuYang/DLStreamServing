from dlcep import StreamDLStub
from dlcep import IncStreamDLStub
from onlinedl import ContinualDL
from onlinedl import IncrementalDL
import numpy as np


kafka_broker = "143.248.146.115:9092,143.248.146.116:9092,143.248.146.117:9092"
cep_id = "CEP_ch"
stream_bk = "143.248.146.115"
batch_size = 5
_dtype = np.float32

model_path = "path/to/model" # the model should be stored by using model.save() of Sequential model in Keras.
num_ami = 10

'''
ContinualDL should get id information from stream_generator
'''
stream_stub = StreamDLStub(kafka_bk=kafka_broker, cep_id=cep_id, stream_bk=stream_bk, batch_size=batch_size, dtype=_dtype)
online_dl = ContinualDL(model_path, num_ami=num_ami, mem_method='cossim')
stream_generator = stream_stub.batch_train_generator()
while True:
    x_batch, y_batch, id_batch = next(stream_generator)
    online_dl.compare_consume(x_batch, y_batch, id_batch) # compare_consume is a proposed method. consume is a basic continual method.
    online_dl.save()


'''
IncrementalDL is different from ContinualDL
because it transfers the result, beta and beta1, of model.profile() to StreamDLStub
and 
'''
Incre_trainer = IncrementalDL(model_path)
beta, beta1 = Incre_trainer.profile()

Incre_stream_stub = IncStreamDLStub(kafka_bk=kafka_broker, cep_id=cep_id, stream_bk=stream_bk, batch_size=batch_size, dtype=_dtype)
Incre_stream_stub.set_beta_for_incremental(beta, beta1)

test_error = 0.3 # We just followed the value in PhD Kim's source code.
while True:
    # Don't use next(generator) because we should pass test_error to calculate batch_size and epoch.
    x_batch, y_batch, scailed_epoch = Incre_stream_stub.batch_train_generator(test_error)
    test_error = Incre_trainer.consume(x_batch, y_batch, scailed_epoch)
