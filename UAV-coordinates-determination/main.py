import tkinter as tk
from tkinter import ttk, messagebox
import math


class DroneCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет координат объекта с БПЛА")

        # Инициализация переменных
        self.declination = tk.DoubleVar()
        self.convergence = tk.DoubleVar()
        self.self_x = tk.DoubleVar()
        self.self_y = tk.DoubleVar()

        self.camera_angle = tk.DoubleVar()
        self.lazer_distance = tk.DoubleVar()
        self.magnetic_course = tk.DoubleVar()

        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.tab_prepare = ttk.Frame(self.notebook)
        self.tab_flight = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_prepare, text="Подготовка")
        self.notebook.add(self.tab_flight, text="Полет")
        self.notebook.pack(expand=True, fill="both")

        # Вкладка "Подготовка"
        self.setup_prepare_tab()

        # Вкладка "Полет"
        self.setup_flight_tab()

    def setup_prepare_tab(self):
        # Магнитное склонение
        ttk.Label(self.tab_prepare, text="Магнитное склонение:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_prepare, textvariable=self.declination, width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.tab_prepare, text="град.").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Среднее сближение
        ttk.Label(self.tab_prepare, text="Среднее сближение:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_prepare, textvariable=self.convergence, width=10).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.tab_prepare, text="град.").grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Координаты взлета
        ttk.Label(self.tab_prepare, text="Координаты взлета (X):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_prepare, textvariable=self.self_x, width=10).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.tab_prepare, text="Координаты взлета (Y):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_prepare, textvariable=self.self_y, width=10).grid(row=3, column=1, padx=5, pady=5)

    def setup_flight_tab(self):
        # Угол наклона камеры
        ttk.Label(self.tab_flight, text="Угол наклона камеры:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_flight, textvariable=self.camera_angle, width=10).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.tab_flight, text="град.").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Показания дальномера
        ttk.Label(self.tab_flight, text="Показания дальномера:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_flight, textvariable=self.lazer_distance, width=10).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.tab_flight, text="м").grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Магнитный курс
        ttk.Label(self.tab_flight, text="Магнитный курс:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.tab_flight, textvariable=self.magnetic_course, width=10).grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.tab_flight, text="град.").grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Кнопка расчета
        ttk.Button(self.tab_flight, text="Рассчитать координаты", command=self.calculate).grid(row=3, column=0,
                                                                                               columnspan=3, pady=10)

        # Вывод результата
        self.result_label = ttk.Label(self.tab_flight, text="Координаты объекта: (X, Y) = ")
        self.result_label.grid(row=4, column=0, columnspan=3, pady=5)

    def dms_to_dd(self, degrees, minutes):
        return degrees + minutes / 60

    def get_distance(self, camera_angle, lazer_distance):
        return lazer_distance * math.cos(math.radians(camera_angle))

    def get_map_angle(self, magnetic_course, declination, convergence):
        return magnetic_course + declination + convergence

    def get_obj_coordinates(self, distance, map_angle, self_x, self_y):
        if 0 <= map_angle <= 90:
            delta_x = distance * math.cos(math.radians(map_angle))
            delta_y = distance * math.sin(math.radians(map_angle))
            obj_x = self_x + delta_x
            obj_y = self_y + delta_y
        elif 90 < map_angle <= 180:
            map_angle = 180 - map_angle
            delta_x = distance * math.cos(math.radians(map_angle))
            delta_y = distance * math.sin(math.radians(map_angle))
            obj_x = self_x - delta_x
            obj_y = self_y + delta_y
        elif 180 < map_angle <= 270:
            map_angle = 270 - map_angle
            delta_x = distance * math.sin(math.radians(map_angle))
            delta_y = distance * math.cos(math.radians(map_angle))
            obj_x = self_x - delta_x
            obj_y = self_y - delta_y
        elif 270 < map_angle <= 360:
            map_angle = 360 - map_angle
            delta_x = distance * math.cos(math.radians(map_angle))
            delta_y = distance * math.sin(math.radians(map_angle))
            obj_x = self_x + delta_x
            obj_y = self_y - delta_y
        return int(obj_x), int(obj_y)

    def calculate(self):
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

            # Вывод
            self.result_label.config(text=f"Координаты объекта: (X, Y) = ({obj_x}, {obj_y})")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте введенные данные!\nОшибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DroneCalculatorApp(root)
    root.mainloop()