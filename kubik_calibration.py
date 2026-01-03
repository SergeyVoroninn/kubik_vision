import numpy as np
import cv2
import time
import json
from testing_color_detect import detect_singlecolor

config_name = 'calibration.json'
config = {}
detect_time = time.time()

messages = ['white','yellow','orange','red','green','blue']
# прямоугольник для поиска

cap = cv2.VideoCapture(0)  # 0 — индекс камеры
ret,frame = cap.read()
len_y,len_x,_ = frame.shape
center_y = len_y//2
center_x = len_x//2

n_calibration = 0
wide = 50
colors_bgr = {
    "white": (255, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255,0),
    "yellow": (0, 255, 255),
    "orange": (0, 122, 255),
    "blue": (255, 0, 0),
}


while True:
    ret,frame = cap.read()
    current_time = time.time()
    key = cv2.waitKey(1) & 0xFF 

    if ret == False:
        print("Не удалось получить кадр!")
        break

    if key == ord('q'):
        break

    if key == ord(' '):
        config[messages[n_calibration]] = tuple(found_color)
        n_calibration+=1
        
        if n_calibration == 6:
            break

    if current_time - detect_time > 1.0:
        found_color = detect_singlecolor(frame[center_y-wide:center_y+wide,center_x-wide:center_x+wide]) # абсолютно не работает
        detect_time = current_time

    cv2.putText(frame,str("Result of calibration"), (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(frame,
                (0,370),
                (wide*2,370+wide*2),
                found_color, # абсолютно работает
                -1)
    cv2.putText(frame,str("<SPACE> to make calibration"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame,str("Place " + messages[n_calibration] + " cell into the center"), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, colors_bgr[messages[n_calibration]], 2)
    cv2.rectangle(frame,
                (center_x-wide,center_y-wide),
                (center_x+wide,center_y+wide),
                (255, 0, 0),
                3)
    cv2.imshow('Rubik Scanner', frame)

cap.release()
cv2.destroyAllWindows()
if n_calibration ==6:
    with open(config_name, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

    print("Конфигурация сохранена в config.json")