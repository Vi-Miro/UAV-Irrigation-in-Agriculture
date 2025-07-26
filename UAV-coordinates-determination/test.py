from pywinauto import Application
import time
import pyautogui

def run_test():
    try:
        # Запуск приложения
        app = Application().connect(process=14340)
        time.sleep(3)  # Даем время на загрузку

        # Получаем главное окно
        window = app.window(title="Расчет координат объекта с БПЛА")
        rect = window.rectangle()

        print("\n=== ТЕСТ ВВОДА ДАННЫХ ===")

        # Координаты полей ввода (подберите свои значения)
        fields = [
            (rect.left + 230, rect.top + 70),  # Магнитное склонение
            (rect.left + 230, rect.top + 100),  # Среднее сближение
            (rect.left + 230, rect.top + 130),  # X
            (rect.left + 230, rect.top + 160),  # Y
            (rect.left + 230, rect.top + 230),  # Угол наклона
            (rect.left + 230, rect.top + 260),  # Дальность
            (rect.left + 230, rect.top + 280)  # Курс
        ]

        values = ["3.0", "1.0", "1000", "2000", "30.0", "500.0", "380.0"]

        for (x, y), val in zip(fields, values):
            pyautogui.click(x, y)
            pyautogui.write(val)
            time.sleep(0.5)

        print("Данные введены успешно")

        print("\n=== ТЕСТ РАСЧЕТА ===")

        # Координаты кнопки (подберите свои)
        button_x = rect.left + 150
        button_y = rect.top + 300
        pyautogui.click(button_x, button_y)
        time.sleep(1)

        # Проверка на наличие диалога ошибки
        try:
            error_dialog = app.window(title="Ошибка ввода")
            error_calc = app.window(title="Ошибка расчета")
            if error_dialog.exists() or error_calc.exists():
                if error_dialog['Магнитное склонение должно быть в диапазоне 0-26 градусов'].exists():
                    error_text = error_dialog['Магнитное склонение должно быть в диапазоне 0-26 градусов'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False
                elif error_dialog['Среднее сближение должно быть в диапазоне 0-3 градуса'].exists():
                    error_text = error_dialog['Среднее сближение должно быть в диапазоне 0-3 градуса'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False
                elif error_dialog['Координаты должны быть в диапазоне 0-10000'].exists():
                    error_text = error_dialog['Координаты должны быть в диапазоне 0-10000'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False
                elif error_dialog['Угол наклона камеры должен быть в диапазоне -90 до 56 градусов'].exists():
                    error_text = error_dialog['Угол наклона камеры должен быть в диапазоне -90 до 56 градусов'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False
                elif error_dialog['Дальность лазерного дальномера должна быть в диапазоне 0-1200 метров'].exists():
                    error_text = error_dialog['Дальность лазерного дальномера должна быть в диапазоне 0-1200 метров'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False
                elif error_dialog['Магнитный курс должен быть в диапазоне 0-360 градусов'].exists():
                    error_text = error_dialog['Магнитный курс должен быть в диапазоне 0-360 градусов'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False
                else:
                    error_text = error_calc['Рассчитанные координаты выходят за допустимый диапазон 0-10000'].window_text()
                    print(f"Обнаружена ошибка: {error_text}")
                    error_dialog.Button.click()  # Закрываем диалог
                    return False


        except Exception as e:
            print(f"Ошибка при проверке диалога: {str(e)}")
            return False

        print("Тест расчета выполнен успешно")
        return True

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_test()
    print("\n=== РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ ===")
    print("УСПЕШНО" if success else "С ОШИБКАМИ")