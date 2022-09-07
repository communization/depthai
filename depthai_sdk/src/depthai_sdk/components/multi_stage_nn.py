import depthai as dai
from typing import Tuple, Union, Optional, List
from string import Template
import os
from pathlib import Path

class MultiStageNnConfig:
    debug: bool
    labels: Optional[List[int]]
    scaleBb: Optional[Tuple[int, int]]

    def __init__(self, debug, labels=None, scaleBb=None):
        self.debug = debug
        self.labels = labels
        self.scaleBb = scaleBb


class MultiStageNN():
    script: dai.node.Script
    manip: dai.node.ImageManip
    out: dai.Node.Output # Cropped imgFrame output
    i: int = 0

    _size: Tuple[int, int]
    def __init__(self,
        pipeline: dai.Pipeline,
        detector: Union[
            dai.node.MobileNetDetectionNetwork,
            dai.node.MobileNetSpatialDetectionNetwork,
            dai.node.YoloDetectionNetwork,
            dai.node.YoloSpatialDetectionNetwork], # Object detector
        highResFrames: dai.Node.Output,
        size: Tuple[int, int],
        debug = False
        ) -> None:
        """
        Args:
            detections (dai.Node.Output): Object detection output
            highResFrames (dai.Node.Output): Output that will provide high resolution frames
        """

        self.script = pipeline.create(dai.node.Script)
        self.script.setProcessor(dai.ProcessorType.LEON_CSS) # More stable
        self._size = size

        detector.out.link(self.script.inputs['detections'])
        highResFrames.link(self.script.inputs['frames'])

        self.configure(MultiStageNnConfig(debug))

        self.manip = pipeline.create(dai.node.ImageManip)
        self.manip.initialConfig.setResize(size)
        self.manip.setWaitForConfigInput(True)
        self.manip.setMaxOutputFrameSize(size[0] * size[1] * 3)
        self.manip.setNumFramesPool(20)
        self.script.outputs['manip_cfg'].link(self.manip.inputConfig)
        self.script.outputs['manip_img'].link(self.manip.inputImage)
        self.out = self.manip.out

    def configure(self, config: MultiStageNnConfig = None) -> None:
        """
        Args:
            debug (bool, default False): Debug script node
            labels (List[int], optional): Crop & run inference only on objects with these labels
            scaleBb (Tuple[int, int], optional): Scale detection bounding boxes (x, y) before cropping the frame. In %.
        """
        if config is None:
            return

        with open(Path(os.path.dirname(__file__)) / 'template_multi_stage_script.py', 'r') as file:
            code = Template(file.read()).substitute(
                DEBUG = '' if config.debug else '#',
                CHECK_LABELS = f"if det.label not in {str(config.labels)}: continue" if config.labels else "",
                WIDTH = str(self._size[0]),
                HEIGHT = str(self._size[1]),
                SCALE_BB_XMIN = f"-{config.scaleBb[0]/100}" if config.scaleBb else "", # % to float value
                SCALE_BB_YMIN = f"-{config.scaleBb[1]/100}" if config.scaleBb else "",
                SCALE_BB_XMAX = f"+{config.scaleBb[0]/100}" if config.scaleBb else "",
                SCALE_BB_YMAX = f"+{config.scaleBb[1]/100}" if config.scaleBb else "",
            )
            self.script.setScript(code)
            # print(f"\n------------{code}\n---------------")

