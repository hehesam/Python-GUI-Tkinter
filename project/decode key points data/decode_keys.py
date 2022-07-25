import redis
import numpy as np

# ========= Settings =========
list_x_num = 35
list_y_num = 3
# ============================

red = redis.Redis()

while True:

    key_data_red = red.get('key_points').decode()

    key_data_list = list(key_data_red.split(' '))
    
    key_data = np.zeros((list_x_num, list_y_num))
    for i in range(list_x_num):
        for j in range(list_y_num):
            key_data[i, j] = int(key_data_list[i*list_y_num + j])

    # Angle calculator
    right_shoulder = key_data[12]
    right_elbow = key_data[14]
    right_wrist = key_data[16]

    se = right_elbow - right_shoulder
    ew = right_wrist - right_elbow

    theta_rad = np.pi -  np.arccos(se.dot(ew)/(np.linalg.norm(se) * np.linalg.norm(ew)))

    theta = np.degrees(theta_rad)

    red.set('R_elbow_angle', theta)
