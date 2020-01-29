# Stream-DL API

To support inference with stream data, we provide client side api. 
This library is used after the deep learning model is deployed.

### How to use the API

```python

from dlcep import StreamDLstub
import numpy as np


kafka broker = "{KAFKA_IP0}:{PortNum},{KAFKA_IP1}:{PortNum}"
cep_id = "ami_prediction_cep_0"
stream_bk = "{STREAM_BROKER_IP}:{PortNum}"
batch_size = 5
_dtype = np.float32

# lb_size = 4
# lf_size = 1
# is_train = True

stream_stub = StreamDLStub(kafka_bk = kafka_broker, cep_id = cep_id, stream_bk = stream_bk, batch_size = batch_size, dtype = _dtype)
stream_generator = stream_stub.batch_train_generator()

while True:

    x_batch, y_batch = next(stream_generator)
    # inference with (x_batch)
    # online train with (y_batch)

```

