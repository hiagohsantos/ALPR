## Descrição

O sistema utiliza a biblioteca TensorFlow Lite para realizar a detecção de placas automotivas em imagens e a biblioteca TesseractOCR para extrair os textos dessas imagens. Além disso, implementa algoritmos de correção e cálculo de similaridade de caracteres para os códigos detectados pelo OCR.

## Diagrama do Sistema

Um diagrama simplificado do sistema pode ser visto na imagem abaixo:

![Diagrama do Sistema](https://github.com/hiagohsantos/ALPR/assets/98746083/f8004874-d71d-4619-ac37-4ba9a8c88082)

## Treinamento do Modelo

Para efetuar o treinamento do modelo, o script contido na pasta `Model-Maker` pode ser utilizado com base no banco de imagens da pasta `Database` para gerar novos modelos. A pasta `Models` contém alguns exemplos de modelos treinados para detecção de placas automotivas, inclusive o modelo utilizado pelo sistema.

## Monografia

Para mais detalhes sobre o trabalho e o sistema, consulte a monografia associada.
