import depthai as dai
import cv2
pipeline = dai.Pipeline()
# Define a source - color camera
camRgb = pipeline.createColorCamera()

camRgb.setPreviewSize(300, 300)
camRgb.setInterleaved(False)
camRgb.setFps(40)
# Create output
xoutRgb = pipeline.createXLinkOut()
xoutRgb.setStreamName("rgb")
# Link plugins CAM -> XLINK
camRgb.preview.link(xoutRgb.input)
# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
        # Retrieve 'bgr' (opencv format) frame
        cv2.imshow("bgr", inRgb.getCvFrame())
        if cv2.waitKey(1) == ord('q'):
            break

# import depthai as dai
# import cv2
#
# # Start defining a pipeline