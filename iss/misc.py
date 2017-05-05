# -*- coding: utf-8 -*-
from psutil import NoSuchProcess


def misc_procs_unpack(procs, app):
    '''Утилита для рекурсивной распаковки дерева зависимых процессов у корневого процесса'''

    tmp = procs
    for proc in app.children():
        if proc.children():
            procs.update(misc_procs_unpack({}, proc))
        procs[proc.name()] = proc

    if "idb.exe" in procs:
        procs = tmp
        procs = misc_procs_unpack(procs, app)
    return procs


def misc_procs_kill(proc):
    '''Утилита для финализации рабочих процессов секуроса'''

    try:
        if proc.is_running():
            try:
                for child in proc.children(True):
                    child.kill()
            except:
                pass
            proc.kill()
    except NoSuchProcess:
        pass