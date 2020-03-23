import numpy as np
import pycocotools.mask as mask_util

from detectron2.structures import BoxMode, PolygonMasks, Boxes

class _DetectedInstance:
    """
    Used to store data about detected objects in video frame,
    in order to transfer color to objects in the future frames.

    Attributes:
        label (int):
        textLabel(string):
        bbox (tuple[float]):
        score (float):
        ttl (int): time-to-live for the instance. For example, if ttl=2,
            the instance color can be transferred to objects in the next two frames.
    """

    __slots__ = ["label", "textLabel", "bbox", "score", "ttl"]

    def __init__(self, label, textLabel, bbox,score, ttl):
        self.label = label
        self.textLabel = textLabel
        self.bbox = bbox
        self.score = score
        self.ttl = ttl

    def get_tracker_predictions(self,mode):
        #Coordinates are in XYXY_ABS: (x0, y0, x1, y1)
        #Return coordinates in range [a point,width,height].
        #XYWH_ABS: (x0, y0, w, h) in absolute floating points coordinates.
        
        if mode == 'centroidWH':
            # compute centroid of the bbox ((x1+x2)/2, (y1+y2)/2)
            x,y = ((self.bbox[0]+self.bbox[2])/2, (self.bbox[1]+self.bbox[3])/2)
            #pred = {}
            pred = {
            "x":int(x),
            "y":int(y),
            "w":int(self.bbox[2]),
            "h":int(self.bbox[3]),
            "confidence":int(float(self.score)*100),
            "name": self.textLabel
        }
        else:
            predList = []
            #get top-left corner
            x,y = (self.bbox[0],self.bbox[3])
            #get W/H
            #convert using detectron2 utils
            bbox_mode = BoxMode.XYXY_ABS
            self.bbox = BoxMode.convert(self.bbox, bbox_mode, BoxMode.XYWH_ABS)
            #From paper MOT 2015
            #1, -1, 794.2, 47.5, 71.2, 174.8, 67.5, -1, -1, -1
            predList.append('-1')
            predList.append(str(round(x,2)))
            predList.append(str(round(y,2)))
            predList.append(str(round(self.bbox[2],2)))
            predList.append(str(round(self.bbox[3],2)))
            predList.append(str(round(float(self.score*100),2)))
            predList.append('-1, -1, -1')                        
            pred = ' ,'.join(predList)   
            
        return pred

class DetectionsTxt:
    def __init__(self, metadata):
        """
        Args:
            metadata (MetadataCatalog): image metadata.
        """
        self.metadata = metadata
        self._old_instances = []        

    def get_instance_predictions(self,predictions,preds_format):
        """
        Draw instance-level prediction results on an image.

        Args:
            predictions (Instances): the output of an instance detection/segmentation
                model. Following fields will be used to draw:
                "pred_boxes", "pred_classes", "scores", "pred_masks" (or "pred_masks_rle").

        Returns:
            output (VisImage): image object with visualizations.
        """
        num_instances = len(predictions)
        if num_instances == 0:
            return 
        boxes = predictions.pred_boxes.tensor.numpy() if predictions.has("pred_boxes") else None
        scores = predictions.scores if predictions.has("scores") else None
        classes = predictions.pred_classes.numpy() if predictions.has("pred_classes") else None
        keypoints = predictions.pred_keypoints if predictions.has("pred_keypoints") else None

        masks = None

        detected = []       
        detectedMOT = ''
        for i in range(num_instances):
                textLabel = self.metadata.get("thing_classes")[classes[i]]
                if preds_format == 'MOTchallenge':
                    detected.append(_DetectedInstance(classes[i],textLabel, boxes[i], scores[i],ttl=8).get_tracker_predictions('MOT'))
                    detectedMOT += ('\n')
                else:
                    detected.append(_DetectedInstance(classes[i],textLabel, boxes[i], scores[i],ttl=8).get_tracker_predictions('centroidWH'))

        return detected
