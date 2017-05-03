# -*- coding: utf-8 -*-


def misc_unpack_procs(procs, app):
    '''Утилита для рекурсивной распаковки дерева зависимых процессов у корневого процесса'''

    for proc in app.children():
        if proc.children():
            procs.update(misc_unpack_procs({}, proc))
        procs[proc.name()] = proc

    return procs