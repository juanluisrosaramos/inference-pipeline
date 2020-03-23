https://arxiv.org/pdf/1603.00831.pdf
3.3 Data format
All images were converted to JPEG and named sequentially to a 6-digit file name (e.g. 000001.jpg). Detection and annotation files are simple comma-separated value (CSV) files. Each line represents one object instance and contains 9 values as shown in Tab. 5.

The first number indicates in which frame the object appears, while the second number identifies that object as belonging to a trajectory by assigning a unique ID (set to −1 in a detection file, as no ID is assigned yet). Each object can be assigned to only one trajectory. The next four numbers indicate the position of the bounding box of the pedestrian in 2D image coordinates. The position is indicated by the top-left corner as well as width and height of the bounding box. This is followed by a single number, which in case of detections denotes their
confidence score. The last two numbers for detection files are ignored (set to -1).

From paper MOT 2015
1, -1, 794.2, 47.5, 71.2, 174.8, 67.5, -1, -1, -1
1, -1, 164.1, 19.6, 66.5, 163.2, 29.4, -1, -1, -1
1, -1, 875.4, 39.9, 25.3, 145.0, 19.6, -1, -1, -1
2, -1, 781.7, 25.1, 69.2, 170.2, 58.1, -1, -1, -1


#From detection file in the MOT16 dataset
1,-1,1359.1,413.27,120.26,362.77,2.3092,-1,-1,-1
1,-1,571.03,402.13,104.56,315.68,1.5028,-1,-1,-1
1,-1,650.8,455.86,63.98,193.94,0.33276,-1,-1,-1
1,-1,721.23,446.86,41.871,127.61,0.27401,-1,-1,-1


Position Name Description
1 Frame number Indicate at which frame the object is present
2 Identity number Each pedestrian trajectory is identified by a unique ID (−1 for detections)
3 Bounding box left Coordinate of the top-left corner of the pedestrian bounding box
4 Bounding box top Coordinate of the top-left corner of the pedestrian bounding box
5 Bounding box width Width in pixels of the pedestrian bounding box
6 Bounding box height Height in pixels of the pedestrian bounding box
7 Confidence score DET: Indicates how confident the detector is that this instance is a pedestrian.
GT: It acts as a flag whether the entry is to be considered (1) or ignored (0).
8 Class GT: Indicates the type of object annotated
9 Visibility GT: Visibility ratio, a number between 0 and 1 that says how much of that object is visible. Can be due
to occlusion and due to image border cropp

Label ID
Pedestrian 1
Person on vehicle 2
Car 3
Bicycle 4
Motorbike 5
Non motorized vehicle 6
Static person 7
Distractor 8
Occluder 9
Occluder on the ground 10
Occluder full 11
Reflection 12