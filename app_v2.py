#! /bin/env python3
import os
import sys
from ultra_lcd import *
from temp_lcd import *
from detect_mask import *
from servo import *
from smbus2 import SMBus
from mlx90614 import MLX90614
import simpleaudio as sa

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

mylcd = I2C_LCD_driver.lcd()

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO_TRIG = 18
GPIO_ECHO = 24


GPIO.setup(GPIO_TRIG, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


prototxtPath = "/home/pi/Desktop/Git/models/deploy.prototxt"
weightsPath =  "/home/pi/Desktop/Git/models/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

mylcd.lcd_clear()
mylcd.lcd_display_string("Initializing...", 1)
mylcd.lcd_display_string("Please Wait", 2, 2)
SetAngle(90)
print("Loading face mask detector model...")
maskNet = load_model("/home/pi/Desktop/Git/models/MaskDetector.h5")

print("Starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(1)

mask_detect = sa.WaveObject.from_wave_file("/home/pi/Desktop/Git/audios/mask_detect.wav")
high_temp = sa.WaveObject.from_wave_file("/home/pi/Desktop/Git/audios/high_temp.wav")
no_mask_detect = sa.WaveObject.from_wave_file("/home/pi/Desktop/Git/audios/no_mask_detect.wav")
normal_temp = sa.WaveObject.from_wave_file("/home/pi/Desktop/Git/audios/normal_temp.wav")
please_check_temp = sa.WaveObject.from_wave_file("/home/pi/Desktop/Git/audios/please_check_temp.wav")

if __name__ == '__main__':
    mylcd.lcd_clear()
    exit=True
    please_check_temp.play()
    try:
        while True:
            while exit==True:
                mylcd.lcd_display_string("Please Check", 1, 2)
                mylcd.lcd_display_string("Your Temperature", 2)
                dist = distance()
                print(dist)
                if dist <= 15 :
                    mylcd.lcd_clear()
                    objectTemp = sensor.get_object_1()      
                    if objectTemp > 30:
                        mylcd.lcd_display_string("HIGH Temperature!", 1, 3)
                        mylcd.lcd_display_string("NO ENTRY", 2, 4)
                        high_temp.play()
                        print("Temperature :", objectTemp)
                        print("High Temperature!!!")
                        time.sleep(5)
                        mylcd.lcd_clear()
                        exit=True
                    else:
                        print("Normal Temperature")
                        mylcd.lcd_display_string("Normal Temperature", 1)
                        mylcd.lcd_display_string("Please Proceed:", 2)
                        normal_temp.play()
                        time.sleep(5)
                        mylcd.lcd_clear()
                        while True:
                            mylcd.lcd_clear()                       
                            mylcd.lcd_display_string("Get Closer to",1)
                            mylcd.lcd_display_string("the Camera",2)
                            frame = vs.read()
                            frame = imutils.resize(frame, width = 240)
                            frame = cv2.flip(frame, flipCode = -1)
                            (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
                            for (box, pred) in zip(locs, preds):
                                (startX, startY, endX, endY) = box
                                (mask, withoutMask) = pred
                                if mask > withoutMask:
                                    mylcd.lcd_clear()
                                    mask_detect.play()
                                    mylcd.lcd_display_string("Mask Detected", 1)
                                    mylcd.lcd_display_string("Please Proceed", 2)
                                    SetAngle(180)
                                    print ("Going to next step")                                
                                    time.sleep(10)
                                    SetAngle(90)
                                    exit = True
                                    break
                                else:
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("NO MASK!", 1, 4)
                                    mylcd.lcd_display_string("NO ENTRY", 2, 4)
                                    no_mask_detect.play()
                                    print ("No Mask Detected")
                                    SetAngle(90)
                                    time.sleep(1)                            
                                    exit = True
                                    mylcd.lcd_clear()
                                    break
                            break
    except:
        cv2.destroyAllWindows()
        mylcd.lcd_clear()
        PWM.stop()
        vs.stop()
        print("Error encountered! Please reset the system")