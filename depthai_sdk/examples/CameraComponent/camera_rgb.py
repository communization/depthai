import depthai as dai
import cv2

pipeline = dai.Pipeline()
# Define a source - color camera

camRgb = pipeline.createColorCamera()
camRgb.setResolution(
    dai.ColorCameraProperties.SensorResolution.THE_1080_P
)  # THE_1080_P #THE_4_K
camRgb.setInterleaved(False)
camRgb.setFps(40)

rgbout = pipeline.createXLinkOut()
rgbout.setStreamName("RGB")
camRgb.video.link(rgbout.input)


camdepth = pipeline.createStereoDepth()
camdepth.setConfidenceThreshold(200)

depthout = pipeline.createXLinkOut()
depthout.setStreamName("depth")
camdepth.depth.link(depthout.input)

# Pipeline defined, now the device is connected to
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()
    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="RGB", maxSize=4, blocking=False)
    qDepth = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
        # Retrieve 'bgr' (opencv format) frame
        cv2.imshow("bgr", inRgb.getCvFrame())
        cv2.imshow("depth", qDepth.get().getFrame())
        if cv2.waitKey(1) == ord("q"):
            break
