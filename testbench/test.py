from dlcep import StreamDLstub
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

stream_stub = StreamDLStub(kafka_bk=kafka_broker, cep_id=cep_id, stream_bk=stream_bk, batch_size=batch_size, dtype=_dtype)
stream_generator = stream_stub.batch_train_generator()
online_dl = ContinualDL(model_path, num_ami=num_ami, mem_method='cossim')

# IncrementalDL is different against ContinualDL
# because it transfers the result of model.profile() to StreamDLStub
online_dl = IncrementalDL(model_path)
beta, beta1 = online_dl.profile()
stream_generator = stream_stub.batch_interaction_train_generator(beta, beta1)

while True:
    x_batch, y_batch, id_batch = next(stream_generator)
    online_dl.compare_consume(x_batch, y_batch, id_batch) # compare_consume is a proposed method. consume is a basic continual method.
    online_dl.save()
