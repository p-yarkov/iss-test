# -*- coding: utf-8 -*-


def misc_procs_unpack(procs, app):
    '''Утилита для рекурсивной распаковки дерева зависимых процессов у корневого процесса'''

    tmp = procs
    for proc in app.children(True):
        procs[proc.name()] = proc

    if "idb.exe" in procs:
        procs = tmp
        procs = misc_procs_unpack(procs, app)
    return procs


def misc_procs_kill(proc):
    '''Утилита для финализации рабочих процессов секуроса'''

    if proc.is_running():
        for child in proc.children(True):
            child.kill()
        proc.kill()