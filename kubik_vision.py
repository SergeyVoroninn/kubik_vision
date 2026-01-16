import cv2
import numpy as np

import time
import json
import os
import sys
from kubik_color_detect import find_closest_bgr_color, detect_color,get_key_by_value

if len(sys.argv) < 2:
    mode = 'easy'
elif len(sys.argv) == 2:
    if sys.argv[1] not in ['easy','hard']:
        print("Invalid mode: it should be ['easy','hard'] or empty for 'easy' mode")
        sys.exit(1)
    mode = sys.argv[1]
else:
    print("Usage: python kubik_vision.py 'easy' OR 'hard'")

cap = cv2.VideoCapture(0)  # 0 — индекс камеры

# Проверяем, открылась ли камера
if not cap.isOpened():
    print("Не удалось открыть камеру")
else:
    # Получаем разрешение кадра
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # Ширина кадра
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # Высота кадра

wide_c = 200//3
x_min, y_min = int(width//2 - 1.5*wide_c), int(height//2 - 1.5*wide_c)
x_max, y_max = int(width//2 + 1.5*wide_c), int(height//2 + 1.5*wide_c)
rows, cols = 3, 3
contour = np.array([
    [[x_min, y_min]],        # левый верхний
    [[x_max, y_min]],        # правый верхний
    [[x_max, y_max]],        # правый нижний
    [[x_min, y_max]]         # левый нижний
])

wide = 35
x0 = wide//2
y0 = int(height) - int(wide*3.5)

if os.path.exists('calibration.json'):
    with open('calibration.json', 'r') as file:
        colors_bgr = json.load(file)
else:
    colors_bgr = {
        "white": (197, 193, 198),
        "red": (88, 80, 227),
        "green": (120, 181,87),
        "yellow": (108, 193, 204),
        "orange": (91, 107, 254),
        "blue": (179, 93, 54),
    }

color_to_face = {
    'white': 'U',
    'red': 'R',
    'green': 'F',
    'yellow': 'D',
    'orange': 'L',
    'blue': 'B'
}
face_to_fill = {
    'U': 'Empty',
    'R': 'Empty',
    'F': 'Empty',
    'D': 'Empty',
    'L': 'Empty',
    'B': 'Empty'
}
colors_bgr_keys = list(color_to_face.keys())
messages = {
    'U': 'top',
    'R': 'right',
    'F': 'front',
    'D': 'down',
    'L': 'left',
    'B': 'back'
}
# messages = ['show top','show right','show front','show down','show left','show back']
# file_names = ['top.jpg','right.jpg','front.jpg','down.jpg','left.jpg','back.jpg']

output_seq = []
detect_time = 0
cubik = cv2.imread('images/cubik.png')
cv2.imshow("Kubik Orientation", cubik)

while True:
    ret, frame = cap.read()
    temp_frame = frame.copy()
    key = cv2.waitKey(1) & 0xFF  

    if not ret:
        print("Не удалось получить кадр!")
        break
    
    # Определение времени
    current_time = time.time()

    # Определение карты цветов раз в 1 секунду
    if current_time - detect_time > 1.0:
        dominant_colors = detect_color(frame[y_min:y_max,x_min:x_max])
        color_map = [find_closest_bgr_color(color,colors_bgr) for color in dominant_colors]
        ccolor = color_map[4]
        detect_time = current_time

    # Сообщение о том, какую грань показывается
    cv2.putText(frame,'showing ' + messages[color_to_face[ccolor]], (x_min, y_min-15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5)
    cv2.putText(frame,'showing ' + messages[color_to_face[ccolor]], (x_min, y_min-15), cv2.FONT_HERSHEY_SIMPLEX, 1, colors_bgr[ccolor], 2)

    # Кнопка для сканирования грани
    cv2.putText(frame,str("<SPACE> to scan edge"), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    n_string =0
    # сообщение о нужной грани
    cv2.putText(frame,'require: ', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,100,255), 2)

    for keys,values in face_to_fill.items():
        if values == 'Empty':
            cur_color = get_key_by_value(color_to_face,keys)
            cv2.putText(frame, messages[keys], (10, 90 + n_string*30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 5)
            cv2.putText(frame, messages[keys], (10, 90 + n_string*30), cv2.FONT_HERSHEY_SIMPLEX, 1, colors_bgr[cur_color], 3)

        n_string +=1


    # нижние квадратики
    n=0
    for i in range(3):
        for j in range(3):
            x = x0 + j *wide
            y = y0 + i *wide
            cv2.rectangle(frame,
                          (x,y),
                          (x+wide,y+wide),
                          tuple(colors_bgr[color_map[n]]),
                          -1)
            n +=1

    cv2.putText(frame,str("Kubik:"), (10, y0 - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Центральная сетка для кубка
    for i in range(1, rows):
        y = y_min + (y_max - y_min) * i // rows
        cv2.line(frame, (x_min, y), (x_max, y), colors_bgr[ccolor], 1)

    for j in range(1, cols):
        x = x_min + (x_max - x_min) * j // cols
        cv2.line(frame, (x, y_min), (x, y_max), colors_bgr[ccolor], 1)

    # Центральный общий контур для кубка
    cv2.drawContours(frame, [contour], -1, colors_bgr[ccolor], 3)
    
    # Запись кадра + сохраненине color map
    if key == ord(' '):  # пробел
        cv2.imwrite(str('images/'+ messages[color_to_face[ccolor]]+'.jpg'), temp_frame[y_min:y_max,x_min:x_max]) #
        face_to_fill[color_to_face[ccolor]]= color_map

        print("Кадр сохранён!")
        if 'Empty' not in face_to_fill.values():
            # print(output_seq)
            break
            
    # Показ кадра
    cv2.imshow('Rubik Scanner', frame)
    # Обработка нажатия клавиши q (выход из программы)
    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
if 'Empty' not in face_to_fill.values():
    cube_string = ""
    for key,value in face_to_fill.items():
        for in_value in value:
            cube_string=cube_string+color_to_face[in_value]
    print(cube_string)

    # cube_state = 'LLLTTTTTTRRTRRTRRTFFFFFFFFFBBBBBBBBBDLLDLLDLLDDDDDDRRR'

    if mode == 'easy':
        import kociemba
        try:
            solution = kociemba.solve(cube_string)
            len_solution = len(solution.split(sep=" "))
            print(f"Solution: {solution} ({len_solution})")

        except Exception as e:
            print("Error:", str(e))

    elif mode =='hard':
        print('Mode hard not supported')
    #     import subprocess

    #     if os.exists(r"venv_pypy\Scripts\pypy3.exe"):
    #         pypy_executable = r"venv_pypy\Scripts\pypy3.exe"
    #     else:
    #         print(r"Pypy not found in <venv_pypy\Scripts\pypy3.exe>")
    #         print("Execute with same interpretaror with what was this script ran")
    #         pypy_executable = sys.executable
    #     # 2. Путь к скрипту, который нужно запустить
    #     script_to_run = "kubik_solver_hard.py"

    #     # 3. Запуск процесса
    #     try:
    #         # Передаем аргументы через список. 
    #         # check=True заставит Python выкинуть ошибку, если тот скрипт упадет.
    #         # capture_output=True позволяет прочитать то, что скрипт напечатал в консоль.
    #         result = subprocess.run(
    #             [pypy_executable, script_to_run, cube_string], 
    #             capture_output=True, 
    #             text=True, 
    #             encoding='utf-8',
    #             check=True
    #         )

    #         # Вывод результата из другой среды
    #         print("Solution:", result.stdout)

    #     except subprocess.CalledProcessError as e:
    #         print("Ошибка при выполнении скрипта в другой среде:")
    #         print(e.stderr)
    #     except FileNotFoundError:
    #         print("Не найден путь к интерпретатору PyPy. Проверьте путь.")