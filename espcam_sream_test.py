import cv2
import time

STREAM_URL = "http://espcam.local:81/stream"

cap = cv2.VideoCapture(STREAM_URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

prev = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    now = time.time()
    fps = 1/(now-prev)
    prev = now

    cv2.putText(frame, f"FPS: {fps:.1f}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("ESP32-CAM", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
