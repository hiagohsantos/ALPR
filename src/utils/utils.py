from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import numpy as np
import cv2
import time
import sys
import pytesseract
import re
import os
from dotenv import load_dotenv
import base64
import requests
import json
from io import BytesIO
from PIL import Image

load_dotenv()

_MARGIN = 5  # pixels
_ROW_SIZE = 5  # pixels
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


def capture():
    try:
        global counter, start_time, fps
        counter += 1
        success, image = cap.read()
        # if not success:
        #     sys.exit(
        #         "ERROR: Unable to read from webcam. Please verify your webcam settings."
        #     )
        # image = cv2.flip(image, -1)
        # Calcula o FPS
        if counter % 10 == 0:
            end_time = time.time()
            fps = 10 / (end_time - start_time)
            start_time = end_time
        fps_text = "{:.1f} fps".format(fps)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image, fps_text
    except Exception as e:
        print(e)
        return None, "00.0"


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

    text = f"X:  {x1}  -  {x2}\n Y:  {y1}  -  {y2}"
    result_text = category.category_name + " (" + str(probability) + ")"
    text_location = (_MARGIN + bbox.origin_x, bbox.origin_y - _MARGIN - _ROW_SIZE)

    image = image[y1:y2, x1:x2]
    data = [(x1, y1), (x2, y2), result_text, text_location]
    return image, text, data


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


def detection_data(detection_result: processor.DetectionResult):
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height

        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)

        result_text = category_name + " (" + str(probability) + ")"
        text_location = (_MARGIN + bbox.origin_x, bbox.origin_y - _MARGIN - _ROW_SIZE)
    return [start_point, end_point, result_text, text_location]


def tesseract_ocr(image: np.ndarray, config: str = "--oem 3 --psm 13") -> str:
    try:
        img = image.copy()
        #img = cv2.GaussianBlur(img, (7,3), 0)
        text = pytesseract.image_to_string(img, config=config)
        if text:
            return re.sub(r"[^a-zA-Z0-9]", "", text).upper()
        else:
            return '' 

    except Exception as e:
        print(f"Houve um erro ao fazer o OCR.{e}")
        return '' 


def threshold_image(image, filter_type: int, thresh: int = 127):
    try:
        img = image.copy()
        if filter_type > 0 or filter_type < 4:
            if filter_type == 1:
                # Limiarizacao normal (FIXA)
                _, thresholded_image = cv2.threshold(
                    img, thresh, 255, cv2.THRESH_BINARY
                )
            elif filter_type == 2:
                # Limiarizacao dinamica Filtro de media
                thresholded_image = cv2.adaptiveThreshold(
                    img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
                )
            elif filter_type == 3:
                # Limiarizacao dinamica Filtro Gaussiano
                thresholded_image = cv2.adaptiveThreshold(
                    img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
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
        outer_contour = max(contours, key=cv2.contourArea)

        rect = cv2.minAreaRect(outer_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        indice_lado_maior = np.argmax(
            [np.linalg.norm(box[i] - box[(i + 1) % 4]) for i in range(4)]
        )
        ponto1 = box[indice_lado_maior]
        ponto2 = box[(indice_lado_maior + 1) % 4]

        angle = np.arctan2(ponto2[1] - ponto1[1], ponto2[0] - ponto1[0]) * 180 / np.pi
        angle = np.clip(angle, -90, 90)
        print(angle)
        if angle > 30 or angle < -30:
            angle = 0
        cv2.drawContours(img_color, [box], 0, (0, 255, 0), 2)

        return img_color, angle, rect

    except Exception as e:
        print(f"Houve um problema ao encontrar os contornos na imagem. {e}")


def rotate_image(image, tilt_angle):
    try:
        img = image.copy()

        if img.size == 0:
            raise ValueError("A imagem de entrada está vazia.")

        height, width = img.shape[:2]

        if width <= 0 or height <= 0:
            raise ValueError("As dimensões da imagem não são válidas.")

        rotation_matrix = cv2.getRotationMatrix2D(
            (width / 2, height / 2), tilt_angle, 1
        )
        reoriented_image = cv2.warpAffine(
            img, rotation_matrix, (width, height), flags=cv2.INTER_NEAREST
        )

        return reoriented_image

    except Exception as e:
        print(f"Houve um problema ao rotacionar a imagem. {e}")
        return img


def ocr_goole_cloud(image) -> str:
    try:
        api_url = (
            os.getenv("GOOGLE_CLOUD_API_URL")+f"?key={os.getenv('GOOGLE_CLOUD_API_KEY')}"
        )

        bytes_io = BytesIO()
        imagem_pil = Image.fromarray(image.copy())
        imagem_pil.save(bytes_io, format="PNG")
        imagem_bytes = bytes_io.getvalue()
        img_base64 = base64.b64encode(imagem_bytes).decode("utf-8")

        data = {
            "requests": [
                {
                    "image": {
                        "content": img_base64,
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION",
                        }
                    ],
                }
            ],
        }

        post_api = requests.post(url=api_url, data=json.dumps(data))
        ocr_text = post_api.json()["responses"][0]["fullTextAnnotation"]["text"]
        
        return re.sub(r"[^a-zA-Z0-9]", "", ocr_text).upper()
        # print(post_api.json()['responses'][0]['textAnnotations'][0]['description'])

    except Exception as e:
        print(f"Falha ao receber dados da API do Google Cloud. {e}")
        return ''
        


# def find_tilt_angle_hough(image):
#     img = image.copy()
#     img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     borders = cv2.Canny(img, 50, 150)

#     lines = cv2.HoughLinesP(borders, rho = 1, theta = 1*np.pi / 180, threshold=50, minLineLength=60, maxLineGap=10)
#     inclinations = []
#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             theta = np.arctan2(y2 - y1, x2 - x1)
#             inclinations.append((theta*180/np.pi))
#             cv2.line(img_color, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             mean_inclination = np.mean(inclinations)
#         return mean_inclination, img_color
#     else:
#         return 0, img


def find_tilt_angle_hough(image, inclinations_threshold=20, max_inclination=45):
    img = image.copy()
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    borders = cv2.Canny(img, 50, 150)

    lines = cv2.HoughLinesP(
        borders,
        rho=1,
        theta=1 * np.pi / 180,
        threshold=50,
        minLineLength=70,
        maxLineGap=50,
    )
    inclinations = []
    filtered_lines_inclination = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            theta = np.arctan2(y2 - y1, x2 - x1)
            inclinations.append((theta * 180 / np.pi))

        # Desvio padrão das inclinações
        std_dev = np.std(inclinations)

        filtered_lines = [
            lines[i]
            for i in range(len(lines))
            if abs(inclinations[i] - np.mean(inclinations)) <= inclinations_threshold
            and inclinations[i] <= max_inclination
        ]

        for line in filtered_lines:
            x1, y1, x2, y2 = line[0]
            theta = np.arctan2(y2 - y1, x2 - x1)
            filtered_lines_inclination.append((theta * 180 / np.pi))
            cv2.line(
                img_color,
                (x1, y1),
                (x2, y2),
                (
                    0,
                    255,
                ),
                2,
            )

        mean_inclination = np.mean(filtered_lines_inclination)
        return mean_inclination, img_color

    else:
        return 0, img


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
