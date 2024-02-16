import customtkinter as ctk
from PIL import Image
import cv2
import time
from utils import utils
import concurrent.futures
import re
import numpy as np
import os


ctk.set_appearance_mode("dark")

class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = (1920 - 400) // 2
        y = (1080 - 800) // 2
        self.geometry(f"400x800+{x}+{y}")
        self.title("DADOS SALVOS")
        self.resizable(False, False)
        self.radiobutton_variable = ctk.StringVar()
        self.button_list = []
        self.checkbox_list = []
        self.components()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_data()

    def on_closing(self):
        self.save_data()
        self.destroy()

    def add_plate_code(self):
        string = self.plate_input.get().upper()
        self.plate_input.delete(first_index=0, last_index=100)
        if utils.is_valid_license_plate(string):
            self.add_item(string)
            self.alert_label.configure(text="Adicionado")
            self.alert_label.configure(text_color="#44fa41")
            self.alert_label.place(in_=self, x=130, y=700)
            self.after(3000, self.alert_label.place_forget)
        else:
            self.alert_label.configure(text="Formato incorreto")
            self.alert_label.configure(text_color="#ff554f")
            self.alert_label.place(in_=self, x=130, y=700)
            self.after(3000, self.alert_label.place_forget)

    def upper_text(self, event):
        self.entry_text.set(self.entry_text.get().upper())

    def components(self):
        self.entry_text = ctk.StringVar()
        self.title = ctk.CTkLabel(self, text= "Status\t Codigo ")
        self.scrollable_list = ctk.CTkScrollableFrame(master=self, width=365, height=680)
        self.plate_input = ctk.CTkEntry(self, placeholder_text="Codigo da placa", width=260, height=40, font=ctk.CTkFont(size=20), textvariable=self.entry_text)
        self.plate_input.bind("<KeyRelease>", self.upper_text)

        self.add_button = ctk.CTkButton(self, text="Adicionar", width=100, height=40, command=self.add_plate_code)
        self.alert_label = ctk.CTkLabel(self, text="", width=140, font=ctk.CTkFont(size=16), text_color='#3d3c3c', corner_radius=10, fg_color='#3d3c3c')

        self.title.place(in_=self, x=10, y=10)
        self.scrollable_list.grid_columnconfigure(0, weight=1)
        self.scrollable_list.grid(row=0, column=2, padx=10, pady=(40, 10), sticky="nsew")
        self.plate_input.place(in_=self, x=10, y=740)
        self.add_button.place(in_=self, x=285, y=740)

    def load_data(self):
        try:
            with open("data.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    data = line.split(":")
                    self.add_item(data[1], data[0])

        except FileNotFoundError as e:
            print('Erro ao abrir o arquivo: ', e)

    def save_data(self):
        try:
            with open("data.txt", "w") as file:
                for checkbox in self.checkbox_list:
                    file.write(f"{checkbox.get()}:{checkbox.cget('text')}\n")
                    

        except FileNotFoundError as e:
            print('Erro ao gravar o arquivo: ', e)


    def add_item(self, item, state=1):
        checkbox = ctk.CTkCheckBox(self.scrollable_list, text=item, font=ctk.CTkFont(size=20), text_color_disabled = "#707070")
        button = ctk.CTkButton(self.scrollable_list, text="Remover", width=100, font=ctk.CTkFont(size=16), height=30, fg_color = '#f5503d', hover_color = '#fc270f')
        button.configure(command=lambda: self.remove_item(item))
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)

        if state == '1':
            checkbox.select()

        self.checkbox_list.append(checkbox)
        self.button_list.append(button)

    def remove_item(self, item):
        for checkbox, button in zip(self.checkbox_list, self.button_list):
            if item == checkbox.cget("text"):
                checkbox.destroy()
                button.destroy()
                self.checkbox_list.remove(checkbox)
                self.button_list.remove(button)
                return

 

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
        self.inclination_type = ctk.IntVar(value=2)
        self.detection = False
        self.slider_reliability = ctk.IntVar(value=95)

        self.import_default_images()
        self.create_frames()
        self.create_cam_components()
        self.create_menu_components()
        self.create_bottonFrame_components()
        self.place_components()

        self.toplevel_window = None

        self.video()

    def __del__(self):
        pass

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self.root)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

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
                height=20,
                # command=lambda: self.capture_timer(),
                command=lambda: self.start_detection(),
                font=ctk.CTkFont(size=20),
            )
            self.modal_button = ctk.CTkButton(
                self.menu_frame,
                text="Adicionar Placas",
                width=180,
                height=20,
                # command=lambda: self.capture_timer(),
                command= self.open_toplevel,
                font=ctk.CTkFont(size=20),
            )

            self.radio_fixed_filter = ctk.CTkRadioButton(
                self.menu_frame, text="Limiar Fixo", variable=self.filter_type, value=1
            )
            self.radio_mean_filter = ctk.CTkRadioButton(
                self.menu_frame,
                text="Média da vizinhança",
                variable=self.filter_type,
                value=2,
            )
            self.radio_gaussian_filter = ctk.CTkRadioButton(
                self.menu_frame,
                text="Distribuição Gaussiana",
                variable=self.filter_type,
                value=3,
            )

            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=260)

            ctk.CTkLabel(
                self.menu_frame, width=180, text = "", height=2, fg_color="#575759", font=ctk.CTkFont(size=1)
            ).place(in_=self.menu_frame, x=10, y=360)

            self.radio_cloud_ocr = ctk.CTkRadioButton(
                self.menu_frame, text="Online", variable=self.ocr_type, value=1
            )
            self.radio_embedded_ocr = ctk.CTkRadioButton(
                self.menu_frame, text="Embarcado", variable=self.ocr_type, value=2
            )

            self.radio_inclination_hough = ctk.CTkRadioButton(
                self.menu_frame, text="Hough", variable=self.inclination_type, value=1
            )
            self.radio_inclination_rect = ctk.CTkRadioButton(
                self.menu_frame, text="Retangulo", variable=self.inclination_type, value=2
            )

            self.slider = ctk.CTkSlider(self.menu_frame, from_=0, to=100, width=180, variable = self.slider_reliability, command= self.slider_event).place(in_=self.menu_frame, x=10, y=520)

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
            ).place(in_=self.menu_frame, x=10, y=270)

            inclination_type = ctk.CTkLabel(
                self.menu_frame, text="Deteção da inclinação", font=ctk.CTkFont(size=12)
            ).place(in_=self.menu_frame, x=10, y=370)

            self.reliability_label = ctk.CTkLabel(
                self.menu_frame, text=f"Confiabilidade\t          {self.slider_reliability.get()} %", font=ctk.CTkFont(size=12)
            )

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
                self.botton_frame, text="", width=2, height=190, fg_color="#575759"
            ).place(in_=self.botton_frame, x=190, y=5)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color="#575759"
            ).place(in_=self.botton_frame, x=390, y=5)

            ctk.CTkLabel(
                self.botton_frame, text="", width=2, height=190, fg_color="#575759"
            ).place(in_=self.botton_frame, x=590, y=5)

            ## Left Images
            ctk.CTkLabel(
                self.botton_frame,
                text="Imagem Segmentada",
                font=ctk.CTkFont(size=12),
            ).place(in_=self.botton_frame, x=20, y=5)

            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame,
                text="",
                image=self.model_plate,
            )

            self.segmented_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )
            # Gray Plate
            self.gray_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )

            ## Center Images
            ctk.CTkLabel(
                self.botton_frame, text="Processamento", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=220, y=5)

            self.thresholded_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )

            self.rectangle_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )
            ## Right Images
            ctk.CTkLabel(
                self.botton_frame, text="Reorientação", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=420, y=5)

            self.reoriented_plate = ctk.CTkLabel(
                self.botton_frame, text="", bg_color="#3c3c3d", width=150, height=50
            )

            ctk.CTkLabel(
                self.botton_frame, text="Resultado do OCR", font=ctk.CTkFont(size=12)
            ).place(in_=self.botton_frame, x=620, y=5)

            self.ocr_result = ctk.CTkLabel(
                self.botton_frame,
                text="ABC2134",
                font=ctk.CTkFont(size=26),
                bg_color="#3c3c3d",
                width=150,
                height=50,
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
            self.modal_button.place(in_=self.menu_frame, x=10, y=40)

            self.textStatus.place(in_=self.menu_frame, x=10, y=100)

            self.radio_fixed_filter.place(in_=self.menu_frame, x=10, y=170)
            self.radio_mean_filter.place(in_=self.menu_frame, x=10, y=200)
            self.radio_gaussian_filter.place(in_=self.menu_frame, x=10, y=230)

            self.radio_cloud_ocr.place(in_=self.menu_frame, x=10, y=300)
            self.radio_embedded_ocr.place(in_=self.menu_frame, x=10, y=330)

            self.radio_inclination_hough.place(in_=self.menu_frame, x=10, y=400)
            self.radio_inclination_rect.place(in_=self.menu_frame, x=10, y=430)

            self.reliability_label.place(in_=self.menu_frame, x=10, y=490)

            # Botton Frame
            self.segmented_plate.place(in_=self.botton_frame, x=20, y=40)
            self.gray_plate.place(in_=self.botton_frame, x=20, y=120)
            self.thresholded_plate.place(in_=self.botton_frame, x=220, y=40)
            self.rectangle_plate.place(in_=self.botton_frame, x=220, y=120)
            self.reoriented_plate.place(in_=self.botton_frame, x=420, y=40)
            self.ocr_result.place(in_=self.botton_frame, x=620, y=40)

        except Exception as e:
            print(f"Falha ao colocar os componentes. {e}")

    def starts_asynchronous_ocr(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if self.ocr_type.get() == 1:
                future_ocr_text = executor.submit(utils.ocr_goole_cloud, image)
            elif self.ocr_type.get() == 2:
                future_ocr_text = executor.submit(utils.tesseract_ocr, image)

            ocr_text = future_ocr_text.result()
            self.ocr_result.configure(text=ocr_text)

    def starts_asynchronous_processing(self, image):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_thresholded_image = executor.submit(
                utils.threshold_image, image, self.filter_type.get()
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
                cropped_image = image.copy()


            future_reoriented_image = executor.submit(
                utils.rotate_image, cropped_image, tilt_angle
            )

            reoriented_image = future_reoriented_image.result()
            self.reoriented_plate.configure(
                image=self.tk_image(reoriented_image, 150, 50)
            )

            self.starts_asynchronous_ocr(reoriented_image)

    def starts_asynchronous_detection(self, frame):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(utils.detect, frame)
            result = future.result()
            if result.detections:
                # Segmenta a imagem e redimensiona para 150x50 px
                segImage, text = utils.segImage(frame.copy(), result)
                # cv2.imwrite(f"../captures/default/img-{time.time()}.png", cv2.cvtColor(segImage, cv2.COLOR_BGR2RGB))
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
                self.starts_asynchronous_processing(gray_image)

                # self.starts_asynchronous_ocr(segImageRGB)
                # Troca a imagem da camera para a imagem com o retangulo de detecçao
                img = utils.visualize(frame, result)
            else:
                self.textStatus.configure(text="Nada encontrado!")

    def video(self):
        frame, fps = utils.capture()
        self.fps_cam.configure(text=fps)
        if self.detection:
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
