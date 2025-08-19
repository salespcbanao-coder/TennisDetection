import cv2
import mediapipe as mp

import matplotlib.pyplot as plt
from common import Landmark

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

FILENAME = "/Users/aryan/Downloads/OcupTennis/results.txt"
total = [['NOSE'], ['LEFT_EYE_INNER'], ['LEFT_EYE'], ['LEFT_EYE_OUTER'], ['RIGHT_EYE_INNER'], ['RIGHT_EYE'],
          ['RIGHT_EYE_OUTER'], ['LEFT_EAR'], ['RIGHT_EAR'], ['MOUTH_LEFT'], ['MOUTH_RIGHT'], ['LEFT_SHOULDER'], 
          ['RIGHT_SHOULDER'], ['LEFT_ELBOW'], ['RIGHT_ELBOW'], ['LEFT_WRIST'], ['RIGHT_WRIST'], ['LEFT_PINKY'], 
          ['RIGHT_PINKY'], ['LEFT_INDEX'], ['RIGHT_INDEX'], ['LEFT_THUMB'], ['RIGHT_THUMB'], ['LEFT_HIP'], ['RIGHT_HIP'], 
          ['LEFT_KNEE'], ['RIGHT_KNEE'], ['LEFT_ANKLE'], ['RIGHT_ANKLE'], ['LEFT_HEEL'], ['RIGHT_HEEL'], ['LEFT_FOOT_INDEX'], ['RIGHT_FOOT_INDEX']]



frame_count = 0
write_interval = 100
allowed = [] #leave empty if no limitations
while True:
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    h, w, c = frame.shape
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            print(id)
            cx, cy = int(lm.x * w), int(lm.y * h)
            total[id].append([cx,cy])
        frame_count +=1


    if (frame_count%write_interval == 0):
        with open(FILENAME, 'w') as file:
            for i in range(len(total)-1):
                if (len(allowed) == 0 or len(allowed) >0 and allowed.count(i) !=0):
                    file.write(str(total[i]) + '\n')
            file.write(str(total[i]) )
        frame_count = 0

        
    
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    cv2.imshow("Pose", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


with open(FILENAME, 'w') as file:
    for i in range(len(total)-1):
        if (len(allowed) == 0 or len(allowed) >0 and allowed.count(i) !=0):
            file.write(str(total[i]) + '\n')
    file.write(str(total[i]) )
frame_count = 0