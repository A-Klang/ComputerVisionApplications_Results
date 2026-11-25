# Assignment 1 results

Working log for the hand-in PDF. Screenshots and raw logs go in `results/`.

Setup: MacBook Air (Apple Silicon), macOS, Python 3.14, OpenCV 5.1.0, NumPy 2.5.5.

## 1. Time per frame and FPS

Laptop camera (idx 1), 1280x720. Mean over 4-8 batches of 100 frames each (`results/14_fps_log_versions.txt`), startup batch excluded.
Loop time = full iteration including `cap.read()`. Processing = detection + drawing. GUI = `imshow` (when display on) + `waitKey(1)`.

| Version | Display | FPS | Loop time (ms) | Processing (ms) | GUI (ms) | Evidence |
|---|---|---|---|---|---|---|
| No detection | on | 30.0 | 33.3 | 0.00 | 16.2 | `results/11_mode_none_laptop.png` |
| No detection | off | 30.0 | 33.3 | 0.00 | 11.0 | log |
| Brightest (OpenCV) | on | 30.0 | 33.3 | 1.93 | 15.0 | `results/12_mode_brightest_laptop.png` |
| Brightest (OpenCV) | off | 30.0 | 33.3 | 2.22 | 11.0 | log |
| Reddest (A and B) | on | 30.0 | 33.3 | 5.04 | 14.8 | `results/13_mode_reddest_laptop.png` |
| Reddest (A and B) | off | 29.9 | 33.4 | 6.35 | 11.1 | log |
| Brightest (Python loop) | on | 10.0 | ~100 | 78.2 (single frame) | | `results/08_search_loop_laptop.png` |

Phone camera (iPhone via Continuity, idx 0), no detection, display on: 30.0 FPS (`results/01_fps_no_detection_phone.png`, single frame). Full phone run pending.

## 2. Brightest spot, three implementations (task 5)

| Implementation | Time per frame (ms) | Evidence |
|---|---|---|
| (a) Double for-loop | 73.0 (mean of 26 x 10 frames, range 72.6-74.1); FPS drops to 10 | `results/08_search_loop_laptop.png`, `results/10_search_log_all_modes.txt` |
| (b) NumPy `argmax` | 0.058 (mean of 3 x 100 frames, range 0.052-0.068) | `results/09_search_numpy_laptop.png`, `results/10_search_log_all_modes.txt` |
| (c) OpenCV `minMaxLoc` | 0.060 (mean of 26 x 100 frames, range 0.054-0.067) | `results/06_search_opencv_laptop.png`, `results/07_search_log_opencv.txt`, `results/10_search_log_all_modes.txt` |

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
- Three implementations (task 5), 1280x720 blurred grayscale, search only: loop 73.0 ms, NumPy 0.058 ms, OpenCV 0.060 ms. The loop is about 1250x slower than compiled code. NumPy and OpenCV are equal within noise: both run one SIMD pass in C over a uint8 array, so the search is memory-bound. The gap is interpreted Python vs. compiled code, not NumPy vs. OpenCV.
- Loop mode drops the display from 30 to 10 FPS: 78 ms processing spans more than two 33 ms camera frame intervals.
- All three implementations mark the same pixel (first maximum in row-major order: strict `>` in the loop, `argmax`, `minMaxLoc`).
- FPS is 30 for every version except the Python loop: the program is camera-bound. `cap.read()` blocks until the next frame (33.3 ms at 30 fps), so any work under about 33 ms only shortens the wait and does not change FPS. Processing and GUI time are what separate the versions.
- Displaying costs about 4-5 ms per frame (`imshow`): GUI time is ~15-16 ms with display on and ~11 ms with display off. The remaining ~11 ms is `waitKey(1)` itself, which on macOS takes far longer than the 1 ms requested (event loop overhead; exact cause not verified).
- Processing was slightly higher with display off (brightest 2.2 vs 1.9 ms, reddest 6.4 vs 5.0 ms). Possibly the CPU clocking down or moving to efficiency cores when it has less work per frame; not verified.
