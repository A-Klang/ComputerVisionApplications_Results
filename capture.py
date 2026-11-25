import cv2
import time
import numpy as np

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
    frame_blur = cv2.GaussianBlur(frame, (11, 11), 0)
    
    # A: R - (G+B)/2 in BGR
    fb = frame_blur.astype(np.float32)
    redness = fb[:, :, 2] - (fb[:, :, 0] + fb[:, :, 1]) / 2
    _, _, _, red_loc_a = cv2.minMaxLoc(redness)
    
    # B: max a* in L*a*b*
    lab = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2LAB)
    _, _, _, red_loc_b = cv2.minMaxLoc(lab[:, :, 1])
        
    cv2.circle(frame, max_loc, 20, (255, 0, 0), 2)
    cv2.circle(frame, red_loc_a, 20, (0, 0, 255), 2)
    cv2.putText(frame, "A", red_loc_a, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.circle(frame, red_loc_b, 26, (255, 0, 255), 2)
    cv2.putText(frame, "B", red_loc_b, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    proc_ms = (time.perf_counter() - t0) * 1000

    cv2.putText(frame, f"{fps:.1f} FPS proc {proc_ms:.1f} ms", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()