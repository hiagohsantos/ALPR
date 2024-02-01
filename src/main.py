import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import time

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
counter = 0
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

class ALPRApp(ctk.CTk):
    def __init__(self, camera_index: int = 0) -> None:
        super().__init__()
        self.title("ALPR PFC")
        self.geometry('900x800+100+100')
        self.resizable(False, False)

        # Inicializa a câmera
        # self.cap = cv2.VideoCapture(camera_index)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.photo = None

        # Inicializa variáveis para o cálculo do FPS
        self.start_time = time.time()
        self.counter = 0
        self.fps = 0

        # Constroi a interface
        self.create_widgets()
        

    def __del__(self):
        # Libera os recursos da câmera quando a janela for destruída
        self.cap.release()

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self,
                     width = 660,
                     height = 550,
                     fg_color = '#343436',
                     )
        self.frame.place(in_ = self,
                    y = 20,
                    x = 20,
                    )

        self.frame2 = ctk.CTkFrame(self,
                     width = 200,
                     height = 550,
                     fg_color = '#343436',
                     )
        self.frame2.place(in_ = self,
             x = 690,
             y = 20,
             )
        self.videoCam = ctk.CTkLabel(self.frame,
                        text = '',
                        width = 640,
                        height = 480,
                        fg_color = '#3c3c3d',
                        )
        self.videoCam.place(in_ = self.frame,
                    x = 10,
                    y = 50,
                    )
      
        # self.label = tk.Label(self)
        # self.label.pack(padx=10, pady=10)

        self.btn_capture = tk.Button(self.frame2, text="Capturar", command=self.capture)
        self.btn_capture.place(in_ = self.frame2,
           x = 10,
           y = 20,
          )

        # self.btn_exit = tk.Button(self, text="Sair", command=self.destroy)
        # self.btn_exit.pack(pady=10)
    
    def capture(self):
        global counter
        # Captura um frame da câmera
        
        #ret, frame = self.cap.read()
        #
        ret, frame = cap.read()
        counter += 1
        frame = cv2.flip(frame, -1)
        if ret:
            #Converte o frame para RGB (Pillow usa o formato RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Adiciona a lógica do contador de frames e FPS

              # Calcula o FPS
            if counter % 10 == 0:
                end_time = time.time()
                self.fps = 10 / (end_time - self.start_time)
                self.start_time = time.time()


            # self.counter += 1
            # if self.counter % 10 == 0:
            #     end_time = time.time()
            #     elapsed_time = end_time - self.start_time

            #     if elapsed_time > 0:
            #         self.fps = 10 / elapsed_time
            #     else:
            #         self.fps = 0.0

            #     self.start_time = end_time

            # Exibe o FPS na imagem
            fps_text = '{:.1f} fps'.format(self.fps)
            text_location = (24, 20)
            cv2.putText(frame_rgb, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

            img = Image.fromarray(frame_rgb)
            imgTk = ctk.CTkImage(light_image = img, dark_image = img, size=(640, 480))
            #self.videoCam.imgTks = imgTk
            # Atualiza o widget de vídeo diretamente
            self.videoCam.configure(image=imgTk)
            #self.videoCam.image = image  # Garante que a referência ao objeto Image seja mantida
            # Agende a próxima chamada para capturar
 
            self.after(2, self.capture)


        




def main():
    app = ALPRApp()
    app.mainloop()

if __name__ == "__main__":
    main()
