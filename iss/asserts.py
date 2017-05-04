# -*- coding: utf-8 -*-
import time
from pywinauto.controls.hwndwrapper import InvalidWindowHandle
from pywinauto.base_wrapper import ElementNotEnabled
from pywinauto.findwindows import ElementNotFoundError


def assert_window(app, obj="DEFAULT", err="Что-то пошло не так - ошибка не задана",
                  action="exist", timer=30, add="", backend="win32"):
    '''Функция для разнообразных проверок в окнах SecurOS
    app - объект pywinauto, obj - имя контролла, err - сообщение об ошибке, action - что нужно сделать,
    timer - сколько ждать реакции от процесса, add - дополнительная информация, backend - тип бэкенда pywinauto'''

    t = 0
    success = False
    while not success:
        if action is "click":  # Осуществляем нажатие мышкой один или два раза
            try:
                dlg = app.top_window()
                dlg.window(title_re=obj).click_input(double=add, use_log=False)
                success = True
            except (InvalidWindowHandle, ElementNotEnabled, RuntimeError):
                t = assert_timer(t, timer, err)
            except ElementNotFoundError:
                try:
                    dlg[obj].click_input(double=add, use_log=False)
                    success = True
                except ElementNotFoundError:
                    t = assert_timer(t, timer, err)
        elif action is "children":  # Проверяем наличие дочерних процессов у процесса
            if app.children():
                success = True
            if not success:
                t = assert_timer(t, timer, err)
        elif action is "exist":  # Проверяем наличие объекта
            try:
                dlg = app.top_window()
                if dlg.window(title_re=obj).exists():
                    success = True
                if not success:
                    t = assert_timer(t, timer, err)
            except RuntimeError:
                assert_timer(timer, timer, err)  # Если упали с рантаймом, значит окна нужного вообще нет
        elif action is "check":  # Проверяем состояние чекбокса
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
            except (InvalidWindowHandle, RuntimeError):
                t = assert_timer(t, timer, err)
        elif action is "length":  # Проверяем длинну списка
            try:
                dlg = app.top_window()
                if len(dlg[obj].children()) == add:
                    success = True
                if not success:
                    t = assert_timer(t, timer, err)
            except RuntimeError:
                assert_timer(timer, timer, err)
        elif action is "enabled":  # Проверяем активность объекта
            try:
                dlg = app.top_window()
                if dlg[obj].is_enabled() and not add:
                    success = True
                elif not dlg[obj].is_enabled() and add:
                    success = True
                if not success:
                    t = assert_timer(t, timer, err)
            except RuntimeError:
                assert_timer(timer, timer, err)
        elif action is "type":  # Вводим в объект последовательность с клавиатуры
            try:
                dlg = app.top_window()
                dlg[obj].type_keys(add)
                success = True
            except RuntimeError:
                t = assert_timer(t, timer, err)
        else:
            assert False, "Неизвестное действие"


def assert_timer(t, timer, err):
    '''Вспомогательная функция таймер'''

    time.sleep(1)
    t += 1
    if t >= timer:
        assert False, err
    return t