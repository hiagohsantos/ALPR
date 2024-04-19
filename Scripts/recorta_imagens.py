import os
import cv2


def recortar_imagens_pasta(pasta, res_x, res_y):
    for nome_pasta in os.listdir(pasta):
        caminho_pasta = os.path.join(pasta, nome_pasta)

        if os.path.isdir(caminho_pasta):
            primeiro_arquivo = os.listdir(caminho_pasta)[3]
            nome_do_arquivo, extensao = os.path.splitext(primeiro_arquivo)

            img = cv2.imread(f"{caminho_pasta}\{nome_do_arquivo}.png")

            with open(f"{caminho_pasta}\{nome_do_arquivo}.txt", "r") as txt_file:
                for linha in txt_file:
                    if linha.startswith("position_plate:"):
                        position_plate = linha.strip().split(": ")[1]
                        x, y, w, h = map(int, position_plate.split(" "))

                        center_x = x + w // 2
                        center_y = y + h // 2

                        # Calcula as novas coordenadas para recorte
                        new_x = max(0, center_x - int(res_x / 2))
                        new_y = max(0, center_y - int(res_y / 2))
                        new_w = min(img.shape[1] - new_x, res_x)
                        new_h = min(img.shape[0] - new_y, res_y)

                        # Recorta a imagem
                        cropped_img = img[new_y : new_y + new_h, new_x : new_x + new_w]

                        # Redimensiona para 640x480
                        cropped_img = cv2.resize(cropped_img, (res_x, res_y))

                        # Salva a nova imagem
                        cv2.imwrite(
                            f"F:\ALPR\Imagens\{nome_do_arquivo}.jpg", cropped_img
                        )


if __name__ == "__main__":
    print("Inicio")
    pasta_raiz = r"C:\Users\hiago_o90hvbx\Desktop\validation"
    recortar_imagens_pasta(pasta_raiz, 1024, 720)
    print("fim")
