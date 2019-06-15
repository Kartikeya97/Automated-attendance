import os, sys
sys.path.append(os.path.abspath(__file__))

import numpy as np
from keras.models import model_from_yaml
from keras.preprocessing.image import ImageDataGenerator

from FaceDetector import *


class FacePredictor:

    def __init__(self):
        # Inintializing path for saving face frames 
        self.face_img_saving_path = "Dataset/TestingDataset/Unknown/"
        
        # Creating object of Face Detector
        self.FD = FaceDetector()
        
        # Initializing paths for 'test images dataset'
        self.test_path = "Dataset/TestingDataset/"        
        # Initializing path for the test dataset images
        self.unknown_img_path = self.test_path + "Unknown/"
                
        # Loading 'YAML' and 'creating model'
        yaml_file = open('TrainedEntities/custom_vgg16_model.yaml', 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        self.predictor_model = model_from_yaml(loaded_model_yaml)

        # Loading 'weights' into the newly created model
        self.predictor_model.load_weights("TrainedEntities/custom_vgg16_model_weights.h5")
        print("Loaded model from disk")    
             
    
    
    def ParameterPreparation(self):
        # Preparing test image batches
        self.test_batches = ImageDataGenerator().flow_from_directory(self.test_path, target_size=(224,224), classes=None, batch_size=10)
        # Finding number of testing images
        self.no_of_images = len(os.listdir(self.unknown_img_path))
           
    
    def TestFaceDatsetDeletor(self):        
        # Deleting the test dataset images
        for file in os.listdir(self.unknown_img_path):
            if(file.split('.')[-1] == "jpg"):
                os.remove(os.path.join(self.unknown_img_path, file))            
                
                
    def Predictor(self, test_image):
        self.test_image = test_image
        # Saving faces found in the image
        self.FD.Detector(test_image, (self.face_img_saving_path + "User_"), 200, 1)        
        
        # Prepares the parameters for face prediction
        self.ParameterPreparation()
        
        # Predicting Ids of Dataset
        predictions = self.predictor_model.predict_generator(self.test_batches, steps=int(self.no_of_images/10)+1, verbose=0)
        
        # Extracting Ids from predictions
        Ids = []
        for i in range(0,len(predictions)):
            temp = np.where(predictions[i] == np.amax(predictions[i]))
            Ids.append(int(temp[0][0]))
        
        
        # Deleting the dataset formed for testing images
        self.TestFaceDatsetDeletor()
        
        return Ids
        
    
        
