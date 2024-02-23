import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import time
from utils import utils, textUtils
from utils.addPlateWindow import ToplevelWindow
import concurrent.futures
import threading
import re
import numpy as np
import os
import RPi.GPIO as GPIO
import cv2

ctk.set_appearance_mode("dark")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button
GPIO.setup(11, GPIO.OUT) # Servo Motor
GPIO.setwarnings(False)



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
        # Variables
        self.filter_type = ctk.IntVar(value=2)
        self.ocr_type = ctk.IntVar(value=2)
        self.inclination_type = ctk.IntVar(value=1)
        self.apply_code_correction = ctk.IntVar(value=1)
        self.detection_type = ctk.IntVar(value=1)
        self.threshold_var = ctk.StringVar(value='127')
        self.slider_reliability = ctk.IntVar(value=95)

        self.detection = False
        self.frame_count_controller = 0
        self.data_detection = None
        self.authorization = False

        self.import_default_images()
        self.create_frames()
        self.create_cam_components()
        self.create_menu_components()
        self.create_bottonFrame_components()
        self.place_components()

        self.toplevel_window = None
        self.code_list = []
        self.load_data()
        self.load_images()
        
        self.servo = GPIO.PWM(11, 50) 
        self.servo.start(0)

        self.video()
        self.verify_button()
        self.root.mainloop()

    def __del__(self):
        self.servo.stop()
        GPIO.cleanup()
        
    
    def servo_motion(self, angle):
        try:
            print(f"mudando servo para {angle}")
            self.servo.ChangeDutyCycle(2+(angle/18))
            time.sleep(0.5)
            self.servo.ChangeDutyCycle(0)

        except Exeption as e:
            print('Falha ao mover o Servo Motor')

     
    def clear_interface(self):
        self.ocr_raw_text.configure(text='')
        self.result_text.configure(text = '')
        self.reliability_text.configure(text = '')
        self.ocr_result.configure(text='')
        self.ocr_result.configure(image= ctk.CTkImage(
                                  dark_image=Image.new("RGB", (1, 1), color="#3c3c3d"),
                                  size=(1,1)))
      

        self.textStatus.configure(text='')

        self.reoriented_plate.configure(image= None)
        self.rectangle_plate.configure(image= None)
        self.thresholded_plate.configure(image= None)
        self.gray_plate.configure(image= None)
        self.segmented_plate.configure(image= None)


    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    data = line.split(":")
                    if (data[0] == '1'):
                        self.code_list.append(data[1])

        except FileNotFoundError as e:
            print('Erro ao abrir o arquivo: ', e)

    def load_images(self):
        self.mercosul_model_plate = ctk.CTkImage(
                                  dark_image=Image.open("/home/pi/Desktop/ALPR/assets/images/mercosulPlate.png"),
                                  size=(186, 60))
        

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self.root)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
        
        self.root.wait_window(self.toplevel_window)
        # Retrieve the list when the ToplevelWindow is closed
        self.code_list = self.toplevel_window.save_data()


    def slider_event(self, value):
        if(self.slider_reliability.get() == 100):
            self.reliability_label.configure(text=f"Confiabilidade\t        {self.slider_reliability.get()} %")
        elif (self.slider_reliability.get() < 10):
            self.reliability_label.configure(text=f"Confiabilidade\t            {self.slider_reliability.get()} %")
        else:
            self.reliability_label.configure(text=f"Confiabilidade\t          {self.slider_reliability.get()} %")

    
    def import_default_images(self):
        self.cam_background = ctk.CTkImage(
            dark_image=Image.fromarray(
                cv2.cvtColor(
                    cv2.imread("../images/camBackground.jpg"), cv2.COLOR_BGR2RGBA
                )
            ),
            size=(640, 480),
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
            ),
            size=(150, 50),
        )

    def capture_timer(self) -> None:
        self.startTimeRec = int(time.time())
        self.progress = 0

    def timer(self):
        self.servo_motion(90)
        time.sleep(15)
        self.clear_interface()
        self.set_authorization(False)
        self.servo_motion(0)
        

    def set_authorization(self, status):
        
        self.authorization = status
        if self.authorization:
            timer_thread = threading.Thread(target=self.timer)
            timer_thread.start()
            

    def start_detection(self) -> None:
        self.clear_interface()
        if self.detection:
            self.detection = False
            if self.detection_type.get() == 3:
                self.start_button.configure(text = 'Iniciar')
                self.start_button.configure(fg_color = '#1f538d', hover_color = '#14375e')
                self.data_detection = None
        else:
            self.detection = True
            if self.detection_type.get() == 3:
                self.start_button.configure(fg_color = '#f26f66', hover_color ='#db4e44' )
                self.start_button.configure(text = 'Parar')

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

    def create_threshold_input(self):
        if(self.filter_type.get() == 1):
                self.threshold_value_text.place(in_=self.menu_frame, x=110, y=230)
                self.threshold.place(in_=self.menu_frame, x=150, y=230)
        else:
            self.threshold_value_text.place_forget()
            self.threshold.place_forget()

    def verify_threshold_value(self, event):
        if not re.match(r'^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]{1,2})$', self.threshold_var.get()):
            self.threshold_var.set("")

    def create_menu_components(self) -> None:
        try:
            # Start Button
            self.start_button = ctk.CTkButton(
                self.menu_frame,
                text="Iniciar",
                width=180,
                height=40,
                # command=lambda: self.capture_timer(),
                command=lambda: self.start_detection(),
                font=ctk.CTkFont(size=26),
            )
            self.start_button.place(in_=self.menu_frame, x=10, y=10)

            # Modal Button
            self.modal_button = ctk.CTkButton(
                self.menu_frame,
                text="Adicionar Placas",
                width=180,
                height=30,
                command= self.open_toplevel,
                font=ctk.CTkFont(size=18),
            )
            self.modal_button.place(in_=self.menu_frame, x=10, y=60)

            ### Detection trigger type
            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=100)

            ctk.CTkLabel(
                self.menu_frame, text="Tipo de detecção", font=ctk.CTkFont(size=12), width=200,
            ).place(in_=self.menu_frame, y=105)

            self.manual_detection = ctk.CTkRadioButton(
                self.menu_frame, text="Manual", variable=self.detection_type, value=1, radiobutton_width=18, radiobutton_height=18
            )
            self.manual_detection.place(in_=self.menu_frame, x=10, y=130)

            self.automatic_detection = ctk.CTkRadioButton(
                self.menu_frame,
                text="Automatica",
                variable=self.detection_type,
                value=2, radiobutton_width=18, radiobutton_height=18
            )
            self.automatic_detection.place(in_=self.menu_frame, x=10, y=150)

            self.continuous_detection = ctk.CTkRadioButton(
                self.menu_frame,
                text="Continua",
                variable=self.detection_type,
                value=3, radiobutton_width=18, radiobutton_height=18
            )
            self.continuous_detection.place(in_=self.menu_frame, x=10, y=170)

            ### Threshold type
            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=200)

            ctk.CTkLabel(
                self.menu_frame, text="Limiarização", font=ctk.CTkFont(size=12), width=200
            ).place(in_=self.menu_frame, y=205)

            self.radio_fixed_filter = ctk.CTkRadioButton(
                self.menu_frame, text="Fixa", variable=self.filter_type, value=1, radiobutton_width=18, radiobutton_height=18, command=self.create_threshold_input
            )
            self.threshold_value_text = ctk.CTkLabel(
                    self.menu_frame, text="Valor:",
                )
            self.threshold = ctk.CTkEntry(self.menu_frame,textvariable= self.threshold_var, width = 40, height = 18)
            self.threshold.bind("<KeyRelease>", self.verify_threshold_value)

            self.radio_fixed_filter.place(in_=self.menu_frame, x=10, y=230)

            self.radio_mean_filter = ctk.CTkRadioButton(
                self.menu_frame,
                text="Média",
                variable=self.filter_type,
                value=2, radiobutton_width=18, radiobutton_height=18,command=self.create_threshold_input
            )
            self.radio_mean_filter.place(in_=self.menu_frame, x=10, y=250)

            self.radio_gaussian_filter = ctk.CTkRadioButton(
                self.menu_frame,
                text="Gaussiana",
                variable=self.filter_type,
                value=3, radiobutton_width=18, radiobutton_height=18,command=self.create_threshold_input
            )
            self.radio_gaussian_filter.place(in_=self.menu_frame, x=10, y=270)

            ### OCR type
            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=300)

            ocr_type = ctk.CTkLabel(
                self.menu_frame, text="Tipo de OCR", font=ctk.CTkFont(size=12), width = 200
            ).place(in_=self.menu_frame, y=305)

            self.radio_cloud_ocr = ctk.CTkRadioButton(
                self.menu_frame, text="Nuvem", variable=self.ocr_type, value=1, radiobutton_width=18, radiobutton_height=18
            )
            self.radio_cloud_ocr.place(in_=self.menu_frame, x=10, y=330)

            self.radio_embedded_ocr = ctk.CTkRadioButton(
                self.menu_frame, text="Embarcado", variable=self.ocr_type, value=2, radiobutton_width=18, radiobutton_height=18
            )
            self.radio_embedded_ocr.place(in_=self.menu_frame, x=100, y=330)

            ### Tilt angle detection type
            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=360)

            inclination_type = ctk.CTkLabel(
                self.menu_frame, text="Deteção de inclinação", font=ctk.CTkFont(size=12), width=200
            ).place(in_=self.menu_frame, y=365)


            self.radio_inclination_hough = ctk.CTkRadioButton(
                self.menu_frame, text="Hough", variable=self.inclination_type, value=1, radiobutton_width=18, radiobutton_height=18
            )
            self.radio_inclination_hough.place(in_=self.menu_frame, x=10, y=390)

            self.radio_inclination_rect = ctk.CTkRadioButton(
                self.menu_frame, text="Retangulo", variable=self.inclination_type, value=2, radiobutton_width=18, radiobutton_height=18
            )
            self.radio_inclination_rect.place(in_=self.menu_frame, x=100, y=390)

            ### Replace OCR string
            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=420)

            inclination_type = ctk.CTkLabel(
                self.menu_frame, text="Corrigir codigo", font=ctk.CTkFont(size=12), width=200
            ).place(in_=self.menu_frame, y=425)

            self.radio_inclination_hough = ctk.CTkRadioButton(
                self.menu_frame, text="Sim", variable=self.apply_code_correction, value=1, radiobutton_width=18, radiobutton_height=18
            )
            self.radio_inclination_hough.place(in_=self.menu_frame, x=10, y=450)

            self.radio_inclination_rect = ctk.CTkRadioButton(
                self.menu_frame, text="Não", variable=self.apply_code_correction, value=2, radiobutton_width=18, radiobutton_height=18
            )
            self.radio_inclination_rect.place(in_=self.menu_frame, x=100, y=450)

        
            ### Reliability Slider
            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=480)

            self.slider = ctk.CTkSlider(self.menu_frame, from_=0, to=100, width=180, variable = self.slider_reliability, command= self.slider_event).place(in_=self.menu_frame, x=10, y=520)

            self.reliability_label = ctk.CTkLabel(
                self.menu_frame, text=f"Confiabilidade\t          {self.slider_reliability.get()} %", font=ctk.CTkFont(size=12)
            )
            self.reliability_label.place(in_=self.menu_frame, x=10, y=490)

        except Exception as e:
            print(f"Houve um problema ao criar os componentes do menu -> {e}")
            raise e

    def create_bottonFrame_components(self):
        try:
            ## Dividers
            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=160, fg_color="#575759"
            ).place(in_=self.botton_frame, x=195, y=35)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=160, fg_color="#575759"
            ).place(in_=self.botton_frame, x=395, y=35)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color="#575759"
            ).place(in_=self.botton_frame, x=600, y=5)

            
            self.textStatus = ctk.CTkLabel(
                self.botton_frame, text="", fg_color="#3c3c3d", width=150, height=50,font=ctk.CTkFont(size=14)
            )
            
            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame,
                text="",
                image=self.model_plate,
            )

            ## Labels
            ctk.CTkLabel(
                self.botton_frame, text="Processamento", font=ctk.CTkFont(size=14)
            ).place(in_=self.botton_frame, x=250, y=2)

            ctk.CTkLabel(
                self.botton_frame, text="Resultado", font=ctk.CTkFont(size=14)
            ).place(in_=self.botton_frame, x=700, y=2)

            ctk.CTkLabel(
                self.botton_frame, text="Coordenadas", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=20, y=30)

            ctk.CTkLabel(
                self.botton_frame, text="Escala de Cinza", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=220, y=30)

            ctk.CTkLabel(
                self.botton_frame, text="Imagem Limiarizada", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=220, y=115)

            ctk.CTkLabel(
                self.botton_frame, text="Detecção de Inclinação", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=420, y=30)

            ctk.CTkLabel(
                self.botton_frame, text="Imagem Reorientada", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=420, y=115)

            ctk.CTkLabel(
                self.botton_frame,
                text="Imagem Segmentada",
                font=ctk.CTkFont(size=12),
            ).place(in_=self.botton_frame, x=20, y=115)

            ## Images
            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )
                # Gray Plate
            self.gray_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )

            self.thresholded_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )

            self.rectangle_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )
    
            self.reoriented_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )

            self.ocr_raw_text = ctk.CTkLabel(
                self.botton_frame,
                text="",
                font=('FE-FONT', 12),
                width=186,
                height=15,
                pady = 5,
               
            )

            self.ocr_result = ctk.CTkLabel(
                self.botton_frame,
                image = None,
                text="",
                font=('FE-FONT', 32),
                bg_color="#3c3c3d",
                width=186,
                height=60,
                text_color = 'black',
            )

            self.reliability_text = ctk.CTkLabel(
                self.botton_frame, text="", font=ctk.CTkFont(size=12), width=190,
                height=15,
            )

            self.result_text = ctk.CTkLabel(
                self.botton_frame, text="", font=ctk.CTkFont(size=20), width=190,
                height=40,bg_color="#3c3c3d",
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

            # Botton Frame
            self.textStatus.place(in_=self.botton_frame, x=20, y=60)
            self.segmented_plate.place(in_=self.botton_frame, x=20, y=140)

            self.gray_plate.place(in_=self.botton_frame, x=220, y=60)
            self.thresholded_plate.place(in_=self.botton_frame, x=220, y=140)

            self.rectangle_plate.place(in_=self.botton_frame, x=420, y=60)
            self.reoriented_plate.place(in_=self.botton_frame, x=420, y=140)

            self.ocr_raw_text.place(in_=self.botton_frame, x=640, y=30)
            self.ocr_result.place(in_=self.botton_frame, x=640, y=50)
            self.reliability_text.place(in_=self.botton_frame, x=640, y=120)
            self.result_text.place(in_=self.botton_frame, x=640, y=140)

        except Exception as e:
            print(f"Falha ao colocar os componentes. {e}")

    def starts_asynchronous_ocr(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if self.ocr_type.get() == 1:
                future_ocr_text = executor.submit(utils.ocr_goole_cloud, image)
            elif self.ocr_type.get() == 2:
                future_ocr_text = executor.submit(utils.tesseract_ocr, image)

            ocr_text = future_ocr_text.result()
            if len(ocr_text) > 7:
                ocr_text = ocr_text[1:]
                if len(ocr_text) > 7:
                    ocr_text = ocr_text[:7]

            self.process_ocr_result(ocr_text)
            

    def starts_asynchronous_processing(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_thresholded_image = executor.submit(
                utils.threshold_image, image, self.filter_type.get(), int(self.threshold_var.get())
            )
            thresholded_image = future_thresholded_image.result()
            self.thresholded_plate.configure(
                image=self.tk_image(thresholded_image, 150, 50)
            )

            if self.inclination_type.get() == 2:
                future_image_contourns = executor.submit(
                    utils.find_tilt_angle, thresholded_image
                )
                image_contourns, tilt_angle, rectangle = future_image_contourns.result()
                self.rectangle_plate.configure(
                    image=self.tk_image(image_contourns, 150, 50)
                )

                box = cv2.boxPoints(rectangle).astype(int)
                box = np.intp(box)

                # Recorta a região dentro do retângulo
                min_x, min_y = np.min(box, axis=0)
                max_x, max_y = np.max(box, axis=0)
                cropped_image = thresholded_image[min_y:max_y, min_x:max_x]
            else:
                future_image_contourns = executor.submit(
                    utils.find_tilt_angle_hough, image
                )
                tilt_angle, canny_image = future_image_contourns.result()
                self.rectangle_plate.configure(
                    image=self.tk_image(canny_image, 150, 50)
                )
                
            future_reoriented_image = executor.submit(
                utils.rotate_image, image, tilt_angle
            )

            reoriented_image = future_reoriented_image.result()
            self.reoriented_plate.configure(
                image=self.tk_image(reoriented_image, 150, 50)
            )
            
            if not self.authorization:
                self.starts_asynchronous_ocr(reoriented_image)
           
    def starts_asynchronous_detection(self, frame):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(utils.detect, frame)
            result = future.result()
            if result.detections:
                # Segmenta a imagem e redimensiona para 150x50 px
                segImage, text, self.data_detection = utils.segImage(frame.copy(), result)
                self.textStatus.configure(text=text)
                segImageRGB = cv2.resize(
                        segImage, (150, 50), interpolation=cv2.INTER_AREA
                    )
                    # substitui a imagem modelo pela imagem segmentada
                self.segmented_plate.configure(
                        image=self.tk_image(segImageRGB, 150, 50)
                    )
                gray_image = cv2.cvtColor(segImageRGB, cv2.COLOR_BGR2GRAY)
                self.gray_plate.configure(image=self.tk_image(gray_image, 150, 50))
                
                # cv2.imwrite(f"../captures/default/img-{time.time()}.png", cv2.cvtColor(segImage, cv2.COLOR_BGR2RGB))
                self.starts_asynchronous_processing(gray_image)
                
            else:
                self.textStatus.configure(text="Nada encontrado!")
                self.textStatus.after(1000, lambda: self.textStatus.configure(text=""))
                self.data_detection = None


    def process_ocr_result(self, code):
        if len(code) == 7:
            if self.apply_code_correction.get() == 1:
                verified_code = textUtils.replace_ocr_code(code)
                if verified_code != code:
                    self.ocr_raw_text.configure(text=code)
                code = verified_code
            
            self.ocr_result.configure(text=code)
            self.ocr_result.configure(image=self.mercosul_model_plate)

            score, plate_code = textUtils.string_simitality(self.code_list, code)
            print(score, plate_code)

            if self.slider_reliability.get()/100 <= score:
                self.reliability_text.configure(text_color ='#44fa41', text = f'Similaridade: {int(score*100)}%')
                self.result_text.configure(text_color ='#44fa41', text = 'AUTORIZADO')
                self.set_authorization(True)

            elif(score > 0.57): # 4 characters
                self.reliability_text.configure(text_color ='#44fa41', text = f'Similaridade: {int(score*100)}%')
                self.result_text.configure(text_color ='#f1fa41', text = 'REJEITADO')
                self.set_authorization(False)
            else:
                self.reliability_text.configure(text_color ='#44fa41', text = f'')
                self.result_text.configure(text_color ='#ff554f', text = 'REJEITADO')
                self.set_authorization(False)
        else:
            self.ocr_result.configure(text='-------')
        


    def verify_button(self):
        if (GPIO.input(13) == GPIO.LOW) and not self.detection and self.detection_type.get() == 2:
            self.start_detection()
    
        self.root.after(100, self.verify_button)


    def video(self):
        self.frame_count_controller +=1
        frame, fps = utils.capture()
        self.fps_cam.configure(text=fps)

        if self.detection:
            if self.detection_type.get() == 3:
                if (self.frame_count_controller % 5 == 0):
                    self.starts_asynchronous_detection(frame)
            else:
                self.starts_asynchronous_detection(frame)
                self.detection = False
                self.data_detection = None

        if self.switch_variable.get() == "on":
            if self.data_detection:
                cv2.rectangle(
                frame,
                self.data_detection[0],
                self.data_detection[1],
                (0, 255, 0),
                2,
            )
                cv2.putText(
                frame,
                self.data_detection[2],
                self.data_detection[3],
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 255, 0),
                2,
            )

            imgtk = ctk.CTkImage(
                dark_image=Image.fromarray(frame),
                size=(640, 480),
            )
            self.videoCam.configure(image=imgtk)
        else:
            self.videoCam.configure(image=self.cam_background)
        self.videoCam.after(1, self.video)

   
        


if __name__ == "__main__":
    ALPRapp()
