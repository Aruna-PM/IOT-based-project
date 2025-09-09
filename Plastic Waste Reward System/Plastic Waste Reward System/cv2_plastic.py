import os
from ultralytics import YOLO 
import cvzone
import cv2

# Ensure Temp directory exists
if not os.path.exists('Temp'):
    os.makedirs('Temp')

model=0
cap=0
def Load_Camera():
    global model, cap
    # Load the custom-trained YOLO model
    model = YOLO('best.pt') 
    #print(f"Model classes: {model.names}")  # Print class names to identify the index of "plastic"

    # Live webcam
    cap = cv2.VideoCapture(0)
    


def Load_ML_Algorithim_Wait():
    global model, cap
	
    while True:
        # Capture a frame from the camera
        ret, image = cap.read()
        
        # **Flip the image horizontally to correct the mirror effect**
        image = cv2.flip(image, 1)  # Flip image horizontally (1 = horizontal)
        
        # **Get image dimensions**
        height, width, _ = image.shape
        
        # **Calculate the position of the upper-right box**
        box_width = 300  # Width of the box
        box_height = 300  # Height of the box
        box_x1 = width - box_width - 10  # Top-left x (20px padding from right)
        box_y1 = 10  # Top-left y (20px from top)
        box_x2 = width - 10  # Bottom-right x
        box_y2 = box_y1 + box_height  # Bottom-right y

        # Draw the static box (green border) on the upper-right corner of the live stream
        cv2.rectangle(image, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)  # Static green box
        cv2.imshow('frame', image)
        # Listen for keypresses
        key = cv2.waitKey(1)
        
        if key == ord('q'):  # Quit the application
            break
        elif key == ord('c'):  # Take a screenshot and process it
            # Save the frame to "Temp" directory
            screenshot_path = os.path.join('Temp', 'screenshot.jpg')
            cv2.imwrite(screenshot_path, image)
            print(f"Screenshot saved at {screenshot_path}")
            
            # Load the saved screenshot
            screenshot = cv2.imread(screenshot_path)

            # Run YOLO model on the captured frame and store the results
            results = model(screenshot)#, conf=0.7, iou=0.5)  # Increase confidence and IoU thresholds
            
            # Process detection results
            for info in results:
                parameters = info.boxes
                for box in parameters:
                    x1, y1, x2, y2 = box.xyxy[0].numpy().astype('int')
                    confidence = box.conf[0].numpy() * 100  # Confidence percentage
                    class_detected_number = int(box.cls[0])  # Class index
                    class_detected_name = results[0].names[class_detected_number]  # Class name
                    
                    # Check if the detected object's box lies completely inside the static box
                    if x1 >= box_x1 and y1 >= box_y1 and x2 <= box_x2 and y2 <= box_y2:
                        if confidence > 50 and class_detected_name.lower() == "plastic": 
                            # Draw a rectangle around the plastic object
                            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)  # Green for plastic
                            cvzone.putTextRect(image, f'{class_detected_name} {confidence:.2f}%', [x1 + 8, y1 - 12], thickness=2, scale=1.5)
                            print("\nPlastic material detected")
							# Ask for confirmation
                            print("Is it correct? Y/N\n")

                            key = cv2.waitKey(1)
                            
                            while True:
                                confirmation_key = cv2.waitKey(0)
                                
                                if confirmation_key == ord('y'):
                                    print("Thanks for confirmation")
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return "Plastic"
                                elif confirmation_key == ord('n'):
                                    print("Sorry!!! Please show again!")
                                    break             

                        else:
                            # Ask for confirmation
                            print("\nNon-Plastic material detected")
                            print("Is it correct? Y/N\n")

                            while True:
                                confirmation_key = cv2.waitKey(0)
                                
                                if confirmation_key == ord('y'):
                                    print("Thanks for confirmation")
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return "Non-Plastic"
                                elif confirmation_key == ord('n'):
                                    print("Sorry!!! Please show again!")
                                    break             

            
            if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
                break


                

                

    cap.release()
    cv2.destroyAllWindows()
