from pywinauto.application import Application

app = Application(backend="uia").connect(process=8796)
tree = app.top_window()

tree["Система"].click_input(double=True)
tree["SecurOS Enterprise"].click_input(double=True)
tree["Оборудование"].click_input(double=True)
tree.window(title_re="Компьютер*").click_input(button="right")
app.Menu["Создать"].click_input()
app.Menu["Устройство видеозахвата"].click_input()

vid = app.window(title_re="Параметры")
vid["ComboBox"].click_input()
vid["Axis"].click_input()
vid["Ok Enter"].click_input()

sets = app.Pane
sets["ОК"].click_input()
tree["Устройство видеозахвата 1"].click_input(button="right")
app.Menu["Создать"].click_input()
app.Menu["Камера"].click_input()

vid = app.window(title_re="Параметры")
vid["Ok Enter"].click_input()

sets = app.Pane
sets["ОК"].click_input()