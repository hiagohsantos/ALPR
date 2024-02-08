import customtkinter as ctk
from PIL import Image
import cv2
import time
from utils import utils
import concurrent.futures
import re

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

        self.detection =  False

        self.import_default_images()
        self.create_frames()
        self.create_cam_components()
        self.create_menu_components()
        self.place_components()
        
        self.video()
    

    def __del__(self):
        pass


    def import_default_images(self):
        self.cam_background = ctk.CTkImage(
            dark_image=Image.fromarray(
                cv2.cvtColor(
                    cv2.imread("../images/camBackground.jpg"), cv2.COLOR_BGR2RGBA
                )
            ), size=(640, 480)
        )

        self.model_plate = ctk.CTkImage(
                dark_image=Image.fromarray(
                cv2.resize(
                    cv2.cvtColor(
                        cv2.imread("../images/modelPlate.jpeg"), cv2.COLOR_BGR2RGBA
                    ),
                    (150, 50),
                    interpolation=cv2.INTER_AREA,
                )
            ), size=(150, 50)
            )

    def capture_timer(self) -> None:
        self.startTimeRec = int(time.time())
        self.progress = 0

    def start_detection(self) -> None:
        self.detection = True

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

            self.fps_cam = ctk.CTkLabel(
                self.cam_frame, text="", font=ctk.CTkFont(size=14)
            )
            

            self.videoCam = ctk.CTkLabel(
                self.cam_frame, text="", width=640, height=480, fg_color="#3c3c3d"
            )
            self.switch_variable = ctk.StringVar(value="on")
            self.cam_switch = ctk.CTkSwitch(
                self.cam_frame,
                text="",
                switch_width=40,
                switch_height=20,
                variable=self.switch_variable,
                onvalue="on",
                offvalue="off",
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
                #command=lambda: self.capture_timer(),
                command=lambda: self.start_detection(),
                font=ctk.CTkFont(size=20),
            )

            # Menu Widgets
            self.progressbar = ctk.CTkProgressBar(
                self.menu_frame,
                orientation="horizontal",
                width=180,
                mode="determinate",
                determinate_speed=1,
            )
            self.progressbar.set(self.progress)

            coord_label = ctk.CTkLabel(
                self.menu_frame, text="Coordenadas", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=125)
            
            self.textStatus = ctk.CTkLabel(
                self.menu_frame, text="", fg_color="#3c3c3d", width=180, height=30
            )
        
            # Segmented Plate Label
            ctk.CTkLabel(
                self.botton_frame, text="Imagem original", font=ctk.CTkFont(size=12),
            ).place(in_=self.botton_frame, x=20, y=5)

            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame, text="",  image=self.model_plate ,
            )
            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame, text="",  bg_color="#3c3c3d", width=150, height =50
            )

            ctk.CTkLabel(
                self.botton_frame, text="Limiarizacão", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=220, y=5)

            self.thresholded_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height =50 
            )
            ctk.CTkLabel(
                self.botton_frame, text="Reorientação", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=420, y=5)

            self.reoriented_plate = ctk.CTkLabel(
                self.botton_frame,  text="",  bg_color="#3c3c3d", width=150, height =50   
            )

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color= "#575759"
            ).place(in_=self.botton_frame, x=190, y=5)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color= "#575759"
            ).place(in_=self.botton_frame, x=390, y=5)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color= "#575759"
            ).place(in_=self.botton_frame, x=590, y=5)
            
        except Exception as e:
            print(f"Houve um problema ao criar os componentes do menu -> {e}")
            raise e

    def place_components(self):
        try:
            self.fps_cam.place(in_=self.cam_frame, relx=0.05, y=10)
            self.videoCam.place(in_=self.cam_frame, x=10, y=50)
            self.cam_switch.place(in_=self.cam_frame, x=600, y=10)

            self.start_button.place(in_=self.menu_frame, x=10, y=20)
            #self.progressbar.place(in_=self.menu_frame, x=10, y=100)
            self.textStatus.place(in_=self.menu_frame, x=10, y=150)

            self.segmented_plate.place(in_=self.botton_frame, x=20, y=60)
            self.thresholded_plate.place(in_=self.botton_frame, x=220, y=30)
            self.reoriented_plate.place(in_=self.botton_frame, x=420, y=30)
        except Exception as e:
            print(f"Falha ao colocar os componentes. {e}")

    def image_processing(self, image):
        # Gray image
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Aplique uma operação de limiarização para destacar os contornos
        #_, imagem_limiarizada = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)
        #imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        thresholded_image  = cv2.adaptiveThreshold(gray_image , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        self.thresholded_plate.configure(image=self.tk_image(thresholded_image,150, 50))
        # Encontre os contornos na imagem limiarizada
        contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Encontre o maior contorno (presumivelmente a placa do veículo)
        outer_contour = max(contours, key=cv2.contourArea)
        # Apique a caixa delimitadora mínima para obter a inclinação
        rectangle = cv2.minAreaRect(outer_contour)
        # Obtenha o ângulo de inclinação
        tilt_angle = rectangle[-1]

        if (tilt_angle > 45 ):
            tilt_angle -= 90

        # Rotacione a imagem para corrigir a inclinação
        height, width = image.shape[:2]
        rotation_matrix  = cv2.getRotationMatrix2D((width / 2, height / 2), tilt_angle , 1)

        reoriented_image = cv2.warpAffine(image, rotation_matrix, (width, height), flags=cv2.INTER_NEAREST)
        self.reoriented_plate.configure(image=self.tk_image(reoriented_image,150, 50))

        # # Desenhar contornos na imagem original
        # imagem_contornos = image.copy()
        # cv2.drawContours(imagem_contornos, [maior_contorno], -1, (0, 255, 0), 2)

        # # Desenhar a caixa delimitadora mínima na imagem original
        # imagem_caixa = image.copy()
        # pontos_caixa = cv2.boxPoints(retangulo).astype(int)
        # cv2.drawContours(imagem_caixa, [pontos_caixa], 0, (0, 0, 255), 2)

    def starts_asynchronous_ocr(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(utils.tesseract_ocr, image)
            result = future.result()
            print("Result:", result)
            if result:
                self.ocr_text.configure(text = re.sub(r'[^a-zA-Z0-9]', '', result))
            else:
                print("Nenhum texto retornado")
    
    def starts_asynchronous_detection(self, frame):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(utils.detect, frame)
            result = future.result()
            if result.detections:
                # Segmenta a imagem e redimensiona para 150x50 px
                segImage, text = utils.segImage(frame.copy(), result)
                #cv2.imwrite(f"../captures/default/img-{time.time()}.png", cv2.cvtColor(segImage, cv2.COLOR_BGR2RGB))
                self.textStatus.configure(text=text)
                segImageRGB = cv2.resize(
                    segImage, (150, 50), interpolation=cv2.INTER_AREA
                )

                # substitui a imagem modelo pela imagem segmentada
                self.segmented_plate.configure(
                    image=self.tk_image(segImageRGB, 150, 50)
                )
                self.image_processing(segImageRGB)
                #self.starts_asynchronous_ocr(segImageRGB)
                    
                # Troca a imagem da camera para a imagem com o retangulo de detecçao
                img = utils.visualize(frame, result)
            else:
                self.textStatus.configure(text="Nada encontrado!")

    def video(self):
        frame, fps = utils.capture()
        self.fps_cam.configure(text=fps)
        # Inicia a detecçao com duraçao de 'decTime'
        #if (self.startTimeRec + self.decTime) >= int(time.time()):
        if (self.detection):   
                # Inicia a detecçao de objetos
                self.starts_asynchronous_detection(frame)
                self.detection = False
                
        if self.switch_variable.get() == "on":
            imgtk = ctk.CTkImage(
                dark_image=Image.fromarray(frame),
                size=(640, 480),
            )
            self.videoCam.configure(image=imgtk)
        else:
            self.videoCam.configure(image=self.cam_background)
        self.videoCam.after(1, self.video)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ALPRapp().run()
