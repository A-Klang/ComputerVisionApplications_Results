# Assignment 1 results

Working log for the hand-in PDF. Screenshots and raw logs go in `results/`.

Setup: MacBook Air (Apple Silicon), macOS, Python 3.14, OpenCV 5.1.0, NumPy 2.5.5.

## 1. Time per frame and FPS

Loop time = full iteration including `cap.read()`. Processing time = from after `cap.read()` to before `imshow`.

| Version | Camera | Display | FPS | Loop time (ms) | Processing time (ms) | Evidence |
|---|---|---|---|---|---|---|
| No detection | Laptop (idx 1) | yes | 30.0 | 33.4 (single frame) | | `results/02_fps_no_detection_laptop.png` |
| No detection | iPhone Continuity (idx 0) | yes | 30.0 | 35.6 (single frame) | | `results/01_fps_no_detection_phone.png` |
| No detection | | no | | | | |
| Brightest (OpenCV) | Laptop (idx 1) | yes | 30.0 | | 2.9 (single frame) | `results/03_brightest_opencv_laptop.png` |
| Brightest (OpenCV) | | no | | | | |
| Brightest + reddest A and B | Laptop (idx 1) | yes | 30.1 | | 5.2 (single frame) | `results/04_reddest_agree_laptop.png` |
| Reddest | | no | | | | |

## 2. Brightest spot, three implementations (task 5)

| Implementation | Time per frame (ms) | Evidence |
|---|---|---|
| (a) Double for-loop | | |
| (b) NumPy | | |
| (c) OpenCV `minMaxLoc` | | |

## 3. Latency (task 7)

| Camera | Run | Timer on screen (ms) | Timer in displayed frame (ms) | Latency (ms) | Evidence |
|---|---|---|---|---|---|
| Laptop | 1 | | | | |
| Laptop | 2 | | | | |
| Laptop | 3 | | | | |
| Phone | 1 | | | | |
| Phone | 2 | | | | |
| Phone | 3 | | | | |

## 4. Reddest spot, two definitions (task 4 short answer)

Definition A: R - (G+B)/2 in BGR, on float32 after an 11x11 Gaussian blur.

Definition B: max a* in L*a*b* (`cv2.COLOR_BGR2LAB`, a* stored with +128 offset), same blur.

Agreement case: a red container held up to the camera, A and B both land on it (`results/04_reddest_agree_laptop.png`).

Frame where they disagree: `results/05_reddest_disagree_laptop.png`. A lands on the top edge of the yellowish lid next to the fingertips, where the lamp lights it brightly. B lands on the dark red body of the container. A is not normalised for brightness, so a brightly lit warm (orange/yellow, skin) surface scores higher than a darker but purer red. a* measures chromaticity largely separate from lightness L*, so B finds the surface that actually looks red.

Chosen definition and why:

## Observations

- Camera index 0 is the iPhone via Continuity Camera, index 1 is the built-in laptop camera (confirmed). Continuity already covers the "phone streamed to computer" setup for task 6.
- FPS sits at the camera's 30 fps cap with no detection: the loop is camera-bound.
- Brightest spot (grayscale, 11x11 Gaussian blur, `cv2.minMaxLoc`) lands on the lamp. Processing 2.9 ms, about 9% of the 33 ms frame budget, so FPS stays at 30.
- The marker sits on the upper edge of the lamp glow, not its centre: the glow is saturated (many pixels at 255) and `minMaxLoc` returns the first maximum in row-major order, i.e. the top-most one.
