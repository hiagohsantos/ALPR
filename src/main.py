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
        self.filter_type = ctk.IntVar(value=2)
        self.ocr_type = ctk.IntVar(value=2)
        self.detection =  False

        self.import_default_images()
        self.create_frames()
        self.create_cam_components()
        self.create_menu_components()
        self.create_bottonFrame_components()
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
            self.radio_fixed_filter = ctk.CTkRadioButton(self.menu_frame, text="Limiar Fixo",
                                                         variable= self.filter_type, value=1)
            self.radio_mean_filter = ctk.CTkRadioButton(self.menu_frame, text="Média da vizinhança",
                                                         variable= self.filter_type, value=2)
            self.radio_gaussian_filter = ctk.CTkRadioButton(self.menu_frame, text="Distribuição Gaussiana",
                                                         variable= self.filter_type, value=3)

            self.radio_cloud_ocr = ctk.CTkRadioButton(self.menu_frame, text="Online",
                                                         variable= self.ocr_type, value=1)
            self.radio_embedded_ocr = ctk.CTkRadioButton(self.menu_frame, text="Embarcado",
                                                         variable= self.ocr_type, value=2)
            
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
            ).place(in_=self.menu_frame, x=10, y=75)

            filter_type = ctk.CTkLabel(
                self.menu_frame, text="Tipo de Limiarização", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=140)

            ocr_type = ctk.CTkLabel(
                self.menu_frame, text="Tipo de OCR", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=260)
            
            self.textStatus = ctk.CTkLabel(
                self.menu_frame, text="", fg_color="#3c3c3d", width=180, height=30
            )
            
        except Exception as e:
            print(f"Houve um problema ao criar os componentes do menu -> {e}")
            raise e

    def create_bottonFrame_components(self):
        try:
            ## Dividers
            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color= "#575759"
            ).place(in_=self.botton_frame, x=190, y=5)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color= "#575759"
            ).place(in_=self.botton_frame, x=390, y=5)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color= "#575759"
            ).place(in_=self.botton_frame, x=590, y=5)
            
            ## Left Images
            ctk.CTkLabel(
            self.botton_frame, text="Imagem Segmentada", font=ctk.CTkFont(size=12),
            ).place(in_=self.botton_frame, x=20, y=5)

            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame, text="",  image=self.model_plate,
            )

            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame, text="",  bg_color="#3c3c3d", width=150, height = 50
            )
            # Gray Plate
            self.gray_plate = ctk.CTkLabel(
                self.botton_frame, text="",  bg_color="#3c3c3d", width=150, height = 50
            )

            ## Center Images
            ctk.CTkLabel(
                self.botton_frame, text="Processamento", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=220, y=5)

            self.thresholded_plate = ctk.CTkLabel(
                self.botton_frame, text="",bg_color="#3c3c3d", width=150, height = 50
            )

            self.rectangle_plate = ctk.CTkLabel(
                self.botton_frame, text="",bg_color="#3c3c3d", width=150, height = 50
            )
            ## Right Images
            ctk.CTkLabel(
                self.botton_frame, text="Reorientação", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=420, y=5)

            self.reoriented_plate = ctk.CTkLabel(
                self.botton_frame,  text="",  bg_color="#3c3c3d", width=150, height =50   
            )

        except Exception as e:
            print("Houve um problema ao criar os componentes do frame base")
            raise e

    def place_components(self):
        try:
            # Cam Frame
            self.fps_cam.place(in_=self.cam_frame, relx=0.05, y=10)
            self.videoCam.place(in_=self.cam_frame, x=10, y=50)
            self.cam_switch.place(in_=self.cam_frame, x=600, y=10)

            # Menu Frame
            self.start_button.place(in_=self.menu_frame, x=10, y=20)
            #self.progressbar.place(in_=self.menu_frame, x=10, y=100)
            self.textStatus.place(in_=self.menu_frame, x=10, y=100)
            self.radio_fixed_filter.place(in_=self.menu_frame, x=10, y=170)
            self.radio_mean_filter.place(in_=self.menu_frame, x=10, y=200)
            self.radio_gaussian_filter.place(in_=self.menu_frame, x=10, y=230)
            self.radio_cloud_ocr.place(in_=self.menu_frame, x=10, y=290)
            self.radio_embedded_ocr.place(in_=self.menu_frame, x=10, y=320)
            # Botton Frame
            self.segmented_plate.place(in_=self.botton_frame, x=20, y=40)
            self.gray_plate.place(in_=self.botton_frame, x=20, y=120)
            self.thresholded_plate.place(in_=self.botton_frame, x=220, y=40)
            self.rectangle_plate.place(in_=self.botton_frame, x=220, y=120)
            self.reoriented_plate.place(in_=self.botton_frame, x=420, y=40)

        except Exception as e:
            print(f"Falha ao colocar os componentes. {e}")


    def starts_asynchronous_ocr(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(utils.tesseract_ocr, image)
            result = future.result()

    def starts_asynchronous_processing(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_thresholded_image = executor.submit(utils.threshold_image, image, self.filter_type.get())
            thresholded_image = future_thresholded_image.result()
            self.thresholded_plate.configure(image=self.tk_image(thresholded_image, 150, 50))

            future_image_contourns = executor.submit(utils.find_tilt_angle, thresholded_image)
            image_contourns, tilt_angle = future_image_contourns.result()
            self.rectangle_plate.configure(image=self.tk_image(image_contourns, 150, 50))

            future_reoriented_image = executor.submit(utils.rotate_image, thresholded_image, tilt_angle)
            reoriented_image = future_reoriented_image.result()
            self.reoriented_plate.configure(image=self.tk_image(reoriented_image,150, 50))

            
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
                gray_image = cv2.cvtColor(segImageRGB, cv2.COLOR_BGR2GRAY)
                self.gray_plate.configure(
                    image=self.tk_image(gray_image, 150, 50)
                )
                self.starts_asynchronous_processing(gray_image)
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
