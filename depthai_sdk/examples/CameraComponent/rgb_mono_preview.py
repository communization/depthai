from depthai_sdk import OakCamera
import cv2

with OakCamera() as oak:
    color = oak.create_camera('color', resolution='4K', fps=30)
    left = oak.create_camera('left')
    right = oak.create_camera('right')
    
    color_image = color.get_frame()
    #oak.visualize([color, left, right], fps=True)
    #oak.start(blocking=True)
