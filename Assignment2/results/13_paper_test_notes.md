# Paper test (laptop sleeve as stand-in), s = 0.5, k = 4, Canny 100/200, N = 1000
Background: me and the room behind me.

a) Slow sideways movement: stays on the sleeve edge mostly, occasionally jumps to my shoulder.
   Strongly distance dependent. Sleeve far away -> edge is short in the image and the line never locks onto it.
   Sleeve close -> slow movement tracked very well.

b) Rotation: follows smoothly mostly.
   In-plane (about the camera axis): near 90 deg my arm comes clearly into view and the line moves to the arm,
   since the sleeve edge is no longer the longest line.
   Out-of-plane (tilting about x/y): follows better, but after too much tilt it breaks down and jitters,
   mostly snapping onto my arm or flickering seemingly randomly.

c) Fast movement: keeps up mostly, lags behind a bit for quick up/down movement.
   In the edges window the sleeve edge drops out during fast motion (goes basically black).

d) Partly out of view: holds until roughly half the edge is out of frame, then switches to the short side
   of the sleeve (which at that point is the longer visible edge). Flickers a bit just before the switch.
   Bringing it back in: locks on again basically right away, with a bit of flicker.

e) Distance: covered under a) (far away -> never locks on, close -> tracks well).

# Other lines in the room (same settings, panning the laptop around)
Picks up anything with clear contrast: dark green curtain against white wall, brown shelves against white wall,
and very strongly the straight mirror edge against the brown wardrobe door (shiny mirror vs matte wood).
- 14_room_mirror_edge.png: line locked on the mirror edge on the wardrobe door, spans full frame height.
  Red (RANSAC) and green (LS) diverge slightly at the top.
- 15_room_curtain_edge.png: line on the curtain/wall boundary, full frame height, red hidden under green.
  The wardrobe edges to the right (lower contrast in the dim light) lose out.
