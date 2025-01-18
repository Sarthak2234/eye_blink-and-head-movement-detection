import cv2
import cvzone
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector
import time
# Initialize webcam, detector for the video and capturing frames 

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)

# Define variables

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

# Timer for blink rate calculation

start_time = time.time()
blink_rate = None  # Initialize with None to avoid warnings initially
elapsed_seconds = 0  # To track the elapsed seconds

# Set output resolution for 16:9 aspect ratio (1280x720)

output_width = 1280
output_height = 720

# Define landmarks for head movement tracking

nose_tip_id = 1
chin_id = 152
left_eye_corner_id = 133
right_eye_corner_id = 263

while True:
    # Loop the video feed
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image horizontally

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]

        # Calculate vertical and horizontal distances for EAR
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        # Calculate ratio and track blink

        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        # Detect blink

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0

        # Head movement detection

        nose_tip = face[nose_tip_id]
        chin = face[chin_id]
        left_eye_corner = face[left_eye_corner_id]
        right_eye_corner = face[right_eye_corner_id]

        # Calculate the angles of the head movement
        
        head_tilt_ver, _ = detector.findDistance(nose_tip, chin)
        head_tilt_hor, _ = detector.findDistance(left_eye_corner, right_eye_corner)

        # Draw lines to visualize head movement

        cv2.line(img, tuple(map(int, nose_tip)), tuple(map(int, chin)), (255, 0, 0), 2)  # Vertical line
        cv2.line(img, tuple(map(int, left_eye_corner)), tuple(map(int, right_eye_corner)), (0, 255, 0), 2)  # Horizontal line

        # Determine head movement direction

        head_center = (left_eye_corner[0] + right_eye_corner[0]) / 2
        frame_center = img.shape[1] / 2

        if head_center < frame_center - 5:
            head_direction = "Left"
            color = (0, 0, 255)  # Red color for left movement
        elif head_center > frame_center + 200:
            head_direction = "Right"
            color = (0, 255, 0)  # Green color for right movement
        else:
            head_direction = "Center"
            color = (255, 0, 255)  # Purple color for center

        # Display head movement direction

        cvzone.putTextRect(img, f'Head: {head_direction}', (30, 100), scale=2, colorR=color)

        # Adjust vertical line length based on eyelid closure

        eye_center = ((leftLeft[0] + leftRight[0]) // 2, (leftUp[1] + leftDown[1]) // 2)
        vertical_line_top = (eye_center[0], leftUp[1])
        vertical_line_bottom = (eye_center[0], int(leftUp[1] + lengthVer))

        # Draw the diminishing vertical line

        cv2.line(img, vertical_line_top, vertical_line_bottom, (0, 255, 0), 2)
        cv2.line(img, (leftLeft[0], eye_center[1]), (leftRight[0], eye_center[1]), (0, 255, 0), 2)  # Horizontal line

    # Calculate elapsed time in seconds

    elapsed_time = time.time() - start_time
    elapsed_seconds = int(elapsed_time)

    # Calculate blink rate every 60 seconds

    if elapsed_seconds >= 60:  # Every minute
        blink_rate = blinkCounter  # Calculate blinks per minute
        blinkCounter = 0  # Reset counter
        start_time = time.time()  # Restart timer

    # Create a blank image for displaying information (increase height for better visibility)

    info_panel_height = 600  # Increased height to double the size (from 300 to 600)
    info_panel = np.zeros((info_panel_height, output_width, 3), dtype='uint8')  # Use numpy to create a black image

    # Define Navy Blue Color

    navy_blue = (128, 0, 0)

    # Display Blink Counter

    cvzone.putTextRect(info_panel, f'Blink Count: {blinkCounter}', (30, 50), scale=3, colorR=(0, 255, 0), colorB=navy_blue)

    # Display Timer

    cvzone.putTextRect(info_panel, f'Time: {elapsed_seconds} sec', (30, 150), scale=3, colorR=(0, 255, 0), colorB=navy_blue)

    # Display Blink Rate

    if blink_rate is None:
        cvzone.putTextRect(info_panel, "Calculating Blink Rate...", (30, 250), scale=3, colorR=(255, 0, 255), colorB=navy_blue)
    else:
        cvzone.putTextRect(info_panel, f'Blink Rate: {blink_rate}/min', (30, 250), scale=3, colorR=(255, 255, 0), colorB=navy_blue)

        # Diagnosis

        if blink_rate < 12:
            diagnosis = "Blink Less! Risk of Dry Eyes!"
            color = (0, 0, 255)
        elif 12 <= blink_rate <= 20:
            diagnosis = "Blink Rate Normal. Eyes are healthy!"
            color = (0, 255, 0)
        else:
            diagnosis = "Excessive Blinking Detected! Eyes may be dry."
            color = (0, 165, 255)
        cvzone.putTextRect(info_panel, diagnosis, (30, 350), scale=3, colorR=color, colorB=navy_blue)

    # Resize the information panel to fit the 16:9 aspect ratio
    
    info_panel_resized = cv2.resize(info_panel, (output_width, info_panel_height))
    combined_frame = cvzone.stackImages([img, info_panel_resized], 2, 1)  # Stack vertically
    combined_frame = cv2.resize(combined_frame, (output_width, output_height))  # Resize to 1280x720 (16:9)
    cv2.imshow("Eye and Head Movement Detection", combined_frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()