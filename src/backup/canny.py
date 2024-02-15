import cv2
import numpy as np

# Carregue a imagem
imagem = cv2.imread('../../images/img2.jpeg')

# Converta a imagem para escala de cinza
imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplique um desfoque para reduzir o ruído
imagem_desfocada = cv2.GaussianBlur(imagem_cinza, (2, 2), 0)

# Use a detecção de bordas (por exemplo, Canny) para realçar as arestas
bordas = cv2.Canny(imagem_cinza, 50, 150)

# Aplique a transformada de Hough para detectar linhas
linhas = cv2.HoughLines(bordas, 1, np.pi / 180, 100)
inclinacoes = []
# Desenhe as linhas na imagem original e calcule a inclinação
for linha in linhas:
    rho, theta = linha[0]

    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(imagem, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Calcule e imprima a inclinação da linha
    angulo = 90 - theta*180/np.pi
    
    inclinacoes.append(angulo)


inclinacao_media = - np.mean(inclinacoes)
print(f'Inclinação da linha: {inclinacao_media:.2f}')
# Rotacione a imagem com base na inclinação média
altura, largura = imagem.shape[:2]
centro = (largura // 2, altura // 2)
matriz_rotacao = cv2.getRotationMatrix2D(centro, inclinacao_media, 1.0)
imagem_rotacionada = cv2.warpAffine(imagem, matriz_rotacao, (largura, altura), flags=cv2.INTER_LINEAR)




# Mostrar a imagem com as linhas detectadas
cv2.imshow('Desfoque', imagem_desfocada)
cv2.imshow('Canny', bordas)
cv2.imshow('Linhas Detectadas', imagem)
cv2.imshow('Imagem Rotacionada', imagem_rotacionada)
cv2.waitKey(0)
cv2.destroyAllWindows()