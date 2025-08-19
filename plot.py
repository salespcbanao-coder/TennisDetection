import matplotlib.pyplot as plt
import ast
import matplotlib.animation as animation
from common import Landmark, names

FILENAME = "/Users/aryan/Downloads/OcupTennis/results.txt"

with open(FILENAME, 'r') as file:
    data = file.readlines()

#['LEFT_EYE', [734, 482], [739, 484], [738, 485], [737, 486], [738, 488]]
#
#
total = []
for line in data:
    total.append(ast.literal_eval(line))


# total is your list of landmarks: each element = [name, [x1,y1], [x2,y2], ...]

landmark_names = [lm[0] for lm in total]

# Choose which landmarks to plot, or plot all
landmarks_to_plot = []


colors = [
    'red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'black', 'orange',
    'purple', 'brown', 'pink', 'lime', 'teal', 'navy', 'olive', 'maroon',
    'gold', 'silver', 'violet', 'indigo', 'coral', 'turquoise', 'darkgreen',
    'darkblue', 'darkred', 'darkorange', 'deeppink', 'darkviolet', 'skyblue',
    'lightgreen', 'plum', 'khaki', 'salmon'
]

#print(total)

# Plot X and Y over time
plt.figure(figsize=(15, 6))
for item in total:
    if (names.count(item[0])):
        positions = item[1:]  # skip the name
    
        x_vals = [pos[0] for pos in positions]
        y_vals = [pos[1] for pos in positions]
        plt.plot(x_vals, label=f'{landmark_names[total.index(item)]} X', color=colors[total.index(item)])
        plt.plot(y_vals, label=f'{landmark_names[total.index(item)]} Y', linestyle='--', color=colors[total.index(item)])
plt.xlabel('Frame')
plt.ylabel('Pixel Position')
plt.title('Landmark X/Y Position over Time')
plt.legend()
plt.show()


# Plot 2D Trajectories
plt.figure(figsize=(8, 8))
for idx in landmarks_to_plot:
    positions = total[idx][1:]
    x_vals = [pos[0] for pos in positions]
    y_vals = [pos[1] for pos in positions]
    plt.plot(x_vals, y_vals, marker='o', label=f'{landmark_names[idx]}')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Landmark Trajectories')
plt.legend()
plt.gca().invert_yaxis()  # Flip y-axis to match image coordinates
plt.show()



# example: 'movement' is a list of frames, each frame has 33 (x,y) points
# normalize back to image size if needed
def animate(i):
    plt.cla()
    frame = [item[i+1] for item in total]


    xs = [p[0] for p in frame]
    ys = [p[1] for p in frame]
    plt.scatter(xs, ys, c='red')
    
    # connect landmarks like skeleton
    skeleton = [
    (11, 12), # shoulders
    (11, 13), (13, 15), # left arm
    (12, 14), (14, 16), # right arm
    (11, 23), (12, 24), # torso sides
    (23, 24), # hips
    (23, 25), (25, 27), (27, 29), (29, 31), # left leg
    (24, 26), (26, 28), (28, 30), (30, 32), # right leg
    (15, 17), (17, 19), (19, 21), # left hand
    (16, 18), (18, 20), (20, 22), # right hand
    (27, 31), (28, 32), # feet,
     (1, 2), (2, 3),       # left eye
    (4, 5), (5, 6),       # right eye
    (2, 5),               # across eyes
    (7, 8),               # ears
    (9, 10),              # mouth
    (0, 2), (0, 5),       # nose to eyes
   

]

    for a,b in skeleton:
        plt.plot([xs[a], xs[b]], [ys[a], ys[b]], 'blue')
    
    plt.gca().invert_yaxis()  # Important: image coords are flipped


ani = animation.FuncAnimation(plt.gcf(), animate, frames=len(total[0])-1, interval=100)
plt.show()