# Deep Learning

## Objectifs

*	Quels objectifs pour ce projet : 
    *	Sur des images qui viennent probablement des réseaux sociaux, détecter : 
        *	Ce qu’il y a dans l’image (objet detection & classification)
        *	Des logos 
        *	Des émotions
    *	Peut être d’autres cas d’usage
    *	Se rappeler d’aller à l’essentiel et de toujours prendre des modèles pré entrainés

## Apprentissage


*	Top-down : 
    *	https://eu.udacity.com/course/deep-learning--ud730 
    *	http://www.fast.ai/  et http://course.fast.ai/
    *	Siraj Raval channel https://www.youtube.com/channel/UCWN3xxRkmTPmbKwht9FuE5A 
*	Bottom-up : 
    *	http://cs231n.github.io/ 
    *	https://fr.coursera.org/specializations/deep-learning 

## Librairies

### Open CV

Documentation officielle d’OpenCV https://docs.opencv.org/2.4/doc/tutorials 

### Deep Learning


* Keras + Tensorflow (Google)

<img src="https://blog.keras.io/img/keras-tensorflow-logo.jpg" width="200"/>

*	Pytorch (Facebook) + fastai (Fast.ai)

<img src="https://pytorch.org/static/img/logos/pytorch-logo-dark.png" width="200"/>

*	Autres (mais moins intéressante pour nous) : CNTK (Microsoft), Caffe2 (Facebook), MXNET (Amazon), Paddle (Baidu)

<img src="https://d1.awsstatic.com/Test%20Images/Kate%20Test%20Images/600x400_Caffe2_Logo.2ccdff2b2fa4883ff845e556cccf1b4baacca547.png" width="200"/>

## Hardware

*	Soit sur ton ordi / CPU, lent mais toujours une possibilité
*	GPU sur le cloud https://www.paperspace.com/ https://www.floydhub.com/ 
*	GPU gratuit sur Kaggle / Colab https://colab.research.google.com/ 

**Comment installer et configurer le GPU de son PC portable (avec CUDA) ?**

<img src="https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Nvidia_CUDA_Logo.jpg/300px-Nvidia_CUDA_Logo.jpg" width="200"/>

*Source* : https://medium.com/@lmoroney_40129/installing-tensorflow-with-gpu-on-windows-10-3309fec55a00

L'installation proposée par ce tutoriel est destinée à TensorFlow, mais après avoir été installé, le GPU et CUDA sont bien détectés par d'autres framework comme PyTorch. Quelques remarques :

1. Il faut install CUDA **v9.0**, et au moment de l'installation, il suffit de choisir l'option  *only CUDA* (pas besoin de *default installation*)

2. Il faut ajouter le path vers le CUDA Toolking aux variables d'environnement :

```sh
set PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin
```

3. Pour tester l'installation dans TensorFlow:

```python
from tensorflow.python.client import device_lib

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']
```