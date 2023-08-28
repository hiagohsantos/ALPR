import customtkinter as ctk
from PIL import Image
import cv2
import time
import detect1


startTimeRec = 0
startTimeProgress = 0
decTime = 3
progress = 0

def tempo() -> None:
   global startTimeRec, progress
   startTimeRec = int(time.time()) 
   progress = 0


# Criaçao da janela raiz
root = ctk.CTk()
root.title("ALPR")
root.geometry('900x800+100+100')
root.resizable(False, False)
ctk.set_appearance_mode("dark")


# Criançao do frame onde é exibido o video
frame = ctk.CTkFrame(root,
                     width = 660,
                     height = 550,
                     fg_color = '#343436',
                     )
frame.place(in_ = root,
            y = 20,
            x = 20,
            )

frame2 = ctk.CTkFrame(root,
                     width = 200,
                     height = 550,
                     fg_color = '#343436',
                     )
frame2.place(in_ = root,
             x = 690,
             y = 20,
             )

frame3 = ctk.CTkFrame(root,
                     width = 870,
                     height = 200,
                     fg_color = '#343436',
                     )
frame3.place(in_ = root,
             x = 20,
             y = 580,
             )



# Criaçao do botao 1
btn1 = ctk.CTkButton(frame2,
                    text='Iniciar',
                    width= 180,
                    height= 50,
                    command=lambda: tempo(),
                    font = ctk.CTkFont(size = 20),
                    )

btn1.place(in_ = frame2,
           x = 10,
           y = 20,
          )

ctk.CTkLabel(frame, text = 'Câmera',font = ctk.CTkFont(size = 20)).place(in_=frame, relx = 0.45, y = 10)

videoCam = ctk.CTkLabel(frame,
                        text = '',
                        width = 640,
                        height = 480,
                        fg_color = '#3c3c3d',
                        )
videoCam.place(in_ = frame,
               x = 10,
               y = 50,
               )

switch_var = ctk.StringVar(value = 'on')

btn2 = ctk.CTkSwitch(frame,
                     text = '',
                     switch_width = 50,
                     switch_height = 25,
                     variable = switch_var,
                     onvalue = 'on',
                     offvalue = 'off',
                     )
btn2.place(in_ = frame,
           
           x = 600,
           y = 10,
           )

progressbar = ctk.CTkProgressBar(frame2, orientation="horizontal", width = 180, mode= 'determinate', determinate_speed = 1)
progressbar.set(progress)
progressbar.place(in_ = frame2,
                  x = 10,
                  y = 100,
                  )

ctk.CTkLabel(frame2, text = 'Coordenadas',font = ctk.CTkFont(size = 12)).place(in_ = frame2, x = 10 ,y = 125)

textStatus = ctk.CTkLabel(frame2, text = "", fg_color = '#3c3c3d', width = 180, height = 30)
textStatus.place(in_ = frame2,
              x = 10,
              y = 150)

# imagem de bacground da placa segmentada
image1 = cv2.imread("images/modelPlate.jpeg")
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGBA)
image1= cv2.resize(image1,(150,50),interpolation = cv2.INTER_AREA)
image1 = Image.fromarray(image1)

ctk.CTkLabel(frame2, text = 'Imagem Segmentada',font = ctk.CTkFont(size = 12)).place(in_ = frame2, x = 10 ,y = 420)
image1 = ctk.CTkImage(light_image=image1, dark_image=image1, size =(150,50))
placa = ctk.CTkLabel(frame2, image=image1, text='')
placa.place(in_ = frame2,
            x = 25,
            y = 450,
            )


def video():
    global startTimeProgress, progress
    imgCam = detect1.capture()
    
    # Inicia a detecçao com duraçao de 'decTime'
    if (startTimeRec + decTime) >= int(time.time()):

      # verificaçao para incrementar a barra de progresso
      if int(time.time()) > startTimeProgress:
        progress += 100/decTime
        progressbar.set(progress/100)
        progressbar.update_idletasks()
        startTimeProgress = int(time.time())
        
      # Inicia a detecçao de objetos
      result = detect1.detect(imgCam)
    
      if result.detections == []:
        textStatus.configure(text="Nada encontrado!")
      else:
        # Segmenta a imagem e redimensiona para 150x50 px
        segImage, text = detect1.segImage(imgCam.copy(), result)
        textStatus.configure(text=text)
        segImageRGB = cv2.resize(segImage,(150,50),interpolation = cv2.INTER_AREA)

        # Altera a imagem no label da placa
        imgSeg = Image.fromarray(segImageRGB)
        segImgtk = ctk.CTkImage(light_image=imgSeg,
                                dark_image=imgSeg,
                                size =(150,50),
                                )
        placa.configure(image=segImgtk)

        # Troca a imagem da camera para a imagem com o retangulo de detecçao
        img = detect1.visualize(imgCam, result)
        
    if switch_var.get() == 'on':

      # Altera a imagem no label do video
      img = imgCam
      img = Image.fromarray(img)
      imgtk = ctk.CTkImage(light_image=img,
                            dark_image=img,
                            size=(640, 480),
                          )     
      videoCam.configure(image = imgtk)
    else: 
      imgbck = cv2.imread("images/camBackground.jpg")
      imgbck = cv2.cvtColor(imgbck, cv2.COLOR_BGR2RGBA)
      imgbck = Image.fromarray(imgbck)
      imgbck = ctk.CTkImage(light_image = imgbck, dark_image = imgbck, size=(640, 480))
      videoCam.configure(image = imgbck)
      
    videoCam.after(2, video)


video()
root.mainloop()


    
    

    




