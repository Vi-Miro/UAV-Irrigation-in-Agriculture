from pywinauto import Application
import time

app = Application(backend="uia").connect(process=14340)
time.sleep(2)

window = app.window(title="Расчет координат объекта с БПЛА")

window.print_control_identifiers()

