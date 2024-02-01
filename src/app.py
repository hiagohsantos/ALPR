import customtkinter as ctk
from PIL import Image
import cv2
import time
import detect1 as detect1
#import easyOcr

root = ctk.CTk()

startTimeRec = 0
startTimeProgress = 0
decTime = 3
progress = 0

def tempo() -> None:
   global startTimeRec, progress
   startTimeRec = int(time.time()) 
   progress = 0

def tk_image(imagem, x, y):
    imagem = Image.fromarray(imagem)
    return  ctk.CTkImage(light_image=imagem, dark_image=imagem, size =(x, y))

# Criaçao da janela raiz

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

# Importanto e tratando a imagem modelo
imagem_modelo = cv2.cvtColor(cv2.imread("../images/modelPlate.jpeg"), cv2.COLOR_BGR2RGBA)
placa_modelo = Image.fromarray(cv2.resize(imagem_modelo,(150,50), interpolation = cv2.INTER_AREA))

# Tornando a imagem modelo em um objeto da Tkinter
placa_modelo = ctk.CTkImage(light_image=placa_modelo, dark_image=placa_modelo, size =(150,50))

# Placa segmentada
ctk.CTkLabel(frame2, text = 'Imagem Segmentada',font = ctk.CTkFont(size = 12)).place(in_ = frame2, x = 10 ,y = 180)
placa_segmentada = ctk.CTkLabel(frame2, image = placa_modelo, text = '')
placa_segmentada.place(in_ = frame2, x = 25, y = 210)

# Placa Limiarizada
ctk.CTkLabel(frame2, text = 'Imagem Limiarizada', font = ctk.CTkFont(size = 12)).place(in_ = frame2, x = 10 ,y = 270)
placa_limiarizada = ctk.CTkLabel(frame2, image=placa_modelo, text='')
placa_limiarizada.place(in_ = frame2, x = 25, y = 300)

# Placa Reorientada
ctk.CTkLabel(frame2, text = 'Imagem Reorientada', font = ctk.CTkFont(size = 12)).place(in_ = frame2, x = 10 ,y = 360)
placa_reorientada = ctk.CTkLabel(frame2, image=placa_modelo, text='')
placa_reorientada.place(in_ = frame2, x = 25, y = 390)


def processa_imagem(imagem):
    # Converta a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplique uma operação de limiarização para destacar os contornos

    #_, imagem_limiarizada = cv2.threshold(imagem_cinza, 128, 255, cv2.THRESH_BINARY)
    #imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    imagem_limiarizada  = cv2.adaptiveThreshold(imagem_cinza,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    placa_limiarizada.configure(image=tk_image(imagem_limiarizada,150, 50))

    # Encontre os contornos na imagem limiarizada
    contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #contornos, _ = cv2.findContours(imagem_limiarizada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    # Encontre o maior contorno (presumivelmente a placa do veículo)
    maior_contorno = max(contornos, key=cv2.contourArea)
    
    # Aplique a caixa delimitadora mínima para obter a inclinação
    retangulo = cv2.minAreaRect(maior_contorno)
    
    # Obtenha o ângulo de inclinação
    angulo_inclinacao = retangulo[-1]

    if (angulo_inclinacao > 45 ):
         angulo_inclinacao -= 90
      
    # Rotacione a imagem para corrigir a inclinação
    altura, largura = imagem.shape[:2]
    matriz_rotacao = cv2.getRotationMatrix2D((largura / 2, altura / 2), angulo_inclinacao , 1)
    imagem_corrigida = cv2.warpAffine(imagem, matriz_rotacao, (largura, altura), flags=cv2.INTER_NEAREST)
    placa_reorientada.configure(image=tk_image(imagem_corrigida,150, 50))
    
    # # Desenhar contornos na imagem original
    # imagem_contornos = imagem.copy()
    # cv2.drawContours(imagem_contornos, [maior_contorno], -1, (0, 255, 0), 2)
    
    # # Desenhar a caixa delimitadora mínima na imagem original
    # imagem_caixa = imagem.copy()
    # pontos_caixa = cv2.boxPoints(retangulo).astype(int)
    # cv2.drawContours(imagem_caixa, [pontos_caixa], 0, (0, 0, 255), 2)
    

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
        segImageRGB = cv2.resize(segImage,(150,50), interpolation = cv2.INTER_AREA)

        # substitui a imagem modelo pela imagem segmentada
        placa_segmentada.configure(image=tk_image(segImageRGB,150, 50))
        processa_imagem(segImageRGB)
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
      imgbck = cv2.imread("../images/camBackground.jpg")
      imgbck = cv2.cvtColor(imgbck, cv2.COLOR_BGR2RGBA)
      imgbck = Image.fromarray(imgbck)
      imgbck = ctk.CTkImage(light_image = imgbck, dark_image = imgbck, size=(640, 480))
      videoCam.configure(image = imgbck)
      
    videoCam.after(2, video)


video()
root.mainloop()


    
    

    




