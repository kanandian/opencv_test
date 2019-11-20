import numpy as np

screen_width = 1280
screen_height = 800
background_color = (111, 111, 111)
leaf_width = 150
leaf_height = 120
max_distance = 300
move_speed = 4
sweep_speed = 10
add_leaf_speed_factor = 0.5
initial_leaves_num = 4
camera_width = 1080
camera_height = 720

lower_skin = np.array([100, 50, 0])
upper_skin = np.array([125, 255, 255])
kernel = np.ones((5, 5), np.uint8)

dectect_mod = 2

show_camera = False