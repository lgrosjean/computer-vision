# Face Recognition

Recognize and manipulate faces from Python or from the command line with the world's simplest face recognition library. Everything comes from this incredible GitHub repo : https://github.com/ageitgey/face_recognition

## Installation

Requirements 

* Windows
	* Anaconda

To install on Anaconda (information from http://github.com/ageitgey/face_recognition/issues/89) :
```
pip install --no-dependencies face_recognition face_recognition_models
conda install -c conda-forge dlib
```

I ran into issues with Pillow when importing the `face_recognition` package. I needed to downgrad Pillow :
```
conda install Pillow==4.0.0
```
