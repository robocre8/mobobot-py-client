import cv2
import time

STREAM_URL = "http://mobobot-cam.local:81/stream"

cap = cv2.VideoCapture(STREAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

prev = time.time()

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open MOBOBOT-CAM.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    now = time.time()
    fps = 1/(now-prev)
    prev = now

    cv2.putText(frame, f"FPS: {fps:.1f}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("MOBOBOT-CAM", frame)

    # 4. Stop the stream when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. When everything is done, release the capture and close windows
cap.release()
cv2.destroyAllWindows()