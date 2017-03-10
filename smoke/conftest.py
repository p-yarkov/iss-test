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
        "monitor.exe": 0
    }
    clipid = []
    mem = []

    PROCS = ["securos.exe", "client.exe", "monitor.exe"]

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


@pytest.fixture(scope="function")
def securos_auto(securos_pids):
    '''Создаем объекты автоматизации pywinauto'''

    for pid in securos_pids.values():
        assert psutil.pid_exists(pid)

    return {
        "core": Application(backend="uia").connect(process=securos_pids["securos.exe"]),
        "client": Application(backend="uia").connect(process=securos_pids["client.exe"]),
        "monitor": Application(backend="uia").connect(process=securos_pids["monitor.exe"])
    }


@pytest.fixture(scope="function")
def securos_start():
    '''Запускаем SecurOS'''

    PROCS = ["securos.exe", "client.exe", "monitor.exe"]

    psutil.Popen(os.path.join(pytest.SECUROS_WIN, "securos.exe")) # Ждем запуска всех процессов
    pid = 0
    t = 0
    while pid < 3:
        pid = 0
        for proc in PROCS:
            for tpid in psutil.process_iter():
                if tpid.name() == proc:
                    pid+=1
        time.sleep(1)
        t+=1
        if t >= 10:
            assert False