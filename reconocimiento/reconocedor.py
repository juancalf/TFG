#!/usr/bin/env python
# coding: utf-8

#ejecutar en la terminal export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import datetime
import tensorflow as tf
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util
print(tf.version) ##solo funciona para la version 1.* de tensorflow no para la v2

##CONSTANTES 
intervaloCapturaMin = 10 ## minima cantidad de segundos que tiene que pasar entre capturas
tiempoCaptura = 0 ##guarda cuando se realizo la ultima captura en segundos
umbralCaptura = 0.75 ##minimo umbral para realizar captura (en porcentaje)

##INPUTS
#inputVideo = cv2.VideoCapture(0) ##entrada por web cam
inputVideo = cv2.VideoCapture("testVideos/park.mp4") ##entrada de video (para depuracion solo)

##MODELOS
# link: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
MODEL_NAME = 'ssd_inception_v2_coco_2017_11_17'
#MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'

##PATHS
PATH_TO_CKPT = 'modelos/' + MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = os.path.join('labels', 'label.pbtxt')

##ALGORITMO
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
    label_map, max_num_classes=1, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Detection
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        while True: ## pararemos la ejecucion desde fuera matando el hilo
            
            ret, image_np = inputVideo.read()#leemos fotograma
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            
            vis_util.visualize_boxes_and_labels_on_image_array(#funcion de visualizacion
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)

            # Descomentar linea para mostrar por pantalla el video
            cv2.imshow('object detection', cv2.resize(image_np, (800, 600)))
            
            if(scores[0][0] >= umbralCaptura): 
                if (datetime.datetime.now().second + datetime.datetime.now().minute*60 - tiempoCaptura >= intervaloCapturaMin):
                    coords = gps.getCords() #sacamos la informacion del modulo gps
                    tiempoCaptura = datetime.datetime.now().second + datetime.datetime.now().minute*60
                    cv2.putText(image_np, str(coords) + " " + str(datetime.datetime.now()) , 
                           (10,700), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 55, 255), 2, cv2.LINE_AA)##añadimos informacion al pie de la imagen
                    cv2.imwrite("capturas/" + str(datetime.datetime.now()) +'.png', image_np)#guradamos img modificada
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
