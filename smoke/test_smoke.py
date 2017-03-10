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
    menu = securos_auto["core"].Menu
    tree["Система"].click_input(double=True)
    tree["SecurOS Enterprise"].click_input(double=True)
    tree["Оборудование"].click_input(double=True)
    tree.window(title_re="Компьютер*").click_input(button="right")
    menu["Создать"].click_input()
    menu["Устройство видеозахвата"].click_input()
    sets = securos_auto["core"].window(title_re="Параметры")
    sets["ComboBox"].click_input()
    sets["ListBox"].type_keys("{UP 1}{DOWN 40}{ENTER}")
    sets["Ok Enter"].click_input()
    pane = securos_auto["core"].Pane
    pane["ComboBox33"].click_input()
    pane["01"].click_input()
    pane["ОК"].click_input()
    tree["Устройство видеозахвата 1"].click_input(button="right")
    menu["Создать"].click_input()
    menu["Камера"].click_input()
    sets["Ok Enter"].click_input()
    pane["ОК"].click_input()

#    assert tree.window(title="Камера 1").exists()
#   assert tree.window(title="Камера 2").exists()