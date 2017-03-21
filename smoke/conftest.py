# -*- coding: utf-8 -*-

import pytest
import psutil
from pywinauto.application import Application
import os
import time


def pytest_namespace():

    return {
        "SECUROS_WIN": "C:\\Program Files (x86)\\ISS\\SecurOS",
        "SECUROS_LINUX": "/opt/iss/securos"
    }


@pytest.fixture(scope="function")
def securos_pids():
    '''Собираем PIDы для процессов SecurOS'''

    securos_pids = {
        "securos.exe": 0,
        "client.exe": 0,
        "monitor.exe": 0,
        "wizard.exe": 0
    }
    clipid = []
    mem = []

    PROCS = ["securos.exe", "client.exe", "monitor.exe", "wizard.exe"]

    time.sleep(10)  # TODO: Уж0с и кошмар, нужно придумать способ детектировать состояние готовности

    for proc in PROCS: #Ищем PIDы
        for tpid in psutil.process_iter():
            if tpid.name() == proc and proc is not "client.exe":
                securos_pids[proc] = tpid.pid
            elif tpid.name() == proc and proc is "client.exe": # client.exe два процесса, нам нужен 1
                clipid.append(tpid.pid)

    if clipid:
        for pid in clipid: # Выбираем тот процесс, который больше памяти занял
            pr = psutil.Process(pid)
            mem.append(pr.memory_info().rss)
        securos_pids["client.exe"] = clipid[mem.index(max(mem))]

    return securos_pids


@pytest.fixture(scope="function")
def securos_auto(securos_pids):
    '''Создаем объекты автоматизации pywinauto'''

    for pid in securos_pids.values():
        assert psutil.pid_exists(pid)

    if securos_pids["wizard.exe"] == 0:
        return {
            "core": Application(backend="uia").connect(process=securos_pids["securos.exe"]),
            "client": Application(backend="uia").connect(process=securos_pids["client.exe"]),
            "monitor": Application(backend="uia").connect(process=securos_pids["monitor.exe"])
        }
    else:
        return {
            "wizard": Application(backend="uia").connect(process=securos_pids["wizard.exe"])
        }


@pytest.fixture(scope="function")
def securos_start():
    '''Запускаем SecurOS'''

    psutil.Popen(os.path.join(pytest.SECUROS_WIN, "securos.exe")) # Ждем запуска всех процессов