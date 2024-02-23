from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt


def caractere_para_matriz(caractere, tamanho=(600, 900)):
    # Criação da imagem
    imagem = Image.new("1", tamanho, color=1)
    desenhador = ImageDraw.Draw(imagem)

    fonte = ImageFont.truetype(
        r"C:\Users\hiago_o90hvbx\AppData\Local\Microsoft\Windows\Fonts\font.ttf",
        size=1000,
    )

    largura, altura = desenhador.textsize(caractere, font=fonte)
    x = (tamanho[0] - largura) / 2
    y = (tamanho[1] - altura) / 2

    desenhador.text((x, y - 30), caractere, font=fonte, fill=0)

    matriz = np.array(imagem)
    return matriz


def calcular_porcentagem_compartilhada(matriz1, matriz2):
    # Conta quantos pixels são idênticos nas duas matrizes
    pixels_compartilhados = np.sum((matriz1 == matriz2))
    # Calcula a porcentagem de pixels compartilhados
    total_pixels = matriz1.size
    porcentagem_compartilhada = ((pixels_compartilhados / total_pixels)) * 100

    return porcentagem_compartilhada


def gerar_terceiro_grafico(matriz1, matriz2):
    # Cria uma nova matriz com os pixels que são 1 em ambas as letras (XOR lógico)
    matriz_comum = np.logical_and(matriz1 == 0, matriz2 == 0).astype(int)
    # Inverte a matriz
    matriz_comum = np.logical_not(matriz_comum).astype(int)

    # Exibe o terceiro gráfico
    plt.subplot(1, 3, 3)
    plt.imshow(matriz_comum, cmap="gray", interpolation="nearest")
    plt.title("Pixels Comuns")


# Loop para continuar a execução
while True:
    # Solicita as letras ao usuário
    letra1 = input("Insira a primeira letra ('exit' para sair): ")

    # Verifica se o usuário deseja sair
    if letra1.lower() == "exit":
        break

    letra2 = input("Insira a segunda letra: ")

    # Obtém as matrizes para cada letra
    matriz_letra1 = caractere_para_matriz(letra1)
    matriz_letra2 = caractere_para_matriz(letra2)

    # Exibe as letras em gráficos separados
    plt.subplot(1, 3, 1)
    plt.imshow(matriz_letra1, cmap="gray", interpolation="nearest")
    plt.title(f'Caractere "{letra1}"')

    plt.subplot(1, 3, 2)
    plt.imshow(matriz_letra2, cmap="gray", interpolation="nearest")
    plt.title(f'Caractere "{letra2}"')

    # Calcula e exibe a porcentagem de pixels compartilhados
    porcentagem_compartilhada = calcular_porcentagem_compartilhada(
        matriz_letra1, matriz_letra2
    )
    plt.suptitle(
        f"Similaridade: {porcentagem_compartilhada:.2f}%",
        y=0.92,
        fontsize=12,
        ha="center",
    )

    # Gera o terceiro gráfico
    gerar_terceiro_grafico(matriz_letra1, matriz_letra2)

    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.show()
