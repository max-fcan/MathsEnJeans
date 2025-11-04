# For each point i = 0..3, pick:
#   ("side", which_side, t0) where which_side in {"left","right","top","bottom"} and 0<=t0<=1
#   ("vertex", which_vertex) where which_vertex in {0,1,2,3} (0: top-left, then CCW)
CONNECTIONS = [
  ("side",   "left",   0.25),   # point 0 -> left side at t=0.25
  ("side",   "right",  0.75),   # point 1 -> right side at t=0.75
  ("vertex", 3),                # point 2 -> vertex 3 (bottom-left)
  ("side",   "top",    0.50),   # point 3 -> middle of top side
]

from p5 import *
import random, math

# ===================== USER CONFIG =====================
# Square placement (in pixels)
SQUARE_CENTER = (600, 350)      # center of the square on screen
SQUARE_SIZE   = 300             # square is 1x1 conceptually; here it’s 300×300 pixels

# Four starting draggable points (x, y, diameter, optional color)
POINT_SPECS = [
  (250, 200, 50, 'cornflowerBlue'),
  (950, 220, 50, 'indianRed'),
  (260, 540, 50, 'aquamarine'),
  (960, 560, 50, 'gold'),
]

# How each point connects to the square (edit me!)
#   ("side", which_side, t0) where which_side in {"left","right","top","bottom"} and t0∈[0,1]
#   ("vertex", which_vertex) where which_vertex in {0,1,2,3} in CCW order starting at top-left
CONNECTIONS = [
  ("side",   "left",   0.25),   # point 0
  ("side",   "right",  0.75),   # point 1
  ("vertex", 3),                # point 2
  ("side",   "top",    0.50),   # point 3
]

BRUTE_FORCE_ON = False       # toggled by 's'
ITER_PER_FRAME = 200         # random tries per frame when searching
T_JIGGLE       = 0.08        # step size for random t-perturbation
# =======================================================

# ---------- Helpers for geometry ----------
def square_vertices():
  cx, cy = SQUARE_CENTER
  h = SQUARE_SIZE / 2
  # order: 0=top-left, 1=top-right, 2=bottom-right, 3=bottom-left
  return [
    (cx - h, cy - h),
    (cx + h, cy - h),
    (cx + h, cy + h),
    (cx - h, cy + h),
  ]

def point_on_side(which_side, t):
  """t in [0,1]. which_side in {'left','right','top','bottom'}"""
  v = square_vertices()
  tl, tr, br, bl = v[0], v[1], v[2], v[3]
  if which_side == "left":
    x = tl[0]
    y = lerp(tl[1], bl[1], t)
  elif which_side == "right":
    x = tr[0]
    y = lerp(tr[1], br[1], t)
  elif which_side == "top":
    x = lerp(tl[0], tr[0], t)
    y = tl[1]
  elif which_side == "bottom":
    x = lerp(bl[0], br[0], t)
    y = bl[1]
  else:
    raise ValueError("Side must be left/right/top/bottom")
  return (x, y)

def dist2(p, q):
  dx = p[0] - q[0]
  dy = p[1] - q[1]
  return dx*dx + dy*dy

def line_mid(a, b):
  return ((a[0]+b[0])/2, (a[1]+b[1])/2)

# ---------- Movable points ----------
def createMovableCircle(x, y, d, clr=None):
  return MovableCircle(x, y, d, clr)

class MovableCircle:
  instances = []
  currently_dragging = None

  def __init__(self, x, y, d, clr=None):
    self.x, self.y, self.d = x, y, d
    self.clr = clr
    self.dragging = False
    self.rollover = False
    self.offset_x = 0
    self.offset_y = 0
    MovableCircle.instances.append(self)

  def draw(self):
    self.update()
    noStroke()
    fill(self.clr if (self.rollover and self.clr) else (self.clr or 200))
    circle(self.x, self.y, self.d)

  def update(self):
    self.rollover = (dist(mouse_x, mouse_y, self.x, self.y) < self.d/2)
    if self.dragging:
      self.x = mouse_x + self.offset_x
      self.y = mouse_y + self.offset_y

  def mousePressed(self):
    if self.rollover and MovableCircle.currently_dragging is None:
      self.dragging = True
      MovableCircle.currently_dragging = self
      self.offset_x = self.x - mouse_x
      self.offset_y = self.y - mouse_y

  def mouseReleased(self):
    if self.dragging:
      self.dragging = False
      MovableCircle.currently_dragging = None

  @classmethod
  def handle_mouse_pressed(cls):
    for instance in reversed(cls.instances):
      instance.mousePressed()
      if cls.currently_dragging:
        break

  @classmethod
  def handle_mouse_released(cls):
    if cls.currently_dragging:
      cls.currently_dragging.mouseReleased()

# ---------- App globals ----------
points = []
side_params = []   # holds t for each point connected to a side; None if vertex
best_total = None

def setup():
  size(1200, 800)
  text_font("times")
  text_size(18)
  # create 4 draggable points
  for (x, y, d, clr) in POINT_SPECS:
    points.append(createMovableCircle(x, y, d, clr))
  # capture t-values (for sides); None for vertices
  for spec in CONNECTIONS:
    if spec[0] == "side":
      side_params.append(float(max(0.0, min(1.0, spec[2]))))
    else:
      side_params.append(None)

def draw():
  global best_total
  background(20)
  draw_square()
  # brute force jiggle if toggled
  if BRUTE_FORCE_ON:
    brute_force_step(ITER_PER_FRAME)

  # draw connectors and compute total
  tot = 0.0
  stroke_weight(6)
  for i, p in enumerate(points):
    p.draw()
    a = (p.x, p.y)

    spec = CONNECTIONS[i]
    if spec[0] == "side":
      which_side = spec[1]
      t = side_params[i]
      attach = point_on_side(which_side, t)
      stroke(160, 210, 255)
    else:  # vertex
      vidx = spec[1]
      attach = square_vertices()[vidx]
      stroke(255, 170, 140)

    line(a[0], a[1], attach[0], attach[1])
    tot += math.sqrt(dist2(a, attach))

    # draw attachment marker + length label
    noStroke()
    fill(240)
    circle(attach[0], attach[1], 10)
    mid = line_mid(a, attach)
    fill(220)
    text(str(round(math.sqrt(dist2(a, attach)))), mid[0]+10, mid[1]+10)

  # info panel
  fill(200)
  text(f"Total length = {tot:.2f}", 20, 30)
  text("Drag the circles.  Press 's' to start/stop brute-force (optimizes side-attachments).  Press 'r' to randomize t.", 20, 55)
  if (best_total is None) or (tot < best_total):
    best_total = tot

def draw_square():
  v = square_vertices()
  stroke(255)
  stroke_weight(3)
  noFill()
  # draw perimeter
  begin_shape()
  for (x, y) in v:
    vertex(x, y)
  end_shape(CLOSE)
  # small ticks for 1x1 look (optional grid feel)
  noStroke()
  fill(180)
  for i in range(5):
    x = lerp(v[0][0], v[1][0], i/4)
    y = v[0][1]
    rect(x-1, y-6, 2, 12)
  for i in range(5):
    x = v[3][0]
    y = lerp(v[0][1], v[3][1], i/4)
    rect(x-6, y-1, 12, 2)

def brute_force_step(n_tries):
  """Random hill-climb: jiggle each side-param t; keep improvements."""
  changed = False
  for _ in range(n_tries):
    i = random.randrange(0, 4)
    if side_params[i] is None:
      continue  # vertices are fixed targets
    old_t = side_params[i]
    # measure current total
    old_tot = current_total_length()

    # propose new t
    prop_t = max(0.0, min(1.0, old_t + random.uniform(-T_JIGGLE, T_JIGGLE)))
    side_params[i] = prop_t
    new_tot = current_total_length()

    # keep only if better; else revert
    if new_tot + 1e-9 < old_tot:
      changed = True
    else:
      side_params[i] = old_t
  return changed

def current_total_length():
  tot = 0.0
  v = square_vertices()
  for i, p in enumerate(points):
    a = (p.x, p.y)
    spec = CONNECTIONS[i]
    if spec[0] == "side":
      which_side = spec[1]
      t = side_params[i]
      b = point_on_side(which_side, t)
    else:
      b = v[spec[1]]
    tot += math.sqrt(dist2(a, b))
  return tot

# ---------- Mouse + keys ----------
def mouse_pressed():
  MovableCircle.handle_mouse_pressed()

def mouse_released():
  MovableCircle.handle_mouse_released()

def key_pressed():
  global BRUTE_FORCE_ON
  if key == 's' or key == 'S':
    BRUTE_FORCE_ON = not BRUTE_FORCE_ON
  if key == 'r' or key == 'R':
    # randomize all t for side connections
    for i, spec in enumerate(CONNECTIONS):
      if spec[0] == "side":
        side_params[i] = random.random()

# p5 expects these aliases in snake_case
mousePressed   = mouse_pressed
mouseReleased  = mouse_released
keyPressed     = key_pressed
