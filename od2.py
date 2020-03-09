#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys

import cv2
import numpy as np
import tensorflow as tf
import multiprocessing
import os
import time
import configparser
from collections import defaultdict
from scan1090 import insert_table_error_log

#sys.path.insert(1, '/home/pi/tensorflow/models/research/object_detection')
from utils import label_map_util
from utils import visualization_utils as vis_util

import image
import mail

config = configparser.ConfigParser()
config.read('creds.conf')


width  = int(config["cam"]["width"])
height = int(config["cam"]["height"])

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
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
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


# ------------------------------------------------------------------------------------------------------------------------------------


def camvid():
    try:
        return cv2.VideoCapture(0)
    except Exception as e:
        print(e)
        time.sleep(5)
        camvid()


def detect(runtime, wait, img_dir, img_name):

    detection_dict = defaultdict(list)
    framerate_list = []
    video = camvid()
    ret = video.set(3, width)
    ret = video.set(4, height)
    ret = video.set(6, 1196444237)
    fps = cv2.getTickFrequency()
    font = cv2.FONT_HERSHEY_SIMPLEX
    frame_rate_calc = 1
    det_count = 0


    start_time = time.time()
    i = 0
    while(True):
        time_diff = time.time() - start_time

        if time_diff < runtime:
            i += 1

            t1 = cv2.getTickCount()
            print(round(time_diff))
            global frame
            ret, frame = video.read()
            if ret == False:
                error = "ret == False\n-> reboot!"
                mail.send(subject="error", text=error)
                insert_table_error_log(error)
                os.system('sudo shutdown -r now')

            if frame is None:
                error = "frame is None\n-> reboot!"
                mail.send(subject="error", text=error)
                insert_table_error_log(error)
                os.system('sudo shutdown -r now')

            if np.sum(frame) == 0 and i > 20:
                error = "20th image still black\n-> reboot!"
                insert_table_error_log(error)
                mail.send(subject="error", text=error)
                os.system('sudo shutdown -r now')
                #np.average(image) < 20 #black gray


            frame = np.asarray(frame)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_expanded = np.expand_dims(frame, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})


            # Draw the results of the detection (aka 'visulaize the results')
            bbox = vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=4,
                min_score_thresh=0.8)
            # -------------------------------------------------------------FUNKTIONIERT---------------------------------------------------------------------------------------

            object_dict = defaultdict(list)

            for index, value in enumerate(classes[0]):
                if scores[0, index] > 0.8: #0.6
                    det_count += 1

                    object_dict[(category_index.get(value)).get('name')].append(scores[0, index])
                #if int(classes[0][0]) == 1: #TODO warum ? Ob Flugzeug das erkannte objekt ist...
                    print(object_dict)

                    max_boxes_to_draw = boxes.shape[0]
                    min_score_thresh = 0.8
                    if det_count == 2:

                        xtf_frame, ymin, xmin, ymax, xmax = bbox

                        img_named = img_dir + "d_" + "_" + img_name
                        p1 = multiprocessing.Process(target=image.save_cv(image=frame, url=img_named))
                        p1.start()

                        h = frame.shape[0]
                        w = frame.shape[1]

                        ymin = int(ymin * h)
                        ymax = int(ymax * h)
                        xmin = int(xmin * w)
                        xmax = int(xmax * w)
                        # print(ymin, ymax, xmin, xmax)

                        croped_frame = frame[ymin:ymax, xmin:xmax]

                        img_named = img_dir + "d_c_" + "_" + img_name
                        p2 = multiprocessing.Process(target=image.save_cv(image=croped_frame, url=img_named))
                        p2.start()


                    obj = list(object_dict.keys())[0]
                    precision = list(object_dict.values())[0][0].item()
                    detection_dict["precision"].append(precision)
                    detection_dict["object"].append(obj)



                    print(obj, precision)

            framerate_list.append(frame_rate_calc)

            #cv2.putText(frame, "FPS: {0:.2f} {0:.2f}".format(frame_rate_calc, fps), (30, 50), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
            #resized_frame = cv2.resize(frame, (0, 0), fx=0.4, fy=0.4)
            #cv2.imshow('Object detector', resized_frame)
            t2 = cv2.getTickCount()
            time1 = (t2 - t1) / fps
            frame_rate_calc = 1 / time1

            if cv2.waitKey(1) == ord('q'):
                video.release()
                cv2.destroyAllWindows()

        else:
            img_namec = img_dir + "c_" +  img_name
            p1 = multiprocessing.Process(target=image.save_cv(image=frame, url=img_namec))
            p1.start()
            video.release()
            cv2.destroyAllWindows()
            try:

                return {"object": str(detection_dict["object"]), "precision": str(detection_dict["precision"]),
                        "img_url": img_named, "framerate_avg": round(np.mean(framerate_list),2)}
            except:

                return {"object": None, "precision": None, "img_url": img_namec, "framerate_avg": round(np.mean(framerate_list),2)}
