# Diabetic-Retinopathy-Detection

You are provided with a large set of retina images taken using fundus photography under a variety of imaging conditions.
A clinician has rated each image for the severity of diabetic retinopathy on a scale of 0 to 4:

* 0 - No DR
* 1 - Mild
* 2 - Moderate
* 3 - Severe
* 4 - Proliferative DR 

Images in the Dataset are of different sizes. Some of them are out of focus, underexposed, or overexposed. 

## Workflow
1. Resize Images: We will resize both the training and test images to 224x224, so that it matches the ImageNet format.
2. Model: We will use a DenseNet-121 pre-trained on ImageNet. We will finetune it using Adam for 15 epochs, and evaluate it on an unseen   validation set.
3. Quadratic Weighted Kappa: QWK also known as Cohen's Kappa. We will use a custom callback to monitor the score.
4. Training and Evaluation : We take a look at the change in loss and QWK score through the epochs.
5. Web app : We build a python app using flask to deploy our keras model as Web App.

## Libraries Used
* Flask
* gevent
* Werkzeug
* Numpy
* Pandas
* PIL
* OpenCV
* Matplotlib
* Keras
* Tensorflow
