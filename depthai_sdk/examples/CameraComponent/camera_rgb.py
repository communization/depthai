import depthai as dai
import cv2
import time

pipeline = dai.Pipeline()

camRgb = pipeline.createColorCamera()
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(False)
camRgb.setFps(40)

rgbout = pipeline.createXLinkOut()
rgbout.setStreamName("RGB")
camRgb.video.link(rgbout.input)

with dai.Device(pipeline) as device:
    device.startPipeline()
    qRgb = device.getOutputQueue(name="RGB", maxSize=4, blocking=False)

    frame_count = 0
    start_time = time.time()

    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
        frame_count += 1

        # Calculate FPS
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time

        # Display FPS on frame
        frame = inRgb.getCvFrame()
        cv2.putText(
            frame,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        cv2.imshow("bgr", frame)

        if cv2.waitKey(1) == ord("q"):
            break
