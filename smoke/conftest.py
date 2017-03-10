# -*- coding: utf-8 -*-

import pytest
import psutil
from pywinauto.application import Application
import os


def pytest_namespace():

    return {
        "SECUROS_WIN": "C:\\Program Files (x86)\\ISS\\SecurOS",
        "SECUROS_LINUX": "/opt/iss/securos"
    }


@pytest.fixture(scope="session")
def securos_pids():
    '''Собираем PIDы для процессов SecurOS'''

    PROCS = ["securos.exe", "client.exe"]
    securos_pids = {
        "securos.exe": 0,
        "client.exe": 0
    }
    clipid = []
    mem = []

    for proc in PROCS: #Ищем PIDы
        for tpid in psutil.process_iter():
            if tpid.name() == proc and proc is not "client.exe":
                securos_pids[proc] = tpid.pid
            elif tpid.name() == proc and proc is "client.exe": # client.exe два процесса, нам нужен 1
                clipid.append(tpid.pid)

    for pid in clipid: # Выбираем тот PID, в котором больше памяти
        pr = psutil.Process(pid)
        mem.append(pr.memory_info().rss)
    securos_pids["client.exe"] = clipid[mem.index(max(mem))]

    return securos_pids


@pytest.fixture(scope="session")
def securos_auto(securos_pids):
    '''Создаем объекты автоматизации pywinauto'''

    return {
        "core": Application(backend="uia").connect(process=securos_pids["securos.exe"]),
        "client": Application(backend="uia").connect(process=securos_pids["client.exe"])
    }