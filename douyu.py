#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Life's pathetic, happy coding ♡~ Nasy.

O._.O
(=/) +1s

@author: Nasy
@date: Apr 25, 2017
@email: sy_n@me.com
@file: douyu.py
@license: MIT

Copyright © 2017 by Nasy. All Rights Reserved.
"""
import json
import time
from multiprocessing.dummy import Process, Queue

import requests
from danmu import DanMuClient


class DouYu:
    """Dou Yu dan mu spider."""

    @staticmethod
    def find_room():
        """Find the most hot 50 rooms of douyu."""
        result = []
        for page in range(0, 400, 30):
            datas = json.loads(
                requests.get("http://capi.douyucdn.cn/api/v1/live?"
                             "limit={}&offset={}".format(page + 30, page))
                .text)["data"]
            for data in datas:
                result.append((data["game_name"], data["room_id"]))

        return list(set(result))

    @staticmethod
    def log(url, err):
        with open("dy_log", "a") as f:
            f.write(time.time + "\t" + str(url) + "\t" + str(err))

    def __init__(self):
        """Initailization spider."""
        self.fname = time.strftime("%Y%m%d_%H%M%S")
        self.rooms = self.find_room()
        self.pool_queue = Queue()
        self.msg_queue = Queue()

    def pool_join(self):
        """Processes pool join function."""
        while 1:
            p = self.pool_queue.get()
            if p is None:
                return
            else:
                try:
                    p.join()
                except KeyboardInterrupt:
                    return
                except BaseException:
                    pass

    def record(self):
        with open("record/" + self.fname + ".danmu", "w") as f:
            while 1:
                msg = self.msg_queue.get()
                if msg is None:
                    return
                else:
                    try:
                        f.write(msg)
                    except KeyboardInterrupt:
                        return
                    except BaseException:
                        pass

    def _run(self, room, game):
        dmc = DanMuClient('http://www.douyu.com/{}'.format(room))
        if not dmc.isValid():
            self.log('http://www.douyu.com/{}'.format(room), "Url not valid")

        @dmc.default
        def danmu_fn(msg):
            """Dan mu function."""
            nn = msg["NickName"]
            if msg["MsgType"] == "other":
                content = "other msg"
                nn = "other"
            elif msg["MsgType"] == "gift":
                content = "gift msg"
            else:
                content = msg["Content"]

            res = "\t".join((str(room), str(game), str(time.time()),
                             msg["MsgType"], nn, content, "\n"))

            self.msg_queue.put(res)

        dmc.start(blockThread=False)
        time.sleep(3600)
        dmc.stop()

    def run(self):
        """Run and get datas."""
        print(self.fname, len(self.rooms))

        p_re = Process(target=self.record)
        pool = Process(target=self.pool_join)
        pool.start()
        p_re.start()

        for (game, room) in self.rooms:
            p = Process(target=self._run, args=(room, game))
            p.start()
            self.pool_queue.put(p)

        self.pool_queue.put(None)
        pool.join()
        self.msg_queue.put(None)
        return p_re, self.fname


def main() -> None:
    """Main function."""
    pool = []
    for _ in range(2):
        pool.append(DouYu().run())
    for p in pool:
        print("please wait for complete...")
        p.join()


if __name__ == "__main__":
    main()
