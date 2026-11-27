import cv2
import time
import numpy as np

rng = np.random.default_rng()

def ransac_line(pts, n_iter, t, k=1):
    best_count, best_line, best_mask = 0, None, None
    sub = pts[::k]
    for _ in range(n_iter):
        i, j = rng.integers(len(pts), size=2)
        d = pts[j] - pts[i]
        norm = np.hypot(d[0], d[1])
        if norm == 0:
            continue
        a, b = -d[1] / norm, d[0] / norm
        c = -(a * pts[i, 0] + b * pts[i, 1])
        mask = np.abs(a * sub[:, 0] + b * sub[:, 1] + c) < t
        count = mask.sum()
        if count > best_count:
            best_count, best_line = count, (a, b, c)
            
    if best_line is not None:
        a, b, c = best_line
        best_mask = np.abs(a * pts[:, 0] + b * pts[:, 1] + c) < t
    return best_line, best_mask

def draw_line(img, line, color):
    a, b, c = line
    x0, y0 = -a * c, -b * c
    L = 3000
    p1 = (int(x0 - L * b), int(y0 + L * a))
    p2 = (int(x0 + L * b), int(y0 - L * a))
    cv2.line(img, p1, p2, color, 2)

def refine_line(pts):
    mean = pts.mean(axis=0)
    _, _, vt = np.linalg.svd(pts-mean)
    a, b = vt[1]
    c = -(a * mean[0] + b * mean[1])
    return a, b, c

def rms_dist(pts, line):
    a, b, c = line
    return np.sqrt(np.mean((a*pts[:, 0] + b*pts[:, 1] + c) ** 2))


cap = cv2.VideoCapture(1)

prev = time.perf_counter()
fps = 0.0
s = 0.5
k = 4
while True:
    t0 = time.perf_counter()
    ret, frame = cap.read()
    if not ret:
        continue
    t1 = time.perf_counter()
    
    dt = t1 - prev
    prev = t1
    fps = 1/dt if fps == 0 else 0.9*fps + 0.1*(1/dt)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if s != 1.0:
        gray = cv2.resize(gray, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    edges = cv2.Canny(gray, 100, 200)
    t2 = time.perf_counter()
    
    ys, xs = np.nonzero(edges)
    pts = np.column_stack((xs, ys)).astype(np.float32)
    
    t3 = time.perf_counter()
    line, mask = (None, None)
    if len(pts) >= 2:
        line, mask = ransac_line(pts, 1000, 2.0, k)
    t4 = time.perf_counter()
    if line is not None:
        inl = pts[mask]
        ref = refine_line(inl)
        ang = np.degrees(np.arccos(min(1.0, abs(line[0]*ref[0] + line[1]*ref[1]))))
        print(f"angle diff {ang:.2f} deg  rms ransac {rms_dist(inl, line):.2f}. rms ls {rms_dist(inl, ref):.2f}  fps {fps:.1f} pro  roc_fps {1/((t2-t1)+(t4-t3)):.0f}  w {frame.shape[1]}")
        draw_line(frame, (line[0], line[1], line[2] / s), (0, 0, 255))
        draw_line(frame, (ref[0], ref[1], ref[2] / s), (0, 255, 0))

    
    
    n_in = 0 if mask is None else int(mask.sum())
    print(f"capture {1000*(t1-t0):.1f} ms  canny {1000*(t2-t1):.1f} ms  "
          f"ransac {1000*(t4-t3):.1f} ms  points {len(pts)}  inliers {n_in}")
    cv2.imshow("edges", edges)
    cv2.putText(frame, f"{fps:.1f} fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()