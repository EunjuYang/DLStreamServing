<<<<<<< HEAD
# Online-DL API
To support the function of online deep learning with using common deep learning library, we provide an online-dl wrapper api.
### Dependency
=======
#Online-DL API
To support the function of online deep learning with using common deep learning library, we provide an online-dl wrapper api.
###Dependency
>>>>>>> origin/master
* Python >= 3.6
* Tensorflow >= 2.1.x
* quadprog >= 0.1.7
* numpy
* scikit-learn >= 0.22.2
<<<<<<< HEAD
### Main Description of Online-DL API
=======
###Main Description of Online-DL API
>>>>>>> origin/master
* OnlinDL : containing common init function and save model parameter function
* ContinualDL : continual OnlineDL
  * consume : original continual learning
  * compare_consume : continual learning with proposed scheduling method by changha lee
* inMemory : ring-buffer for continual learning
* cossimMemory : cosine similarity based buffer
  