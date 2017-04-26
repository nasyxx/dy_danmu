#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Life's pathetic, happy coding ♡~ Nasy.

O._.O
(=/) +1s

@author: Nasy
@date: Apr 25, 2017
@email: sy_n@me.com
@file: main.py
@license: MIT

Copyright © 2017 by Nasy. All Rights Reserved.
"""
from douyu import DouYu
from multiprocessing.dummy import Process, Queue
import tarfile
import time

POOL = Queue()
FNAMES = Queue()


def archive() -> None:
    """Archiving files."""
    while 1:
        tt = time.strftime("%H")
        with tarfile.open(
                time.strftime("record/"
                              "%Y%m%d_%H%M%S.tar.gz"), "w:gz") as f:
            while 1:
                p = POOL.get()
                fnames = FNAMES.get()
                f.add("record/" + fnames + ".danmu")
                p.join()
                if tt == "12":
                    break
                else:
                    tt = time.strftime("%H")


def main() -> None:
    """Main function."""
    Process(target=archive).start()
    while 1:
        p, fname = DouYu().run()
        POOL.put(p)
        FNAMES.put(fname)


if __name__ == "__main__":
    main()
