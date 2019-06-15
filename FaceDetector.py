import time
import imutils
import cv2
import numpy as np
from imutils.video import VideoStream

class FaceDetector:
    
    def __init__(self):
        # Initializing paths for 'prototxt', 'model', 'test and 'confidence'
        prototxt_path = "TrainingEntities/deploy.prototxt"
        model_path = "TrainingEntities/res10_300x300_ssd_iter_140000.caffemodel"
        self.threshold_confidence = 0.5
        
        # Starting 'WebCam'
        self.vCap = VideoStream(src=0).start()
        time.sleep(1.0)
        
        # Loading 'Serialized Model' from Disk
        self.recognizer_modal = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
        
        
    def Detector(self, test_image, img_saving_path, no_of_images, flag):  
        sampleIndex = 0

        # Loop over the 'Frames' from the 'Video Stream'
        while True:
            if(test_image == ""):
                # Reading returned 'captured frame image'
                capturedFrame = self.vCap.read()
            else:
                capturedFrame = cv2.imread(test_image)
            
            # Resizing the 'captured frame image'
            newFrame = imutils.resize(capturedFrame, width=700)
            
            # Calculating 'mean RGB' values for Captured frame
            a, b, c = np.mean(newFrame, axis=(0, 1))
            a = int(a) * 1.0
            b = int(b) * 1.0
            c = int(c) * 1.0
            
            # Grabbing the 'Frame Dimensions'
            (h, w) = newFrame.shape[:2]
            
            # Converting the image frame into a 'Blob'
            blob = cv2.dnn.blobFromImage(cv2.resize(newFrame, (300, 300)), 1.0, (300, 300), (a, b, c))

            # Pass the 'Blob' through the network and obtain the 'Detections' and 'Predictions'
            self.recognizer_modal.setInput(blob)
            detections = self.recognizer_modal.forward()

            # Looping over all the 'Detections'
            for i in range(0, detections.shape[2]):
                # Extracting the 'confidence' (i.e., probability) associated with the prediction
                confidence = detections[0, 0, i, 2]

                # Filtering out weak detections by ensuring 'confidence' to be greater than the minimum confidence
                if confidence < self.threshold_confidence:
                    continue

                # Computing the (X, Y)-coordinates of the Bounding Box for the Object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Calclating the Face Outlining parameters in the frame
                confidencePercentage = "{:.2f}%".format(confidence * 100)
                if ((startY - 10) > 10):
                    y = startY - 10
                else:
                    y = startY + 10
                    
                if (flag == 1):
                    if (startX > 0 and startY > 0):
                        if (endX < 700 and endY < 525):
                            # Extracting the face from the Captured frame
                            faceFrame = newFrame[startY:endY, startX:endX];
                            # Resizing the Face frame
                            faceFrame = cv2.resize(faceFrame, (224, 224))
                            # Saving the extracted face
                            cv2.imwrite(img_saving_path + str(sampleIndex) + ".jpg", faceFrame)
                            sampleIndex += 1
                        
                # Draw the Bounding Box of the face along with the Associated Probability
                cv2.rectangle(newFrame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.putText(newFrame, confidencePercentage, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)


            # Showing the captured frame image
            cv2.imshow("Frame", newFrame)                       

            # Checking if any key was pressed
            keyPressed = cv2.waitKey(1)
            # Checking if sufficient images have been saved or else any interruption has been raised
            if(sampleIndex == no_of_images and flag == 1):
                break
            elif(keyPressed == ord("s") or keyPressed == ord("S")):
                sampleIndex = 0
                flag = 1
            elif(keyPressed == ord("q") or keyPressed == ord("Q")):
                break

        # Exiting Camera
        self.vCap.stop()
        # Destroying All Windows
        cv2.destroyAllWindows()