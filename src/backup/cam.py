import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time

class CameraApp(tk.Tk):
    def __init__(self, camera_index=0):
        super().__init__()
        self.title("Camera App")

        # Inicializa a câmera
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.photo = None

        # Inicializa variáveis para o cálculo do FPS
        self.counter = 0
        self.start_time = time.time()
        self.fps = 0.0

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self)
        self.label.pack(padx=10, pady=10)

        self.btn_capture = tk.Button(self, text="Capturar", command=self.capture)
        self.btn_capture.pack(pady=10)

        self.btn_exit = tk.Button(self, text="Sair", command=self.destroy)
        self.btn_exit.pack(pady=10)

    def capture(self):
        # Captura um frame da câmera
        ret, frame = self.cap.read()
        #frame = cv2.flip(frame, -1)

        if ret:
            # Converte o frame para RGB (Pillow usa o formato RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Adiciona a lógica do contador de frames e FPS
            self.counter += 1
            if self.counter % 10 == 0:
                end_time = time.time()
                elapsed_time = end_time - self.start_time

                if elapsed_time > 0:
                    self.fps = 10 / elapsed_time
                else:
                    self.fps = 0.0

                self.start_time = end_time

            # Exibe o FPS na imagem
            fps_text = '{:.1f} fps'.format(self.fps)
            text_location = (24, 20)
            cv2.putText(frame_rgb, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

            # Atualiza a imagem exibida
            self.photo = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

            # Atualiza o rótulo com a nova imagem
            self.label.config(image=self.photo)
            self.label.image = self.photo

            # Agende a próxima chamada para capturar
            self.after(10, self.capture)


    def __del__(self):
        # Libera os recursos da câmera quando a janela for destruída
        self.cap.release()

def main():
    app = CameraApp(camera_index=0)
    app.mainloop()

if __name__ == "__main__":
    main()
