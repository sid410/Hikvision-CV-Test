import os
import cv2 as cv
from pathlib import Path
from dotenv import load_dotenv

# Load the enviroment Variables.
# Get the Camera details from me (the .env file)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

username = os.environ['CAM_USER']
password = os.environ['CAM_PASS']
address = os.environ['CAM_IP']

cam_url = f"rtsp://{username}:{password}@{address}"

# Initialize background subtraction and frame capture
backSub = cv.createBackgroundSubtractorMOG2()
cap = cv.VideoCapture(cam_url)

# Compare performance of convert to grayscale vs applying BG Sub
# Press key '1' to change
testSub = False

while(True):
    ret, frame = cap.read()

    if not ret:
        print("No stream found. Exiting...")
        break

    # Test either Grayscale or BG Sub
    if testSub:
        frame = backSub.apply(frame)
    else:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Place FPS
    cv.rectangle(frame, (10,2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(cap.get(cv.CAP_PROP_FPS)), (15,15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
    
    # Show the frame
    cv.imshow('Frame', frame)

    # This is just for testing:
    # Very basic opencv algos
    # Waitkey method to swtich state also bad (not responsive)
    # Press 1 to switch test mode
    if cv.waitKey(1) == ord('1'):
        testSub = not testSub
    # q key to exit loop
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
print("Stopped stream")