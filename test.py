import os
import cv2 as cv


img = cv.imread('./images/cat.jpg')


def get_image_file():

    while True:
        file_path = input("Введите название изображения, с которым хотите работать: ")
        if file_path.endswith('.jpg') or file_path.endswith('.png'):
            return file_path, print('ok')
        else:
            print("Файл может быть только типа .jpg или .png. Попробуйте заново.")


get_image_file()


