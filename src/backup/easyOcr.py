import easyocr
from PIL import Image

def perform_ocr(image_path, language='en'):
    reader = easyocr.Reader([language], gpu=False)  # Defina gpu=True se estiver usando uma GPU no Raspberry Pi 4

    # Abra a imagem usando PIL
    image = Image.open(image_path)

    # Realize OCR na imagem
    results = reader.readtext(image)

    # Exiba os resultados
    for detection in results:
        text = detection[1]
        print(f'Texto: {text}')

if __name__ == "__main__":
    # Substitua "caminho/para/sua/imagem.jpg" pelo caminho real da sua imagem
    image_path = "../images/1.png"
    perform_ocr(image_path)
