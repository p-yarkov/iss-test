# -*- coding: utf-8 -*-
import time
from pywinauto.controls.hwndwrapper import InvalidWindowHandle
from pywinauto.base_wrapper import ElementNotEnabled


def assert_window(app, obj="DEFAULT", err="Что-то пошло не так - ошибка не задана", action="assert", timer=30, add=""):
    '''Функция для разнообразных проверок в окнах SecurOS'''

    t = 0
    success = False
    while not success:
        if action is "click":
            try:
                dlg = app.top_window()
                dlg.window(title_re=obj).click()
                success = True
            except (InvalidWindowHandle, ElementNotEnabled):
                t = assert_timer(t, timer, err)
        elif action is "children":
            if app.children():
                success = True
            if not success:
                t = assert_timer(t, timer, err)
        elif action is "assert":
            dlg = app.top_window()
            if dlg.window(title_re=obj).exists():
                success = True
            if not success:
                t = assert_timer(t, timer, err)
        elif action is "check":
            try:
                dlg = app.top_window()
                if dlg[obj].GetCheckState() == add:
                    success = True
            except InvalidWindowHandle:
                t = assert_timer(t, timer, err)
        else:
            assert False, "Неизвестное действие"


def assert_timer(t, timer, err):
    '''Вспомогательная функция таймер'''

    time.sleep(1)
    t += 1
    if t == timer:
        assert False, err
    return t