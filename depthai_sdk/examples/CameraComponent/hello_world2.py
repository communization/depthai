import depthai as dai
import cv2 

pipeline = dai.Pipeline()

camera = pipeline.create(dai.node.ColorCamera)
mjpeg_still_encoder = pipeline.create(dai.node.VideoEncoder)
mjpeg_encoder_output = pipeline.create(dai.node.XLinkOut)
mjpeg_encoder_output.setStreamName("MJPEG Encoder Output")

mjpeg_still_encoder.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)

camera.setBoardSocket(dai.CameraBoardSocket.RGB)
camera.still.link(mjpeg_still_encoder.input)
mjpeg_still_encoder.bitstream.link(mjpeg_encoder_output.input)

with dai.Device(pipeline) as device:
    still_queue = device.getOutputQueue("MJPEG Encoder Output")
    still_frames = still_queue.tryGetAll()
    for still_frame in still_frames:
        frame = cv2.imdecode(still_frame.getData(), cv2.IMREAD_UNCHANGED)
        cv2.imshow("Still", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()