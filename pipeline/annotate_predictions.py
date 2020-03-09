import cv2
import torch
import numpy as np

from detectron2.data import MetadataCatalog
#from detectron2.utils.visualizer import ColorMode
# from detectron2.utils.video_visualizer import VideoVisualizer
# from detectron2.utils.visualizer import Visualizer

from pipeline.pipeline import Pipeline
# from pipeline.utils.colors import colors
# from pipeline.utils.text import put_text
from pipeline.build_predictions import DetectionsTxt


class AnnotatePredictions(Pipeline):
    """Pipeline task for video annotation."""

    def __init__(self, dst, metadata_name,frame_num=True, predictions=True):
        self.dst = dst
        self.metadata_name = metadata_name
        self.metadata = MetadataCatalog.get(self.metadata_name)
        #self.instance_mode = instance_mode
        self.frame_num = frame_num
        self.predictions = predictions
        #self.pose_flows = pose_flows

        self.cpu_device = torch.device("cpu")
        #self.video_detections = DetectionsTxTLine(self.metadata, self.instance_mode)
#        self.visualizer = Visualizer(self.metadata, self.instance_mode)

        self.detections_annotations = DetectionsTxt(self.metadata)
        super().__init__()

    def map(self, data): 
        #dst_image = data["image"].copy()
        #data[self.dst] = dst_image

        if self.frame_num:
            self.annotate_frame_num(data)
        if self.predictions:
            self.annotate_predictions(data)
        # if self.pose_flows:
        #     self.annotate_pose_flows(data)

        return data

    def annotate_frame_num(self, data):
        #dst_image = data[self.dst]
        frame_idx = data["frame_num"]

        # put_text(dst_image, f"{frame_idx:04d}", (0, 0),
        #          color=colors.get("white").to_bgr(),
        #          bg_color=colors.get("black").to_bgr(),
        #          org_pos="tl")

    def annotate_predictions(self, data):
        if "predictions" not in data:
            return
        predictions = data["predictions"]
        if "instances" in predictions:
            instances = predictions["instances"]
            tracker_preds = self.detections_annotations.get_instance_predictions(instances.to(self.cpu_device))
        data[self.dst] = tracker_preds
        
        # with PathManager.open(cache_path, "w") as json_file:
        #     logger.info(f"Caching annotations in COCO format: {cache_path}")
        #     json.dump(coco_dict, json_file)