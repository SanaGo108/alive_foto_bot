import cv2
import numpy as np
import mediapipe as mp

def animate_face(image_path, output_path):
    """Создание 3D-анимации лица"""
    # Чтение изображения
    image = cv2.imread(image_path)

    # Подготовка MediaPipe для обработки лица
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)

    # Обработка изображения
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.multi_face_landmarks:
        raise ValueError("Лицо не найдено на изображении!")

    # Генерация простейшей анимации
    height, width, _ = image.shape
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

    for angle in range(-30, 30, 2):  # Поворот головы
        rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
        video.write(rotated_image)

    video.release()