# Assignment 1: Results

Repository: https://github.com/A-Klang/ComputerVisionApplications_Results

MacBook Air (Apple Silicon), Python 3.14, OpenCV 5.1.0, NumPy 2.5.5. Laptop camera at 1280x720. Phone: iPhone streamed to the laptop with Continuity Camera. All values are means over batches of 100 frames unless stated otherwise.

## Time per frame and FPS

| Version | Camera | Display | FPS | Time per frame (ms) | Processing (ms) | Display (ms) |
|---|---|---|---|---|---|---|
| No detection | Laptop | on | 30.0 | 33.3 | 0.0 | 16.2 |
| No detection | Laptop | off | 30.0 | 33.3 | 0.0 | 11.0 |
| Brightest | Laptop | on | 30.0 | 33.3 | 1.9 | 15.0 |
| Brightest | Laptop | off | 30.0 | 33.3 | 2.2 | 11.0 |
| Reddest | Laptop | on | 30.0 | 33.3 | 5.0 | 14.8 |
| Reddest | Laptop | off | 29.9 | 33.4 | 6.4 | 11.1 |
| No detection | Phone | on | 29.9 | 33.4 | 0.0 | 19.0 |
| No detection | Phone | off | 29.9 | 33.4 | 0.0 | 11.0 |

Time per frame is the full loop including `cap.read()`. Processing is detection and drawing. Display is `imshow` plus `waitKey(1)`.

## Brightest spot, three implementations

Search time only, on the same blurred grayscale frame.

| Implementation | Time per frame (ms) | FPS |
|---|---|---|
| (a) Double for-loop | 73.0 | 10 |
| (b) NumPy `argmax` | 0.058 | 30 |
| (c) OpenCV `minMaxLoc` | 0.060 | 30 |

## Latency

| Camera | Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Mean (ms) |
|---|---|---|---|---|---|---|
| Laptop | 100 | 130 | 100 | 140 | | 118 |
| Phone | 30 | 120 | 180 | 140 | 170 | 128 |

Latency is the stopwatch on screen minus the stopwatch in the displayed video frame, read from one screenshot per run. The laptop camera filmed the screen through a mirror.

## Task 4: Reddest spot

Definition A: largest R − (G+B)/2 in BGR, i.e. how much red exceeds the other two channels.

Definition B: largest a\* in L\*a\*b\*, the green to red axis.

Frame where they disagree: `results/05_reddest_disagree_laptop.png`. A lands on the brightly lit yellowish lid, B on the red container.

I chose B. A grows with brightness, so a brightly lit warm surface can score higher than a darker surface that is clearly red, which is what happens in this frame. a\* separates colour from lightness, so B finds what actually looks red.

## Raw logs and screenshots

All in `Assignment1/results/`: timing logs (`07`, `10`, `14`, `16`), detection screenshots (`03`–`06`, `08`, `09`, `11`–`13`, `15`) and latency screenshots (`17`, `18`).
