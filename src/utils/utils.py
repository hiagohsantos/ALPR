from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import numpy as np
import cv2
import time
import sys


_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 255, 0)  # verde


# Initialize the object detection model
base_options = core.BaseOptions(
    file_name="../Models/modelo_EL0_AP53.tflite", use_coral=False, num_threads=4
)
detection_options = processor.DetectionOptions(max_results=1, score_threshold=0.3)
options = vision.ObjectDetectorOptions(
    base_options=base_options, detection_options=detection_options
)
detector = vision.ObjectDetector.create_from_options(options)


# Configuraçoes da camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables to calculate FPS
counter, fps = 0, 0
start_time = time.time()


def capture() :
    global counter, start_time, fps
    counter += 1
    success, image = cap.read()
    # if not success:
    #     sys.exit(
    #         "ERROR: Unable to read from webcam. Please verify your webcam settings."
    #     )
    #image = cv2.flip(image, -1)
    # Calcula o FPS
    if counter % 10 == 0:
        end_time = time.time()
        fps = 10 / (end_time - start_time)
        start_time = end_time
    fps_text = "{:.1f} fps".format(fps)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, fps_text 


# Processa a imagem e devolve um resultado de detecçao
def detect(image: np.ndarray) -> processor.DetectionResult:

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_tensor = vision.TensorImage.create_from_array(rgb_image)
    detection_result = detector.detect(input_tensor)

    return detection_result


# Devolve uma imagem segmentada, de acordo com o resultado da detecçao
def segImage(
    image: np.ndarray, detection_result: processor.DetectionResult
) -> np.ndarray:
    aux = 0
    x1, x2, y1, y2 = 0, 0, 0, 0

    for detection in detection_result.detections:
        bbox = detection.bounding_box
        category = detection.categories[0]
        probability = round(category.score, 2)

        if probability > aux:
            x1 = bbox.origin_x
            y1 = bbox.origin_y
            x2 = bbox.origin_x + bbox.width
            y2 = bbox.origin_y + bbox.height

            aux = probability

    text = f"X1:{x1}, X2: {x2}\n Y1: {y1}, Y2: {y2}"

    image = image[y1:y2, x1:x2]

    return image, text


# Mostra a imagem com as caixas de detecçao desenhadas
def visualize(
    image: np.ndarray, detection_result: processor.DetectionResult
) -> np.ndarray:

    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(
            image,
            start_point,
            end_point,
            _TEXT_COLOR,
            2,
        )

        # Draw label and score
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)

        result_text = category_name + " (" + str(probability) + ")"
        text_location = (_MARGIN + bbox.origin_x, bbox.origin_y - _MARGIN - _ROW_SIZE)

        cv2.putText(
            image,
            result_text,
            text_location,
            cv2.FONT_HERSHEY_PLAIN,
            _FONT_SIZE,
            _TEXT_COLOR,
            _FONT_THICKNESS,
        )
    return image

def tesseract_ocr(image: np.ndarray, config:str = "--oem 3 --psm 13") -> str:
    try:
        img = image.copy()
        text =  pytesseract.image_to_string(img, config = config )
        return text

    except Exception as e:
        print(f"Houve um erro ao fazer o OCR.{e}")

def threshold_image(image, filter_type: int, thresh: int = 127):
    try:
        img = image.copy()
        if (filter_type > 0 or filter_type < 4):
            if(filter_type == 1):
                # Limiarizacao normal (FIXA)
                _, thresholded_image = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
            elif(filter_type == 2):
                # Limiarizacao dinamica Filtro de media
                thresholded_image  = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
            elif(filter_type == 3):
                # Limiarizacao dinamica Filtro Gaussiano
                thresholded_image  = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            return thresholded_image
        else:
            raise ValueError("O tipo de filtro varia de 1 a 3.")

    except Exception as e:
        print(f"Houve um problema ao limiarizar imagem. {e}")
        raise e

def find_tilt_angle(image):
    try:    
        img = image.copy()
        # Copie a imagem limiarizada para os canais R, G e B
        img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        outer_contour = max(contours, key= cv2.contourArea)
 
        rectangle = cv2.minAreaRect(outer_contour)

        cv2.drawContours(img_color, [cv2.boxPoints(rectangle).astype(int)], 0, (0, 255, 0), 2)
        #cv2.drawContours(img_color, [outer_contour], -1, (0, 255, 0), 4)

        tilt_angle = rectangle[-1]
        if (tilt_angle > 45 ):
            tilt_angle -= 90

        return img_color, tilt_angle

    except Exception as e:
        print(f"Houve um problema ao encontrar os contornos na imagem. {e}")
        raise e

def rotate_image(image, tilt_angle):
    try: 
        img = image.copy()
        height, width = img.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), tilt_angle , 1)
        reoriented_image = cv2.warpAffine(img, rotation_matrix, (width, height), flags=cv2.INTER_NEAREST)
        return reoriented_image

    except Exception as e:
        print(f"Houve um problema rotacionar imagem. {e}")
        raise e

if __name__ == "__main__":
    while 1:
        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break
        image = capture()
        options.detection_options.max_results = 3
        detector = vision.ObjectDetector.create_from_options(options)
        image = visualize(image, detect(image))
        cv2.imshow("object_detector", image)

    cap.release()
    cv2.destroyAllWindows()
