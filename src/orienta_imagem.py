import cv2
import numpy as np
import matplotlib.pyplot as plt

def exibir_imagem_titulo(imagem, titulo, posicao):
    plt.subplot(2, 3, posicao)
    plt.imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    plt.title(titulo)
    plt.axis('off')

def corrigir_orientacao_imagem(imagem):
    # Converta a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplique uma operação de limiarização para destacar os contornos

    #_, imagem_limiarizada = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)
    #imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    # Encontre os contornos na imagem limiarizada
    contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    # Encontre o maior contorno (presumivelmente a placa do veículo)
    maior_contorno = max(contornos, key=cv2.contourArea)
    
    # Aplique a caixa delimitadora mínima para obter a inclinação
    retangulo = cv2.minAreaRect(maior_contorno)
    
    # Obtenha o ângulo de inclinação
    angulo_inclinacao = retangulo[-1]

    if (angulo_inclinacao > 45 ):
         angulo_inclinacao -= 90
        
    # Ajuste o ângulo para o intervalo -45 a 45 graus
    #angulo_inclinacao = angulo_inclinacao + 90 if angulo_inclinacao < -45 else angulo_inclinacao - 90

    # Rotacione a imagem para corrigir a inclinação
    altura, largura = imagem.shape[:2]
    matriz_rotacao = cv2.getRotationMatrix2D((largura / 2, altura / 2), angulo_inclinacao , 1)
    imagem_corrigida = cv2.warpAffine(imagem, matriz_rotacao, (largura, altura), flags=cv2.INTER_NEAREST)

    # Exibir a imagem original
    exibir_imagem_titulo(imagem, 'Imagem Original', 1)

    # Exibir a imagem em escala de cinza
    exibir_imagem_titulo(imagem_cinza, 'Imagem em Escala de Cinza', 2)

    # Exibir a imagem limiarizada
    exibir_imagem_titulo(imagem_limiarizada, 'Imagem Limiarizada', 3)

    # Desenhar contornos na imagem original
    imagem_contornos = imagem.copy()
    cv2.drawContours(imagem_contornos, [maior_contorno], -1, (0, 255, 0), 2)
    exibir_imagem_titulo(imagem_contornos, 'Contornos na Imagem Original', 4)

    # Desenhar a caixa delimitadora mínima na imagem original
    imagem_caixa = imagem.copy()
    pontos_caixa = cv2.boxPoints(retangulo).astype(int)
    cv2.drawContours(imagem_caixa, [pontos_caixa], 0, (0, 0, 255), 2)
    exibir_imagem_titulo(imagem_caixa, 'Caixa Delimitadora Mínima na Imagem Original', 5)

    # Exibir a imagem corrigida
    exibir_imagem_titulo(imagem_corrigida, 'Imagem Corrigida', 6)

    plt.show()

# Exemplo de uso
imagem_original = cv2.imread('../images/img10.jpeg')
corrigir_orientacao_imagem(imagem_original)
