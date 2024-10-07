# WRITER: LauNT # DATE: 05/2024
# FROM: akaOCR Team - QAI

import numpy as np
import onnxruntime
import cv2
import math

from .utils import post_processing
from .utils import prepare_session


class Detector(object):

    def __init__(self, model_path=None, img_size=640, conf_thres=0.5, iou_thres=0.1):
         # Initialize model

        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.img_size = img_size
        self.initialize_model(model_path)

    
    def __call__(self, image):
        # Object detection

        input_tensor, img_shape, model_shape  = self.prepare_input(image)

        # model inference
        outputs = self.session.run(
            self.output_names,
            {self.input_names[0]: input_tensor}
        )
        # post-processing
        self.boxes, self.scores, self.class_ids = post_processing(
            outputs, img_shape, model_shape,
            self.conf_threshold,
            self.iou_threshold
        )

        return self.boxes, self.scores, self.class_ids


    def initialize_model(self, model_path):
        # Get model informations

        assert model_path != None, "Error: Model not found!"

        # prepare model inference session
        so, provider = prepare_session()
        self.session = onnxruntime.InferenceSession(
            model_path, sess_options=so, providers=provider)
        
        # get model information
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name 
            for i in range(len(model_inputs))
        ]

        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name 
            for i in range(len(model_outputs))
        ]

    def prepare_input(self, image):
        # Prepare input tensor

        img_h, img_w = image.shape[:2]

        # calculate scaling ratio while preserving aspect ratio
        ratio = self.img_size / max(img_h, img_w)
        scaled_w = math.ceil(img_w * ratio)
        scaled_h = math.ceil(img_h * ratio)

        # ensure width and height are multiples of 32
        model_w = min(scaled_w, self.img_size)
        model_h = min(scaled_h, self.img_size)
        model_w = math.ceil(model_w / 32) * 32
        model_h = math.ceil(model_h / 32) * 32

        # resize the image
        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_img = cv2.resize(input_img, (model_w, model_h))

        # normalize the image to 0-1 range
        input_img = input_img.astype(np.float32) / 255.0

        # reorder dimensions to (C, H, W)
        input_img = input_img.transpose(2, 0, 1)

        # add batch dimension
        input_tensor = np.expand_dims(input_img, axis=0)

        return input_tensor, (img_w, img_h), (model_w, model_h)
