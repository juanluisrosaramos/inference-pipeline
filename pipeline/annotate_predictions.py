import cv2
import torch
import numpy as np
import json
from detectron2.data import MetadataCatalog
from pipeline.pipeline import Pipeline
from pipeline.build_predictions import DetectionsTxt


class AnnotatePredictions(Pipeline):
    """Pipeline task for video annotation."""

    def __init__(self, dst, metadata_name,frame_num=True, predictions=True,preds_format='MOTchallenge'):
        self.dst = dst
        self.preds_format = preds_format
        self.metadata_name = metadata_name
        self.metadata = MetadataCatalog.get(self.metadata_name)
        self.frame_num = frame_num
        self.predictions = predictions
        self.cpu_device = torch.device("cpu")
        self.detections_annotations = DetectionsTxt(self.metadata)
        super().__init__()

    def map(self, data): 
        dst_image = data["tracker_preds"]
        data[self.dst] = dst_image
        if self.frame_num:
            self.annotate_frame_num(data)
        if self.predictions:
            self.annotate_predictions(data)
        
        return data

    def annotate_frame_num(self, data):
        dst_image = data[self.dst]
        frame_idx = data["frame_num"]
        

    def annotate_predictions(self, data):
        if "predictions" not in data:
            return
        #dst_image = data[self.dst]
        predictions = data["predictions"]
        if "instances" in predictions:
            instances = predictions["instances"]
            tracker_preds = {
                "frame":str(data["frame_num"]),
                "detections":self.detections_annotations.get_instance_predictions(instances.to(self.cpu_device),'MOTchallenge')
            }
            #tracker_preds = self.detections_annotations.get_instance_predictions(instances.to(self.cpu_device))
        
        data[self.dst] = tracker_preds  
        if self.preds_format != 'MOTchallenge':
            with open('predictions.txt','w') as outfile:
                json.dump(tracker_preds,outfile)
                outfile.write('\n')
        else:
            import csv
            val_string = ''
            with open('predictions.txt', 'a') as f:    
                if tracker_preds["detections"] != None:
                    for i in tracker_preds["detections"]:
                        val_string = val_string + tracker_preds["frame"]+','+i+'\n'
                    f.write(val_string)
        
        #print(tracker_preds)     
        #{"frame":0,"detections":[{"x":1635,"y":247,"w":61,"h":38,"confidence":38,"name":"car"},{"x":1799,"y":250,"w":54,"h":33,"confidence":33,"name":"car"}]}
