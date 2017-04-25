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
import sys


def main() -> None:
    """Main function."""
    hours = int(sys.argv[1])
    pool = []
    for i in range(hours):
        pool.append(DouYu().run())
    print("please wait for complete...")
    for p in pool:
        p.join()


if __name__ == "__main__":
    main()
