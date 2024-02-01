from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import numpy as np
import cv2
import time
import sys

# Initialize the object detection model
base_options = core.BaseOptions(
    file_name='../Models/modelo_EL0_AP53.tflite', use_coral=False, num_threads=4)
detection_options = processor.DetectionOptions(
    max_results=1, score_threshold=0.3)
options = vision.ObjectDetectorOptions(
    base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)


_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 255, 0)  # verde
# Configuraçoes da camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables to calculate FPS
counter, fps = 0, 0
start_time = time.time()

def capture() -> np.ndarray:
  global counter, start_time, fps
  counter += 1
  success, image = cap.read()
  if not success:
    sys.exit('ERROR: Unable to read from webcam. Please verify your webcam settings.')

  image = cv2.flip(image, -1)

  # Calcula o FPS
  if counter % 10 == 0:
    end_time = time.time()
    fps = 10 / (end_time - start_time)
    start_time = time.time()

  # Exibe o  FPS
  fps_text = '{:.1f} fps'.format(fps)
  text_location = (24, 20)
  cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1) 
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  return image


# Processa a imagem e devolve um resultado de detecçao
def detect(image: np.ndarray) -> processor.DetectionResult:

  rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  input_tensor = vision.TensorImage.create_from_array(rgb_image)
  detection_result = detector.detect(input_tensor)
  
  return detection_result


# Devolve uma imagem segmentada, de acordo com o resultado da detecçao
def segImage(image: np.ndarray, detection_result: processor.DetectionResult) -> np.ndarray:
  aux = 0
  x1, x2, y1, y2 = 0, 0, 0, 0
  
  for detection in detection_result.detections:
    bbox = detection.bounding_box
    category = detection.categories[0]
    probability = round(category.score, 2)

    if probability > aux :
      x1 = bbox.origin_x
      y1 = bbox.origin_y
      x2 = bbox.origin_x + bbox.width
      y2 = bbox.origin_y + bbox.height

      aux = probability

  text = f'X1:{x1}, X2: {x2}\n Y1: {y1}, Y2: {y2}'

  image = image[y1:y2, x1:x2] 

  return image, text


# Mostra a imagem com as caixas de detecçao desenhadas
def visualize(image: np.ndarray, detection_result: processor.DetectionResult) -> np.ndarray:
  

  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image,
                  start_point,
                  end_point,
                  _TEXT_COLOR,
                  2,
                  )

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + bbox.origin_x,
                      bbox.origin_y -_MARGIN - _ROW_SIZE)
    
    cv2.putText(image,
                result_text,
                text_location,
                cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE,
                _TEXT_COLOR,
                _FONT_THICKNESS,
                )
    
  return image



if __name__ == '__main__':

    while 1:
      
         # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
           break

        image = capture()
        
        options.detection_options.max_results = 3
        detector = vision.ObjectDetector.create_from_options(options)

        image = visualize(image, detect(image))
        cv2.imshow('object_detector', image)


    cap.release()
    cv2.destroyAllWindows()

