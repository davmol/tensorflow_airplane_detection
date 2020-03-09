import os
import sys
sys.path.insert(1, '/home/pi/tensorflow/models/research/object_detection')
import csv
from time import sleep
import system_stats
import cv2
import numpy as np
import tensorflow as tf

import sys

from utils import label_map_util
from utils import visualization_utils as vis_util


import image
#------------------------------------------------------------------------------------------------------------------------------------

# This is needed since the working directory is the object_detection folder.
sys.path.append('..')


OD_FOLDER = '/home/pi/tensorflow/models/research/object_detection/'
GRAPH_FOLDER = '/home/pi/tensorflow/models/research/object_detection/aircraft_v1'

CWD_PATH = os.getcwd()

PATH_TO_CKPT = os.path.join(GRAPH_FOLDER,'aircraft_v1.pb')

PATH_TO_LABELS = os.path.join(OD_FOLDER,'data','aircraft_v1.pbtxt')
NUM_CLASSES = 1
## Load the label map.
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    sess = tf.Session(graph=detection_graph)
# Define input and output tensors (i.e. data) for the object detection classifier
# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

#------------------------------------------------------------------------------------------------------------------------------------




results = dict()

resolutions = {"0.3": (640,480), "800x600": (800,600), "1024x768": (1024,768), "1":(1280,960), "2":(1600,1200), "3": (2048,1536), "4": (2240,1680), "5": (2560,1920 ), "6":(3032,2008), "7":(3072,2304 ), "8": (3264,2448)}

for format, res in resolutions.items():

    video = cv2.VideoCapture(0)
    video.set(6, 1196444237) # MJPEG
    video.set(3,res[0])
    video.set(4,res[1])

    i = 0
    frame_rates = []

    while i < 100:
        e1 = cv2.getTickCount()
        fps = video.get(5)
        ret, frame = video.read()

        frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        # Draw the results of the detection (aka 'visulaize the results')
        vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=2,
            min_score_thresh=0.60)



        cv2.imshow("frame", frame)
        e2 = cv2.getTickCount()
        freq = cv2.getTickFrequency()
        t = (e2 - e1) / freq
        frame_rate_calc = 1 / t

        #print(format, res, fps, frame_rate_calc)
        frame_rates.append(frame_rate_calc)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if i == 9:
            global cpu
            cpu = system_stats.cpu()


        i += 1




    video.release()
    cv2.destroyAllWindows()

    results.update({format: {"format": format, "width": res[0], "height": res[1], "max_fps": fps, "fps": [round(i, 2) for i in frame_rates], "fps_mean": round(np.mean(frame_rates), 2), "cpu": cpu}})

    sleep(5)



with open('fps_mean_test_tf.csv', 'w', newline='') as csvfile:
    fieldnames = ['format', 'width',"height",  "max_fps", "fps", "fps_mean", "cpu"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, result in results.items():
        writer.writerow(result)