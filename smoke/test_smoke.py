# -*- coding: utf-8 -*-
import pytest
import time
import shutil
import os


def test_smoke_object(securos_auto):
    '''4. Добавление объекта'''

    shutil.copy2(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "1._01"),
                 pytest.SECUROS_WIN)

    cli = securos_auto["client"].top_window()
    cli["CheckBox2"].click_input()

    tree = securos_auto["core"].top_window()
    assert tree.exists() # Шаг 1 - Ожидаемый результат
    tree["Система"].click_input(double=True)
    tree["SecurOS Enterprise"].click_input(double=True)
    tree["Оборудование"].click_input(double=True)
    tree.window(title_re="Компьютер*").click_input()
    assert tree.window(title_re="Компьютер*").is_selected() # Шаг 2 - Ожидаемый результат
    securos_auto["core"]["Pane22"]["Создать"].click_input()
    menu = securos_auto["core"].Menu
    assert menu.exists() # Шаг 3 - Ожидаемый результат
    menu["Устройство видеозахвата"].click_input()
    sets = securos_auto["core"].window(title_re="Параметры")
    assert sets.exists() # Шаг 4 - Ожидаемый результат
    sets["ComboBox"].click_input()
    sets["ListBox"].type_keys("{UP 1}{DOWN 40}{ENTER}")
    sets["Ok Enter"].click_input()
    pane = securos_auto["core"].Pane
    pane["ComboBox33"].click_input()
    pane["01"].click_input()
    pane["ОК"].click_input()
    assert tree["Устройство видеозахвата 1"].exists() # Шаг 5 - Ожидаемый результат
    tree["Устройство видеозахвата 1"].click_input(button="right")
    menu["Создать"].click_input()
    menu["Камера"].click_input()
    sets["Ok Enter"].click_input()
    pane["ОК"].click_input()
    monitor = securos_auto["monitor"].top_window()
    monitor["Custom22"].click_input()
    assert tree.window(title="Камера 1 [1]").exists() # Шаг 6 - Ожидаемый результат
    '''Хитрая проверка - проверяем наличие кнопки "Поставить на рхрану" в окне камеры. Если камеры нет в МК или нет
    с нее видео - то кнопка будет недоступна и это баг. Так костыль пока конечно.'''
    assert monitor.window(title_re="Поставить на охрану*").exists()