import cv2
from collections import Counter
import numpy as np

def get_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

def detect_color(img,k=3):
    """
    Делит изображение на 3x3 = 9 блоков и возвращает доминирующий цвет каждого.
    Всегда возвращает ровно 9 цветов.
    """
    len_y, len_x, _ = img.shape
    y_step = len_y // 3
    x_step = len_x // 3
    colors_massive = []

    for i in range(3):  
        for j in range(3):
            y_start = i * y_step
            y_end = (i + 1) * y_step if i != 2 else len_y  # на последнем блоке — до конца
            x_start = j * x_step
            x_end = (j + 1) * x_step if j != 2 else len_x

            roi = img[y_start:y_end, x_start:x_end]
            pixels = roi.reshape(-1, 3).astype(np.float32)
    
            # Define criteria and apply kmeans
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Count how many pixels are in each cluster
            counts = np.bincount(labels.flatten())
            
            # Return the center (color) of the largest cluster
            dominant_color = centers[np.argmax(counts)]
            colors_massive.append(tuple(map(int, dominant_color)))



            # pixels = roi.reshape(-1, 3)
            # pixels_tuple = [tuple(pixel) for pixel in pixels]
            # most_common = Counter(pixels_tuple).most_common(1)
            # colors_massive.append(most_common[0][0])

    return colors_massive  

def find_closest_bgr_color(target_bgr,colors_bgr):
    """
    Возвращает название цвета из эталонного списка, ближайшего к target_bgr.
    """

    target = np.array(target_bgr)
    values = list(colors_bgr.values())
    keys = list(colors_bgr.keys())

    distances = [np.linalg.norm(target - np.array(color)) for color in values]
    index = np.argmin(distances)

    return keys[index]


def detect_singlecolor(img):
    """
    Возвращает доминирующий цвет.
    """
    if img.size ==0 or img is None:
        return (255,255,255)
    
    # Reshape to a list of BGR colors
    pixels = img.reshape(-1, 3)
    # Use NumPy to find unique rows and their counts
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    
    # Get the color with the maximum count
    dominant_color = colors[counts.argmax()]

    # Добавляем только цвет (B, G, R)
    return tuple(map(int, dominant_color))


colors_bgr = {
    "white": (152, 147, 168),
    "red": (100, 96, 232),
    "green": (124, 188,92),
    "yellow": (108, 205, 215),
    "orange": (103, 113, 254),
    "blue": (184, 125, 93),
}
# image = cv2.imread('images/front.jpg', cv2.IMREAD_COLOR)

# dominant_colors = detect_color(image)
# color_map = [find_closest_bgr_color(color,colors_bgr) for color in dominant_colors]

# print(color_map)