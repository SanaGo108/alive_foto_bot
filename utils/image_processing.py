import os
import cv2
from utils.animation import animate_face

def process_image(image_path):
    """Обработка изображения и создание анимации"""
    # Создаем анимацию лица
    output_path = image_path.replace(".jpg", "_animated.mp4")
    animate_face(image_path, output_path)
    return output_path