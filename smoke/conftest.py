# -*- coding: utf-8 -*-

import pytest
import psutil
import pywinauto
from os.path import abspath, curdir, join
import time

from iss.misc import misc_unpack_procs


def pytest_namespace():
    return {
        "SECUROS_INSTALL_PATH": "C:\\Program Files (x86)\\ISS\\SecurOS",
        "SECUROS_INSTALL_BUILD": join(abspath(curdir), 'smoke', 'data', 'SecurOSEnterprise_9.3.95_Dev_ISS.exe')
    # TODO: Очевидно тут будет номер билда который мы тестируем вместо хардкода
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

    for proc in PROCS:  # Ищем PIDы
        for tpid in psutil.process_iter():
            if tpid.name() == proc and proc is not "client.exe":
                securos_pids[proc] = tpid.pid
            elif tpid.name() == proc and proc is "client.exe":  # client.exe два процесса, нам нужен 1
                clipid.append(tpid.pid)

    if clipid:
        for pid in clipid:  # Выбираем тот процесс, который больше памяти занял
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
            "core": pywinauto.Application(backend="uia").connect(process=securos_pids["securos.exe"]),
            "client": pywinauto.Application(backend="uia").connect(process=securos_pids["client.exe"]),
            "monitor": pywinauto.Application(backend="uia").connect(process=securos_pids["monitor.exe"])
        }
    else:
        return {
            "wizard": pywinauto.Application(backend="uia").connect(process=securos_pids["wizard.exe"])
        }


@pytest.fixture(scope="session")
def securos_install():
    '''Запуск установки SecurOS'''

    return psutil.Popen(pytest.SECUROS_INSTALL_BUILD)


@pytest.fixture(scope="function")
def securos_start():
    '''Запуск SecurOS'''

    securos = psutil.Popen(join(pytest.SECUROS_INSTALL_PATH, "securos.exe"))
    t = 0
    while not securos.children() and t < 10:  # TODO: тут вот надо придумать способ дожидаться пока все процессы прогрузятся
        time.sleep(1)
        t += 1

    return misc_unpack_procs({"securos.exe": securos}, securos)
