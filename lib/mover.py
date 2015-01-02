#!/usr/bin/env python3

import shutil


class Mover:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def move(self):
        shutil.move(self.src, self.dest)
        print('Moved %s --> %s' % (self.src, self.dest))
