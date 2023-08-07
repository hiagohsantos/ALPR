import customtkinter as ctk
from PIL import Image
import cv2
import time
import detect1


startTimeRec = 0
decTime = 5

def tempo() -> None:
   global startTimeRec
   startTimeRec = int(time.time()) 

# Criaçao da janela raiz
root = ctk.CTk()
root.title("ALPR")
root.geometry('1024x768')
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
             x = 700,
             y = 20,
             )

# Criaçao do botao 1
btn1 = ctk.CTkButton(frame2,
                    text='Iniciar',
                    width= 180,
                    height= 50,
                    command=lambda: tempo(),
                    font = ctk.CTkFont(size = 30),

                    )

btn1.place(in_ = frame2,
           x = 10,
           y= 20,
          )

ctk.CTkLabel(frame, text = 'Câmera',font = ctk.CTkFont(size = 20)).place(in_=frame,
                                           relx = 0.45,
                                           )


videoCam = ctk.CTkLabel(frame,
                        text = '',
                        width = 640,
                        height = 480,
                        bg_color = '#343436',
                        )
videoCam.place(in_ = frame,
               x = 10,
               y = 50,
               )

#image1 = Image.open("modelPlate.jpeg")
image1 = cv2.imread("images/modelPlate.jpeg")
image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGBA)
image1= cv2.resize(image1,(150,50),interpolation = cv2.INTER_AREA)
image1 = Image.fromarray(image1)

test = ctk.CTkImage(light_image=image1, dark_image=image1, size =(150,50))
placa = ctk.CTkLabel(frame2, image=test, text='')
placa.place(in_ = frame2,
            x = 25,
            y = 450,
            )



def video():
    
    imgCam = detect1.capture()
    
    # Inicia a detecçao com duraçao de 'decTime'
    if (startTimeRec + decTime) > int(time.time()):

      result = detect1.detect(imgCam)
      segImage = detect1.segImage(imgCam.copy(), result)
      img = detect1.visualize(imgCam, result)
      

      if len(segImage) == 0:
        print('Nada detectado!\n\n')
      else:
        
        segImageRGB = cv2.resize(segImage,(150,50),interpolation = cv2.INTER_AREA)

        # Altera a imagem no label da placa
        imgSeg = Image.fromarray(segImageRGB)
        segImgtk = ctk.CTkImage(light_image=imgSeg,
                                dark_image=imgSeg,
                                size =(150,50),
                                )
        placa.configure(image=segImgtk)
        

    # Altera a imagem no label do video
    img = imgCam
    img = Image.fromarray(img)
    imgtk = ctk.CTkImage(light_image=img,
                          dark_image=img,
                          size=(640, 480),
                        )     
    
    videoCam.configure(image=imgtk)
    videoCam.after(2, video)




video()
root.mainloop()


    
    

    




