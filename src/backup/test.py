import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import time

class CameraApp:
    def __init__(self, master, width, height, camera_index=0):
        self.master = master
        self.width = width
        self.height = height
        self.camera_index = camera_index
        self.fps = 0

        self.canvas = tk.Canvas(master, width=width, height=height)
        self.canvas.pack()

        self.stop_event = threading.Event()

        self.capture_thread = threading.Thread(target=self._capture_loop)
        self.capture_thread.start()

        master.protocol("WM_DELETE_WINDOW", self.on_close)

    def _capture_loop(self):
        cap = cv2.VideoCapture(self.camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        start_time = time.time()
        frames = 0

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)

            self.canvas.config(width=self.width, height=self.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.master.update_idletasks()

            frames += 1
            if frames >= 30:
                end_time = time.time()
                self.fps = frames / (end_time - start_time)
                start_time = end_time
                frames = 0

        cap.release()

    def on_close(self):
        self.stop_event.set()
        self.capture_thread.join()
        self.master.destroy()

def main():
    root = tk.Tk()
    root.title("Raspberry Pi Camera Viewer")

    width, height = 640, 480

    app = CameraApp(root, width, height)

    def update_fps():
        root.title(f"Raspberry Pi Camera Viewer - FPS: {app.fps:.2f}")
        root.after(1000, update_fps)

    update_fps()
    root.mainloop()

if __name__ == "__main__":
    main()
