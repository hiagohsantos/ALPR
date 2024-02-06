import customtkinter as ctk
from PIL import Image
import cv2
import time
from utils import utils

ctk.set_appearance_mode("dark")


class ALPRapp:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.startTimeRec = 0
        self.startTimeProgress = 0
        self.decTime = 3
        self.progress = 0
        self.root.title("ALPR")
        self.root.geometry("900x800+100+100")
        self.root.resizable(False, False)

        self.create_frames()
        self.create_cam_components()
        self.create_menu_components()

        self.video()

    def __del__(self):
        pass

    def capture_timer(self) -> None:
        self.startTimeRec = int(time.time())
        self.progress = 0

    def tk_image(self, image, x, y):
        image = Image.fromarray(image)
        return ctk.CTkImage(light_image=image, dark_image=image, size=(x, y))

    def create_frames(self) -> None:
        try:
            # Root Frames
            self.cam_frame = ctk.CTkFrame(
                self.root, width=660, height=550, fg_color="#343436"
            )
            self.cam_frame.place(in_=self.root, y=20, x=20)

            self.menu_frame = ctk.CTkFrame(
                self.root, width=200, height=550, fg_color="#343436"
            )
            self.menu_frame.place(in_=self.root, x=690, y=20)

            self.botton_frame = ctk.CTkFrame(
                self.root, width=870, height=200, fg_color="#343436"
            )
            self.botton_frame.place(in_=self.root, x=20, y=580)
        except Exception as e:
            print(f"Houve um problema ao criar os Frames -> {e}")
            raise e

    def create_cam_components(self) -> None:
        try:
            # Cam widgets
            self.title_cam = ctk.CTkLabel(
                self.cam_frame, text="Câmera", font=ctk.CTkFont(size=20)
            ).place(in_=self.cam_frame, relx=0.45, y=10)

            self.videoCam = ctk.CTkLabel(
                self.cam_frame, text="", width=640, height=480, fg_color="#3c3c3d"
            )
            self.videoCam.place(in_=self.cam_frame, x=10, y=50)

            self.switch_variable = ctk.StringVar(value="off")
            self.cam_switch = ctk.CTkSwitch(
                self.cam_frame,
                text="",
                switch_width=50,
                switch_height=25,
                variable=self.switch_variable,
                onvalue="on",
                offvalue="off",
            )
            self.cam_switch.place(
                in_=self.cam_frame,
                x=600,
                y=10,
            )
        except Exception as e:
            print(f"Houve um problema ao criar os componentes da camera -> {e}")
            raise e

    def create_menu_components(self) -> None:
        try:
            # Start Button
            self.start_button = ctk.CTkButton(
                self.menu_frame,
                text="Iniciar",
                width=180,
                height=50,
                command=lambda: self.capture_timer(),
                font=ctk.CTkFont(size=20),
            )
            self.start_button.place(in_=self.menu_frame, x=10, y=20)

            # Menu Widgets
            self.progressbar = ctk.CTkProgressBar(
                self.menu_frame,
                orientation="horizontal",
                width=180,
                mode="determinate",
                determinate_speed=1,
            )
            self.progressbar.set(self.progress)
            self.progressbar.place(
                in_=self.menu_frame,
                x=10,
                y=100,
            )

            coord_label = ctk.CTkLabel(
                self.menu_frame, text="Coordenadas", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=125)

            self.textStatus = ctk.CTkLabel(
                self.menu_frame, text="", fg_color="#3c3c3d", width=180, height=30
            )
            self.textStatus.place(in_=self.menu_frame, x=10, y=150)

            # Model Image
            model_plate = Image.fromarray(
                cv2.resize(
                    cv2.cvtColor(
                        cv2.imread("../images/modelPlate.jpeg"), cv2.COLOR_BGR2RGBA
                    ),
                    (150, 50),
                    interpolation=cv2.INTER_AREA,
                )
            )
            model_plate = ctk.CTkImage(
                light_image=model_plate, dark_image=model_plate, size=(150, 50)
            )
            # Segmented Plate Label
            ctk.CTkLabel(
                self.menu_frame, text="Imagem Segmentada", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=180)
            self.segmented_plate = ctk.CTkLabel(
                self.menu_frame, image=model_plate, text=""
            )
            self.segmented_plate.place(in_=self.menu_frame, x=25, y=210)

            ctk.CTkLabel(
                self.menu_frame, text="Imagem Limiarizada", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=270)
            self.thresholded_plate = ctk.CTkLabel(
                self.menu_frame, image=model_plate, text=""
            )
            self.thresholded_plate.place(in_=self.menu_frame, x=25, y=300)

            ctk.CTkLabel(
                self.menu_frame, text="Imagem Reorientada", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=360)
            self.reoriented_plate = ctk.CTkLabel(
                self.menu_frame, image=model_plate, text=""
            )
            self.reoriented_plate.place(in_=self.menu_frame, x=25, y=390)

        except Exception as e:
            print(f"Houve um problema ao criar os componentes do menu -> {e}")
            raise e

        # def processa_imagem(imagem):
        #     # Converta a imagem para escala de cinza
        #     imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        #     # Aplique uma operação de limiarização para destacar os contornos

        #     #_, imagem_limiarizada = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)
        #     #imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        #     imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        #     placa_limiarizada.configure(image=tk_image(imagem_limiarizada,150, 50))

        #     # Encontre os contornos na imagem limiarizada
        #     contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #     #contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #     # Encontre o maior contorno (presumivelmente a placa do veículo)
        #     maior_contorno = max(contornos, key=cv2.contourArea)

        #     # Aplique a caixa delimitadora mínima para obter a inclinação
        #     retangulo = cv2.minAreaRect(maior_contorno)

        #     # Obtenha o ângulo de inclinação
        #     angulo_inclinacao = retangulo[-1]

        #     if (angulo_inclinacao > 45 ):
        #         angulo_inclinacao -= 90

        #     # Rotacione a imagem para corrigir a inclinação
        #     altura, largura = imagem.shape[:2]
        #     matriz_rotacao = cv2.getRotationMatrix2D((largura / 2, altura / 2), angulo_inclinacao , 1)
        #     imagem_corrigida = cv2.warpAffine(imagem, matriz_rotacao, (largura, altura), flags=cv2.INTER_NEAREST)
        #     placa_reorientada.configure(image=tk_image(imagem_corrigida,150, 50))

        #     # # Desenhar contornos na imagem original
        #     # imagem_contornos = imagem.copy()
        #     # cv2.drawContours(imagem_contornos, [maior_contorno], -1, (0, 255, 0), 2)

        #     # # Desenhar a caixa delimitadora mínima na imagem original
        #     # imagem_caixa = imagem.copy()
        #     # pontos_caixa = cv2.boxPoints(retangulo).astype(int)
        #     # cv2.drawContours(imagem_caixa, [pontos_caixa], 0, (0, 0, 255), 2)

    def video(self):

        imgCam = utils.capture()
        # Inicia a detecçao com duraçao de 'decTime'
        if (self.startTimeRec + self.decTime) >= int(time.time()):

            # verificaçao para incrementar a barra de progresso
            if int(time.time()) > self.startTimeProgress:
                self.progress += 100 / self.decTime
                self.progressbar.set(self.progress / 100)
                self.progressbar.update_idletasks()
                self.startTimeProgress = int(time.time())

            # Inicia a detecçao de objetos
            result = utils.detect(imgCam)

            if result.detections == []:
                self.textStatus.configure(text="Nada encontrado!")
            else:
                # Segmenta a imagem e redimensiona para 150x50 px
                segImage, text = utils.segImage(imgCam.copy(), result)
                self.textStatus.configure(text=text)
                segImageRGB = cv2.resize(
                    segImage, (150, 50), interpolation=cv2.INTER_AREA
                )

                # substitui a imagem modelo pela imagem segmentada
                self.segmented_plate.configure(
                    image=self.tk_image(segImageRGB, 150, 50)
                )
                # processa_imagem(segImageRGB)
                # Troca a imagem da camera para a imagem com o retangulo de detecçao
                img = utils.visualize(imgCam, result)

        if self.switch_variable.get() == "on":
            # Altera a imagem no label do video
            img = imgCam
            img = Image.fromarray(img)
            imgtk = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(640, 480),
            )
            self.videoCam.configure(image=imgtk)
        else:
            imgbck = Image.fromarray(
                cv2.cvtColor(
                    cv2.imread("../images/camBackground.jpg"), cv2.COLOR_BGR2RGBA
                )
            )
            imgbck = ctk.CTkImage(
                light_image=imgbck, dark_image=imgbck, size=(640, 480)
            )
            self.videoCam.configure(image=imgbck)
        self.videoCam.after(1, self.video)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ALPRapp().run()
