# -*- coding: utf-8 -*-
import time
from pywinauto.controls.hwndwrapper import InvalidWindowHandle
from pywinauto.base_wrapper import ElementNotEnabled


def assert_window(app, obj="DEFAULT", err="Что-то пошло не так - ошибка не задана",
                  action="exist", timer=30, add="", backend="win32"):
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
        elif action is "exist":
            dlg = app.top_window()
            if dlg.window(title_re=obj).exists():
                success = True
            if not success:
                t = assert_timer(t, timer, err)
        elif action is "check":
            try:
                dlg = app.top_window()
                if backend == "win32":
                    if dlg[obj].GetCheckState() == add:
                        success = True
                elif backend == "uia":
                    if dlg[obj].is_selected() == add:
                        success = True
                else:
                    assert False, "Неизвестный бэкенд pywinauto"
            except InvalidWindowHandle:
                t = assert_timer(t, timer, err)
        elif action is "length":
            dlg = app.top_window()
            if len(dlg[obj].children()) == add:
                success = True
            if not success:
                t = assert_timer(t, timer, err)
        elif action is "enabled":
            dlg = app.top_window()
            if dlg[obj].is_enabled() and not add:
                success = True
            elif not dlg[obj].is_enabled() and add:
                success = True
            if not success:
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