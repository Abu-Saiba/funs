import cv2
import numpy as np
import time

# Mock function to simulate bulb control
def control_bulb(level):
    if level == 0:
        print("Bulb is OFF")
    elif level == 1:
        print("Bulb is dim")
    elif level == 2:
        print("Bulb is brighterer")
    elif level == 3:
        print("Bulb is medium brightness")
    elif level == 4:
        print("Bulb is very bright")
    elif level == 5:
        print("Bulb is at maximum brightness")

# Initialize the camera
cap = cv2.VideoCapture(0)

# Function to detect palm gestures
def detect_palm(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define skin color range for detection (tweak as per lighting conditions)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.medianBlur(mask, 5)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(largest_contour, returnPoints=False)

        if len(hull) > 3:
            defects = cv2.convexityDefects(largest_contour, hull)

            if defects is not None:
                defect_count = 0

                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(largest_contour[s][0])
                    end = tuple(largest_contour[e][0])
                    far = tuple(largest_contour[f][0])

                    a = np.linalg.norm(np.array(start) - np.array(end))
                    b = np.linalg.norm(np.array(start) - np.array(far))
                    c = np.linalg.norm(np.array(end) - np.array(far))
                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

                    if angle <= np.pi / 2:
                        defect_count += 1

                return defect_count + 1  # Number of fingers detected

    return 0

last_level = None
last_time = time.time()
delay_time = 1  # Delay in seconds between changes

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    level = detect_palm(frame)

    # Check if the detected level has changed and enforce delay
    if level != last_level and time.time() - last_time > delay_time:
        control_bulb(level)
        last_level = level
        last_time = time.time()

    cv2.putText(frame, f"Brightness Level: {level}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Palm Gesture Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        print("Restarting loop...")
        last_level = None  # Reset last_level to restart the sequence

cap.release()
cv2.destroyAllWindows()
