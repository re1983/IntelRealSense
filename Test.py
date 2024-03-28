import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# # Get the first device
# device = rs.context().devices[0]

# # Get the first sensor of the device
# sensor = device.sensors[1]

# # Get the stream profiles
# profiles = sensor.get_stream_profiles()

# # Print all profiles
# for p in profiles:
#     print(p)

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Enable gyro stream
config.enable_stream(rs.stream.gyro)

# Enable accelerometer stream
config.enable_stream(rs.stream.accel)


# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        # Get gyro and accelerometer frames
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        accel_frame = frames.first_or_default(rs.stream.accel)
        if not color_frame or not gyro_frame or not accel_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        color_colormap_dim = color_image.shape

        # images = color_image
        # Cast to motion frame and get its data
        gyro_data = gyro_frame.as_motion_frame().get_motion_data()
        accel_data = accel_frame.as_motion_frame().get_motion_data()
        # print("Gyro: ", gyro_data.x, gyro_data.y, gyro_data.z)
        # print("Accel: ", accel_data.x, accel_data.y, accel_data.z)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', color_image)
        cv2.waitKey(1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

finally:

    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()