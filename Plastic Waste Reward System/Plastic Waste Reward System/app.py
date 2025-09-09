import random
import rewardpage
from rewardpage import *
import database
from database import *

run_app()

import Arduion_Py_Connection
from Arduion_Py_Connection import *
import cv2_plastic
from cv2_plastic import *

while(1):
    print("\nWaiting to receive Signal from Arduino to turn ON Webcam")
    received_data = Data_Received_From_Arduino_Wait()
    print(f"Received from Arduino: {received_data}")

    if received_data == "Turn_ON_Camera":
        print("Turn_ON_Camera")
        Load_Camera()
        Data_Send_To_Arduino('CAMERA_ON') # Completed

        material_type = Load_ML_Algorithim_Wait()
        if material_type == "Plastic":
            # Once Camera ON Success
            Data_Send_To_Arduino('Plastic') # Completed
        else:
            Data_Send_To_Arduino('Non-Plastic') # Completed

        print("Waiting to receive Signal from Arduino")
        received_data = Data_Received_From_Arduino_Wait()
        print(f"Received from Arduino: {received_data}")

        
        if received_data == "Thanks": # Non-Plastic
            print("Non-Plastic detected")
            
        else: # Plastic
            print("Mobile No. storing into Server")
            database_main(received_data)
            print("Mobile No. Stored Successfully Stored into Server")
        
        


        
        
        

        
        
        

    
    




        
        
        

    
    


