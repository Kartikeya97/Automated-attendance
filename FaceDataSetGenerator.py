import os, sys
sys.path.append(os.path.abspath(__file__))

from FaceDetector import *


class FaceDataSetGenerator:
    pass

    def __init__(self):
        # Creating objects of Face Detector for training and validation images
        self.FD1 = FaceDetector()
        self.FD2 = FaceDetector()
        
        # Setting path for 'training' and 'validation' images
        self.training_img_path = "Dataset/TrainingDataSet/TrainingImages/"
        self.validation_img_path = "Dataset/TrainingDataSet/ValidationImages/"
    

    def GetUID(self):
        # Inputting User ID
        self.U_ID = input("Enter User ID: ")


    def SetPath(self):
        # Setting path for 'training' and 'validation' images according to User ID
        self.training_img_path = self.training_img_path + str(self.U_ID) + "/"
        self.validation_img_path = self.validation_img_path + str(self.U_ID) + "/"
        
        # Creating U_ID directory for 'training' and 'validation' images if not present
        if not os.path.exists(self.training_img_path):
            os.makedirs(self.training_img_path)
        if not os.path.exists(self.validation_img_path):
            os.makedirs(self.validation_img_path)


    def GenerateDataset(self):
        # Getting Id of the user
        self.GetUID()
        # Setting paths for saving the captured frames
        self.SetPath()

        # Detecting faces and saving for future predictions
        test_image = ""
        u_id = "User_" + self.U_ID + "_"
        self.FD1.Detector(test_image, (self.training_img_path + u_id), 100, 0)
        self.FD2.Detector(test_image, (self.validation_img_path + u_id), 50, 1)
        
        
        
def main():
    # Creating object of the class
    DG = FaceDataSetGenerator()

    # Detecting the faces in the frame
    DG.GenerateDataset()


if __name__ == "__main__":
    main()