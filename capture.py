import cv2
import time
import numpy as np

def brightest_loop(img):
    h, w = img.shape
    best, best_loc = -1, (0, 0)
    for y in range(h):
        for x in range(w):
            v = img[y, x]
            if v > best:
                best, best_loc = v, (x, y)
    return best_loc

def brightest_numpy(img):
    y, x = np.unravel_index(np.argmax(img), img.shape)
    return (int(x), int(y))

def brightest_opencv(img):
    _, _, _, loc = cv2.minMaxLoc(img)
    return loc

cap = cv2.VideoCapture(1)

prev = time.perf_counter()
fps = 0.0
mode = 3
names = {1: "loop", 2: "numpy", 3: "opencv"}
search_times = []

det = "n"
show = True
dts, procs, disps = [], [], []

while(True):
    ret, frame = cap.read()
    if not ret:
        continue
    now = time.perf_counter()
    dt = now - prev
    prev = now
    fps = 1/dt if fps == 0 else 0.9*fps + 0.1*(1/dt)
    t0 = time.perf_counter()
    search_ms = 0.0

    if det == "b":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)

        ts = time.perf_counter()
        if mode == 1:
            max_loc = brightest_loop(blurred)
        elif mode == 2:
            max_loc = brightest_numpy(blurred)
        else:
            max_loc = brightest_opencv(blurred)
        search_ms = (time.perf_counter() - ts) * 1000
        search_times.append(search_ms)
        n = 10 if mode == 1 else 100
        if len(search_times) == n:
            print(f"{names[mode]}: mean search {np.mean(search_times):.3f} ms over {n} frames, image {blurred.shape}")
            search_times = []

        cv2.circle(frame, max_loc, 20, (255, 0, 0), 2)

    elif det == "r":
        frame_blur = cv2.GaussianBlur(frame, (11, 11), 0)

        # A: R - (G+B)/2 in BGR
        fb = frame_blur.astype(np.float32)
        redness = fb[:, :, 2] - (fb[:, :, 0] + fb[:, :, 1]) / 2
        _, _, _, red_loc_a = cv2.minMaxLoc(redness)

        # B: max a* in L*a*b*
        lab = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2LAB)
        _, _, _, red_loc_b = cv2.minMaxLoc(lab[:, :, 1])

        cv2.circle(frame, red_loc_a, 20, (0, 0, 255), 2)
        cv2.putText(frame, "A", red_loc_a, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.circle(frame, red_loc_b, 26, (255, 0, 255), 2)
        cv2.putText(frame, "B", red_loc_b, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    proc_ms = (time.perf_counter() - t0) * 1000

    label = {"n": "none", "b": f"brightest/{names[mode]}", "r": "reddest A+B"}[det]
    cv2.putText(frame, f"{fps:.1f} FPS proc {proc_ms:.1f} ms {label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    td = time.perf_counter()
    if show:
        cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xFF
    disp_ms = (time.perf_counter() - td) * 1000

    dts.append(dt * 1000)
    procs.append(proc_ms)
    disps.append(disp_ms)
    if len(dts) == 100:
        print(f"[{label}, display {'on' if show else 'off'}] "
              f"{1000/np.mean(dts):.1f} FPS, loop {np.mean(dts):.1f} ms, "
              f"proc {np.mean(procs):.2f} ms, display {np.mean(disps):.2f} ms")
        dts, procs, disps = [], [], []

    if key == ord('q'):
        break
    elif key in (ord('1'), ord('2'), ord('3')):
        mode = key - ord('0')
        search_times = []
        dts, procs, disps = [], [], []
    elif key in (ord('n'), ord('b'), ord('r')):
        det = chr(key)
        dts, procs, disps = [], [], []
    elif key == ord('d'):
        show = not show
        dts, procs, disps = [], [], []



cap.release()
cv2.destroyAllWindows()