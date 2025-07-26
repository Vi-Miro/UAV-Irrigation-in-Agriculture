import tkinter as tk
from tkinter import ttk, messagebox
import math


class DroneCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет координат объекта с БПЛА")
        self.root.name = "drone_calculator_main_window"

        # Инициализация переменных с установкой значений по умолчанию в допустимых диапазонах
        self.declination = tk.DoubleVar(value=0.0)  # 0-26
        self.convergence = tk.DoubleVar(value=0.0)  # 0-3
        self.self_x = tk.DoubleVar(value=0.0)  # 0-10000
        self.self_y = tk.DoubleVar(value=0.0)  # 0-10000

        self.camera_angle = tk.DoubleVar(value=0.0)  # -90 до 56
        self.lazer_distance = tk.DoubleVar(value=0.0)  # до 1200
        self.magnetic_course = tk.DoubleVar(value=0.0)  # 0-360

        # Создаем основной фрейм для всех элементов
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Разделитель для параметров подготовки
        ttk.Label(self.main_frame, text="Параметры подготовки", font=('Helvetica', 10, 'bold')).grid(row=0, column=0,
                                                                                                     columnspan=3,
                                                                                                     pady=(0, 5),
                                                                                                     sticky="w")

        # Магнитное склонение (0-26)
        ttk.Label(self.main_frame, text="Магнитное склонение (0-26):").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.declination, width=10).grid(row=1, column=1, padx=5, pady=2,
                                                                                 sticky="w")
        ttk.Label(self.main_frame, text="град.").grid(row=1, column=2, padx=5, pady=2, sticky="w")

        # Среднее сближение (0-3)
        ttk.Label(self.main_frame, text="Среднее сближение (0-3):").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.convergence, width=10).grid(row=2, column=1, padx=5, pady=2,
                                                                                 sticky="w")
        ttk.Label(self.main_frame, text="град.").grid(row=2, column=2, padx=5, pady=2, sticky="w")

        # Координаты взлета (0-10000)
        ttk.Label(self.main_frame, text="Координаты взлета X (0-10000):").grid(row=3, column=0, padx=5, pady=2,
                                                                               sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.self_x, width=10).grid(row=3, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(self.main_frame, text="Координаты взлета Y (0-10000):").grid(row=4, column=0, padx=5, pady=2,
                                                                               sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.self_y, width=10).grid(row=4, column=1, padx=5, pady=2, sticky="w")

        # Разделительная линия
        ttk.Separator(self.main_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        # Разделитель для параметров полета
        ttk.Label(self.main_frame, text="Параметры полета", font=('Helvetica', 10, 'bold')).grid(row=6, column=0,
                                                                                                 columnspan=3,
                                                                                                 pady=(0, 5),
                                                                                                 sticky="w")

        # Угол наклона камеры (-90 до 56)
        ttk.Label(self.main_frame, text="Угол наклона камеры (-90 до 56):").grid(row=7, column=0, padx=5, pady=2,
                                                                                 sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.camera_angle, width=10).grid(row=7, column=1, padx=5, pady=2,
                                                                                  sticky="w")
        ttk.Label(self.main_frame, text="град.").grid(row=7, column=2, padx=5, pady=2, sticky="w")

        # Показания дальномера (до 1200 м)
        ttk.Label(self.main_frame, text="Показания дальномера (0-1200):").grid(row=8, column=0, padx=5, pady=2,
                                                                               sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.lazer_distance, width=10).grid(row=8, column=1, padx=5, pady=2,
                                                                                    sticky="w")
        ttk.Label(self.main_frame, text="м").grid(row=8, column=2, padx=5, pady=2, sticky="w")

        # Магнитный курс (0-360)
        ttk.Label(self.main_frame, text="Магнитный курс (0-360):").grid(row=9, column=0, padx=5, pady=2, sticky="e")
        ttk.Entry(self.main_frame, textvariable=self.magnetic_course, width=10).grid(row=9, column=1, padx=5, pady=2,
                                                                                     sticky="w")
        ttk.Label(self.main_frame, text="град.").grid(row=9, column=2, padx=5, pady=2, sticky="w")

        # Кнопка расчета
        ttk.Button(self.main_frame, text="Рассчитать координаты", command=self.calculate).grid(row=10, column=0,
                                                                                               columnspan=3, pady=10)

        # Вывод результата
        self.result_label = ttk.Label(self.main_frame, text="Координаты объекта: (X, Y) = ", font=('Helvetica', 10))
        self.result_label.grid(row=11, column=0, columnspan=3, pady=5)

    def validate_input(self):
        """Проверка всех входных параметров на соответствие допустимым диапазонам"""
        try:
            # Проверка параметров подготовки
            declination = self.declination.get()
            if not 0 <= declination <= 26:
                raise ValueError("Магнитное склонение должно быть в диапазоне 0-26 градусов")

            convergence = self.convergence.get()
            if not 0 <= convergence <= 3:
                raise ValueError("Среднее сближение должно быть в диапазоне 0-3 градуса")

            self_x = self.self_x.get()
            self_y = self.self_y.get()
            if not (0 <= self_x <= 10000 and 0 <= self_y <= 10000):
                raise ValueError("Координаты должны быть в диапазоне 0-10000")

            # Проверка параметров полета
            camera_angle = self.camera_angle.get()
            if not -90 <= camera_angle <= 56:
                raise ValueError("Угол наклона камеры должен быть в диапазоне -90 до 56 градусов")

            lazer_distance = self.lazer_distance.get()
            if not 0 <= lazer_distance <= 1200:
                raise ValueError("Дальность лазерного дальномера должна быть в диапазоне 0-1200 метров")

            magnetic_course = self.magnetic_course.get()
            if not 0 <= magnetic_course <= 360:
                raise ValueError("Магнитный курс должен быть в диапазоне 0-360 градусов")

            return True
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return False

    def calculate(self):
        if not self.validate_input():
            return

        try:
            # Получаем данные
            camera_angle = self.camera_angle.get()
            lazer_distance = self.lazer_distance.get()
            magnetic_course = self.magnetic_course.get()
            declination = self.declination.get()
            convergence = self.convergence.get()
            self_x = self.self_x.get()
            self_y = self.self_y.get()

            # Расчет
            distance = self.get_distance(camera_angle, lazer_distance)
            map_angle = self.get_map_angle(magnetic_course, declination, convergence)
            obj_x, obj_y = self.get_obj_coordinates(distance, map_angle, self_x, self_y)

            # Проверка выходных координат
            if not (0 <= obj_x <= 10000 and 0 <= obj_y <= 10000):
                raise ValueError("Рассчитанные координаты выходят за допустимый диапазон 0-10000")

            # Вывод
            self.result_label.config(text=f"Координаты объекта: (X, Y) = ({obj_x:.2f}, {obj_y:.2f})")
        except Exception as e:
            messagebox.showerror("Ошибка расчета", f"Ошибка при расчете координат: {e}")

    def get_distance(self, camera_angle, lazer_distance):
        """Вычисление горизонтального расстояния до объекта"""
        return lazer_distance * math.cos(math.radians(camera_angle))

    def get_map_angle(self, magnetic_course, declination, convergence):
        """Вычисление дирекционного угла на карте"""
        return (magnetic_course + declination + convergence) % 360  # Нормализация угла в диапазон 0-360

    def get_obj_coordinates(self, distance, map_angle, self_x, self_y):
        """Вычисление координат объекта"""
        # Преобразуем полярные координаты в декартовы
        angle_rad = math.radians(map_angle)
        delta_x = distance * math.sin(angle_rad)
        delta_y = distance * math.cos(angle_rad)

        obj_x = self_x + delta_x
        obj_y = self_y + delta_y

        return round(obj_x, 2), round(obj_y, 2)


if __name__ == "__main__":
    root = tk.Tk()
    app = DroneCalculatorApp(root)
    root.mainloop()