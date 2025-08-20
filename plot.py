import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ast
import numpy as np
from common import names

FILENAME = "/Users/aryan/Downloads/OcupTennis/results.txt"

# -------------------------
# 1. Load and Parse Data
# -------------------------
total = []
with open(FILENAME, 'r') as file:
    for line in file:
        try:
            total.append(ast.literal_eval(line))
        except Exception as e:
            print("Error parsing line:", line, e)

landmark_names = [lm[0] for lm in total]

# -------------------------
# 2. Helper Functions
# -------------------------
def angle(a, b, c):
    """Compute angle (degrees) at point b formed by points a-b-c"""
    ba = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

def detect_mistakes(frame_idx):
    """Check posture errors for this frame"""
    mistakes = []

    # Check if data is present
    try:
        # Left elbow angle
        shoulder = total[11][frame_idx+1]
        elbow = total[13][frame_idx+1]
        wrist = total[15][frame_idx+1]
        left_elbow_angle = angle(shoulder, elbow, wrist)
        if left_elbow_angle < 30 or left_elbow_angle > 160:
            mistakes.append(f"Left elbow angle unusual ({left_elbow_angle:.1f}°)")

        # Right elbow angle
        shoulder_r = total[12][frame_idx+1]
        elbow_r = total[14][frame_idx+1]
        wrist_r = total[16][frame_idx+1]
        right_elbow_angle = angle(shoulder_r, elbow_r, wrist_r)
        if right_elbow_angle < 30 or right_elbow_angle > 160:
            mistakes.append(f"Right elbow angle unusual ({right_elbow_angle:.1f}°)")

        # Foot distance check (legs spread)
        left_foot = total[27][frame_idx+1]
        right_foot = total[28][frame_idx+1]
        foot_dist = np.linalg.norm(np.array(left_foot) - np.array(right_foot))
        if foot_dist < 20:
            mistakes.append(f"Feet too close ({foot_dist:.1f} px)")

    except IndexError:
        mistakes.append("Frame data missing")

    return mistakes

def detect_swing(frame_idx, hand='right'):
    """Detect swing motion based on hand trajectory"""
    # Use right or left hand
    hand_idx = 16 if hand == 'right' else 15
    positions = [pos[hand_idx+1] for pos in total]  # all frames
    if frame_idx == 0:
        return None
    # Compute hand movement vector between frames
    prev = np.array(positions[frame_idx-1])
    curr = np.array(positions[frame_idx])
    movement = np.linalg.norm(curr - prev)
    # Threshold for swing motion
    if movement > 15:  # adjust pixels threshold
        return "Swing detected"
    return None

def is_court_occupied(frame_idx):
    """Determine if player is detected on court"""
    # Example: check if nose or shoulder landmarks exist
    try:
        nose = total[0][frame_idx+1]
        if nose:
            return True
    except:
        return False
    return False

# -------------------------
# 3. Animation with Mistake & Swing Detection
# -------------------------
skeleton = [
    (11,12),(11,13),(13,15),(12,14),(14,16),
    (11,23),(12,24),(23,24),(23,25),(25,27),(27,29),(29,31),
    (24,26),(26,28),(28,30),(30,32),(15,17),(17,19),(19,21),
    (16,18),(18,20),(20,22),(27,31),(28,32),
    (1,2),(2,3),(4,5),(5,6),(2,5),(7,8),(9,10),(0,2),(0,5)
]

def animate(i):
    plt.cla()
    try:
        frame = [item[i+1] for item in total]
    except:
        return

    xs = [p[0] for p in frame]
    ys = [p[1] for p in frame]
    plt.scatter(xs, ys, c='red')

    # Draw skeleton
    for a, b in skeleton:
        plt.plot([xs[a], xs[b]], [ys[a], ys[b]], 'blue')

    plt.gca().invert_yaxis()
    plt.title(f'Frame {i}')

    # Mistakes
    mistakes = detect_mistakes(i)

    # Swing detection
    swing = detect_swing(i)
    if swing:
        mistakes.append(swing)

    # Court occupancy
    occupied = is_court_occupied(i)
    court_status = "Court Occupied" if occupied else "Court Unoccupied"

    # Display info
    info = " | ".join(mistakes)
    plt.suptitle(f"{court_status} | {info}", color='red' if mistakes else 'green', fontsize=10)

ani = animation.FuncAnimation(plt.gcf(), animate, frames=len(total[0])-1, interval=100)
plt.show()
