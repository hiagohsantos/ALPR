import RPi.GPIO as GPIO
from time import sleep

# Configurar o modo GPIO e o pino do botão
GPIO.setmode(GPIO.BOARD)
pino_botao = 13  # Substitua pelo número do pino GPIO desejado
GPIO.setup(pino_botao, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def botao_clicado(channel):
    print("Botão clicado!")

# Configurar interrupção para o pino do botão
GPIO.add_event_detect(pino_botao, GPIO.FALLING, callback=botao_clicado, bouncetime=300)

try:
    print("Aguardando clique no botão. Pressione Ctrl+C para sair.")
    while True:
        sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
