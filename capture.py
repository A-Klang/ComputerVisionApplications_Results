import cv2
import time

cap = cv2.VideoCapture(1)

prev = time.perf_counter()
fps = 0.0
while(True):
    ret, frame = cap.read()
    if not ret:
        continue
    now = time.perf_counter()
    dt = now - prev
    prev = now
    fps = 1/dt if fps == 0 else 0.9*fps + 0.1*(1/dt)
    t0 = time.perf_counter()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    _, max_val, _, max_loc = cv2.minMaxLoc(blurred)
    cv2.circle(frame, max_loc, 20, (255, 0, 0), 2)
    proc_ms = (time.perf_counter() - t0) * 1000


    cv2.putText(frame, f"{fps:.1f} FPS proc {proc_ms:.1f} ms", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()