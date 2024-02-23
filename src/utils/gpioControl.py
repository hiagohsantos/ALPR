import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
servo = GPIO.PWM(11, 50)
servo.start(0)


def servo_motion(angle):
    try:
        servo.ChangeDutyCycle(2 + (angle / 18))
        time.sleep(0.5)
        servo.ChangeDutyCycle(0)

    except Exeption as e:
        print("Falha ao mover o Servo Motor")

    finally:
        servo.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    servo_motion(90)
