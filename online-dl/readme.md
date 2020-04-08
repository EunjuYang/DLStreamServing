# Online-DL
To support the function of online deep learning with using common deep learning library, we provide an online-dl module.
Online-DL instance will be launched when serving container is deployed.

## Dependency
* Python >= 3.6
* Tensorflow >= 2.1.x
* quadprog >= 0.1.7
* numpy
* scikit-learn >= 0.22.2

## Main Description of Online-DL 


#### Mode of Online Deep Learning
* ContinualDL : continual OnlineDL
  * consume : original continual learning
  * compare_consume : continual learning with proposed scheduling method by changha lee
* IncrementalDL

#### Continual DL

##### 1) Memory option
* inMemory : ring-buffer for continual learning
* cossimMemory : cosine similarity based buffer
  * insert : without proposed method by changha lee
  * compare_insert with proposed method by changha lee
  
##### 2) Continual DL Method
