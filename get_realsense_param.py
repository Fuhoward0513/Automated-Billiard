import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
#config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

cfg = pipeline.start(config) # Start pipeline and get the configuration it found
#profile = cfg.get_stream(rs.stream.color) # Fetch stream profile for depth stream
profile = cfg.get_stream(rs.stream.color)
intr = profile.as_video_stream_profile().get_intrinsics() # Downcast to video_stream_profile and fetch intrinsics



inMat = np.array([[intr.fx,0,intr.ppx],[0,intr.fy,intr.ppy],[0,0,1]])
np.savetxt('config/L515/inMat1920.txt',inMat)
print(intr)
