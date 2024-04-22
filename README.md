# Documentação do sistema de Deteção Automática de Placas Automotivas (ALPR) 
## PT-BR
Este sistema foi desenvolvido para o trabalho de conclusão de curso de Engenharia Eletrônica e de Telecomunicações da Universidade Federal de Uberlândia.

![image](https://github.com/hiagohsantos/ALPR/assets/98746083/975d5197-7e46-441d-b6e4-dc3361ca2410)

## Descrição

O sistema utiliza a biblioteca TensorFlow Lite para realizar a detecção de placas automotivas em imagens e a biblioteca TesseractOCR/serviço em nuvem Vision AI para extrair os textos dessas imagens. Além disso, implementa algoritmos de processamento de imagem, limiarização e correção de inclinação, juntamente com algoritimos de correção de códigos e calculo de similaridade. O sistema foi feito para operar sobre um Raspberry Pi 3B+.

## Diagrama do Sistema

Um diagrama simplificado do sistema pode ser visto na imagem abaixo:

![Diagrama do Sistema](https://github.com/hiagohsantos/ALPR/assets/98746083/f8004874-d71d-4619-ac37-4ba9a8c88082)

## Treinamento do Modelo

Para efetuar o treinamento do modelo, o script contido na pasta `Model-Maker` pode ser utilizado com base no banco de imagens da pasta `Database` para gerar novos modelos. A pasta `Models` contém alguns exemplos de modelos treinados para detecção de placas automotivas, inclusive o modelo utilizado pelo sistema.

## Monografia

Para mais detalhes sobre o trabalho e o sistema, consulte a monografia disponivel na pasta `Monography`.

# Automated License Plate Recognition (ALPR) System Documentation (EN-US)

This system was developed as the final project for the Electronic and Telecommunications Engineering course at the Federal University of Uberlândia.

![image](https://github.com/hiagohsantos/ALPR/assets/98746083/ac3ee790-0f4f-408f-b828-2fa520f95bde)

## Description

The system uses the TensorFlow Lite library to perform automatic license plate detection in images and the TesseractOCR/cloud service Vision AI library to extract text from these images. Additionally, it implements image processing algorithms, thresholding, and skew correction, along with code correction algorithms and similarity calculation. The system was designed to operate on a Raspberry Pi 3B+.

## System Diagram

A simplified diagram of the system can be seen in the image below:

![System Diagram](https://github.com/hiagohsantos/ALPR/assets/98746083/f8004874-d71d-4619-ac37-4ba9a8c88082)

## Model Training

To train the model, the script contained in the `Model-Maker` folder can be used based on the image database in the `Database` folder to generate new models. The `Models` folder contains some examples of models trained for license plate detection, including the model used by the system.

## Thesis

For further details about the work and the system, please refer to the monograph available in the 'Monography' folder.
