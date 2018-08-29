# Deep Learning

## How to install and configure the GPU inside personal laptot

*Source* : https://medium.com/@lmoroney_40129/installing-tensorflow-with-gpu-on-windows-10-3309fec55a00

Theis installation is mada for TensorFlow but after installed, GPU and CUDA are detected for other frameworks like PyTorch. Here are some remarks about this installation :

1. Install CUDA v9.0 : don't install the *default installation*, the *only CUDA* option is sufficent

2. Set the path to CUDA Toolkit. It could be done within the system environment variables, or directly in the prompt line :

```sh
set PATH=%PATH%;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\bin
```
3. To test the installation inside TensorFlow :

```python
from tensorflow.python.client import device_lib

def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']
```

## Objectifs


*	Quels objectifs pour ce projet : 
    *	Sur des images qui viennent probablement des réseaux sociaux, détecter : 
        *	Ce qu’il y a dans l’image (objet detection & classification)
        *	Des logos 
        *	Des émotions
    *	Peut être d’autres cas d’usage
    *	Se rappeler d’aller à l’essentiel et de toujours prendre des modèles pré entrainés

*	Todo d’apprentissage 
    *	Top-down : 
        *	https://eu.udacity.com/course/deep-learning--ud730 
        *	http://www.fast.ai/  et http://course.fast.ai/
        *	Siraj Raval channel https://www.youtube.com/channel/UCWN3xxRkmTPmbKwht9FuE5A 
    *	Bottom-up : 
        *	http://cs231n.github.io/ 
        *	https://fr.coursera.org/specializations/deep-learning 

*	Liens en vrac 
    *	OpenCV : 
        *	https://pythonprogramming.net/loading-images-python-opencv-tutorial/ 
        *	Documentation officielle d’OpenCV https://docs.opencv.org/2.4/doc/tutorials 
    *	Outils / librairie 
        *	Keras + Tensorflow (Google)
        *	Pytorch (Facebook) + fastai (Fast.ai)
        *	Autres (mais moins intéressante pour nous) : CNTK (Microsoft), Caffe2 (Facebook), MXNET (Amazon), Paddle (Baidu)

*	Quel hardware ? 
    *	Soit sur ton ordi / CPU, lent mais toujours une possibilité
    *	GPU sur le cloud https://www.paperspace.com/ https://www.floydhub.com/ 
    *	GPU gratuit sur Kaggle / Colab https://colab.research.google.com/ 

## Résultats

En mêlant reconnaissance faciale et scrapping (du site de la FIFA et de twitter), on peut obtenir ce genre de résultat

![Giroud-Griezmann](https://image.ibb.co/gLGwPy/Giroud_Griezmann.jpg)

![Messi](https://image.ibb.co/gnFvHJ/test3.jpg)

![Giroud-Lloris](https://image.ibb.co/cSxsxJ/test.jpg)