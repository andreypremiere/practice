import cv2 as cv
import os

default_path = "./images/"


def input_int():
    """
    Создает целочисленное значение. При ошибке повторяет цикл до тех пор,
    пока пользователь не введет верный тип данных.
    :return: целочисленное значение
    """
    while True:
        try:
            value = int(input())
            return value
        except ValueError:
            print("Ошибка. Введите целочисленное значение")


def add_coordinates(img):
    """
    Выводит размер изображения. Запрашивает у пользователя значения для координат.
    Выполняет проверку, чтобы введенные значения не превышали допустимые.
    :param img: изображение
    :return: четыре значения, которые содержат начало и конец координат по осям X и Y
    """
    height, width = img.shape[:2]
    print(f"Размер изображения: высота - {height}, ширина - {width}")
    while True:
        print("Введите начало области по координате X: ")
        start_coordinate_x = input_int()
        if 0 <= start_coordinate_x < width:
            break
    while True:
        print("Введите конец области по координате X: ")
        finish_coordinate_x = input_int()
        if start_coordinate_x < finish_coordinate_x <= width:
            break
    while True:
        print("Введите начало области по координате Y: ")
        start_coordinate_y = input_int()
        if 0 <= start_coordinate_y < height:
            break
    while True:
        print("Введите конец области по координате Y: ")
        finish_coordinate_y = input_int()
        if start_coordinate_y <= finish_coordinate_y <= height:
            break
    return start_coordinate_x, finish_coordinate_x, start_coordinate_y, finish_coordinate_y


def save_img(img):
    """
    Сохраняет изображение в формате jpg в исходную папку, если это подтвердит пользователь.
    :param img: изображение
    :return: None
    """
    while True:
        choose_user = input("Хотите сохранить изображение:\n"
                            "a) да;\n"
                            "b) нет.\n")
        if choose_user == 'a':
            cv.imwrite(f'{default_path}{input("Введите название изображения: ")}.jpg', img)
            print('Изображение сохранено.')
            break
        elif choose_user == 'b':
            print('Изображение не сохранено')
            break
        else:
            print('Ошибка. Попробуйте еще раз.')


def get_image_file():
    """
    Проверяет расширение файла изображения, которое ввел пользователь.
    :return: название изображения в виде строки
    """
    while True:
        file_path = input("Введите название изображения, с которым хотите работать: ")
        if file_path.endswith('.jpg') or file_path.endswith('.png'):
            return file_path
        else:
            print("Файл может быть только типа .jpg или .png. Попробуйте заново.")


class Image:
    """Класс объединяет методы, которые используются для преобразования изображения,
    которое пользователь ввел раннее.

    Attributes
    ----------
    default_path : str
        путь к директории с изображениями
    img : str
        выбранное пользователем изображение

    Methods
    -------
    show_image() - выводит список изображений в папке
    image() - проверка наличия изображения
    one_channel_image() - выводит окно с изображением отдельного канала
    crop_image() - кадрирование изображения
    rotate_image() - вращение изображения
    rectangle_image() - рисует синий прямоугольник
    """
    def __init__(self):
        self.default_path = default_path
        self.img = None

    def show_image(self):
        """
        Выводит список файлов в директории.
        :return: None
        """
        print("\nФайлы в директории: ")
        for i in os.listdir(self.default_path):
            print(i)
        print("\nList end\n")

    def image(self):
        """
        Выполняет проверку наличия изображения в директории.
        :return: None
        """
        while True:
            self.img = get_image_file()
            if os.path.isfile(self.default_path+self.img):
                print("Изображение найдено")
                break
            else:
                print("Изображение не найдено")
        img = cv.imread(f'{self.default_path}{self.img}')
        cv.imshow('window', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def one_channel_image(self):
        """
        Выводит один из каналов изображения, в зависимости от выбора пользователя.
        :return: None
        """
        img = cv.imread(f'{self.default_path}{self.img}')
        blue = img.copy()
        green = img.copy()
        red = img.copy()
        blue[:, :, 1:] = 0
        green[:, :, 0] = 0
        green[:, :, 2] = 0
        red[:, :, :2] = 0
        while True:
            user_choose = input('Выберите канал:\n'
                                'a) Синий;\n'
                                'b) Зеленый;\n'
                                'c) Красный;\n'
                                'd) Назад.\n')
            if user_choose == 'a':
                cv.imshow('window', blue)
                cv.waitKey(0)
                cv.destroyAllWindows()
                save_img(blue)
            elif user_choose == 'b':
                cv.imshow('window', green)
                cv.waitKey(0)
                cv.destroyAllWindows()
                save_img(green)
            elif user_choose == 'c':
                cv.imshow('window', red)
                cv.waitKey(0)
                cv.destroyAllWindows()
                save_img(red)
            elif user_choose == 'd':
                break
            else:
                print('Ошибка. Введите значение заново')

    def crop_image(self):
        """
        Кадрирует изображение по координатам, которые ввел пользователь.
        :return: None
        """
        img = cv.imread(f'{self.default_path}{self.img}')
        start_coordinate_x, finish_coordinate_x, start_coordinate_y, finish_coordinate_y = add_coordinates(img)
        crop_img = img[start_coordinate_y:finish_coordinate_y, start_coordinate_x:finish_coordinate_x]
        cv.imshow("window", crop_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        save_img(crop_img)

    def rotate_image(self):
        """
        Вращает изображение вокруг центра на угол, который ввел пользователь,
        имеется возможность задать коэффициент приближения.
        :return: None
        """
        img = cv.imread(f'{self.default_path}{self.img}')
        h, w = img.shape[:2]
        center = w // 2, h // 2
        print("Введите угол поворота:")
        corner = input_int()
        print("Введите коэффициент приближения. Для значения по умолчанию нажмите Enter.")
        while True:
            coefficient_zoom = input()
            if coefficient_zoom == '':
                coefficient_zoom = 1.0
                break
            try:
                coefficient_zoom = float(coefficient_zoom)
                break
            except ValueError:
                print("Ошибка. Введите десятичное число.")
        mer = cv.getRotationMatrix2D(center, corner, coefficient_zoom)
        rotated = cv.warpAffine(img, mer, (w, h))
        cv.imshow('window', rotated)
        cv.waitKey(0)
        cv.destroyAllWindows()
        save_img(rotated)

    def rectangle_image(self):
        """
        Добавляет на изображение прямоугольник синего цвета. Координаты прямоугольника вводит пользователь.
        Есть возможность сделать прямоугольник заполненным или задать толщину линии.
        :return: None
        """
        img = cv.imread(f'{self.default_path}{self.img}')
        p1, p2, p3, p4 = add_coordinates(img)
        point_one = p1, p3
        point_two = p2, p4
        # black = (0, 0, 0)
        # white = (255, 255, 255)
        # red = (0, 0, 255)
        # green = (0, 255, 0)
        blue = (255, 0, 0)
        # cyan = (255, 255, 0)
        # magenta = (255, 0, 255)
        # yellow = (0, 255, 255)
        while True:
            print("Введите толщину линии. Введите '-1', если прямоугольник должен быть заполнен. ")
            width = input_int()
            if width < -1:
                continue
            else:
                break
        cv.rectangle(img, point_one, point_two, blue, width)
        cv.imshow('window', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        save_img(img)


# Вывод списка файлов в папке и выбор изображения
show = Image()
show.show_image()
show.image()

# Меню программы
while True:
    user_choice = input('Выберите действие:\n'
                        'a) Просмотреть изображения из папки;\n'
                        'b) Просмотреть определенный канал изображения;\n'
                        'c) Обрезать изображения;\n'
                        'd) Выполнить вращение изображение;\n'
                        'e) Нарисовать прямоугольник на изображении;\n'
                        'f) Выход из программы;\n'
                        'h) Изменить изображение для работы.\n')
    if user_choice == 'a':
        show.show_image()
    elif user_choice == 'b':
        show.one_channel_image()
    elif user_choice == 'c':
        show.crop_image()
    elif user_choice == 'd':
        show.rotate_image()
    elif user_choice == 'e':
        show.rectangle_image()
    elif user_choice == 'f':
        break
    elif user_choice == 'h':
        show.image()
    else:
        print('Некорректное значение. Попробуйте снова')
        continue
