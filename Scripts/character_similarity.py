from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import json

def caractere_para_matriz(caractere, tamanho=(600, 900)):
    # Criação da imagem
    imagem = Image.new("1", tamanho, color=1)
    desenhador = ImageDraw.Draw(imagem)

    fonte = ImageFont.truetype(
        r"C:\Users\hiago\AppData\Local\Microsoft\Windows\Fonts\FE-FONT.TTF",
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
    print("Pixeis pretos caracter 1: ",np.sum(matriz1 == 0))
    print("Pixeis pretos caracter 2: ",np.sum(matriz2 == 0))

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

def exibe_grafico_caracteres():
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

def gera_dicionario_similaridade():
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"

    combinacoes = []
    for letra1 in alfabeto:

        for letra2 in alfabeto + numeros:
            combinacao = letra1 +"-"+ letra2
            combinacoes.append(combinacao)

    for numero1 in numeros:
        for numero2 in alfabeto + numeros:
            combinacao = numero1 +"-"+ numero2
            combinacoes.append(combinacao)

    dicionario = {}
    for combinacao in combinacoes:
        caracter1 = combinacao.split("-")[0]
        caracter2 = combinacao.split("-")[1]
        matriz_caracter1 = caractere_para_matriz(caracter1)
        matriz_caracter2 = caractere_para_matriz(caracter2)
        porcentagem_compartilhada = calcular_porcentagem_compartilhada(matriz_caracter1, matriz_caracter2)
        
        dicionario[f"('{caracter1}', '{caracter2}')"] = porcentagem_compartilhada

    json_string = json.dumps(dicionario, indent=4, ensure_ascii=False)

    #print(dicionario)
    #print("menor valor: ", min(dicionario.values()))
    with open(r"F:\Backup Arquivos\UFU\PFC2\Similaridade_caracteres.json", 'w', encoding='utf-8') as arquivo:
        arquivo.write(json_string)
    return dicionario


def normaliza_dicionario(dicionario):
    minimo = min(dicionario.values())
    maximo = max(dicionario.values())

    dicionario_normalizado = {
        chave: ((valor - minimo) / (maximo - minimo)) * 100 for chave, valor in dicionario.items()
    }

    # Imprimindo o dicionário normalizado
    print(dicionario_normalizado)
    print("Menor valor: ",min(dicionario_normalizado.values()) )

    json_string = json.dumps(dicionario_normalizado, indent=4, ensure_ascii=False)
    with open(r"F:\Backup Arquivos\UFU\PFC2\Similaridade_caracteres_normalizado.json", 'w', encoding='utf-8') as arquivo:
        arquivo.write(json_string)

    dicionario_filtrado = {chave: round(valor/100, 3) for chave, valor in dicionario_normalizado.items() if (valor >= 70 and valor < 100)}
    json_string_filtrado = json.dumps(dicionario_filtrado, indent=4, ensure_ascii=False)
    with open(r"F:\Backup Arquivos\UFU\PFC2\Similaridade_caracteres_normalizado_filtrado.json", 'w', encoding='utf-8') as arquivo:
        arquivo.write(json_string_filtrado)

def main():
    exibe_grafico_caracteres()
    #dicionario = gera_dicionario_similaridade()
    #normaliza_dicionario(dicionario)









# Loop para continuar a execução


if __name__== "__main__":
    main()
