#!/usr/bin/env python

import subprocess
import sys
import threading


class WorkerThread(threading.Thread):
    def __init__(self, queue):
        """
        A thread that executes shell commands

        :type queue: queue.Queue
        """
        self.queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while True:
            info = self.queue.get()
            print('Executing: %s' % ' '.join(info['command']))
            try:
                subprocess.check_call(info['command'])
            except subprocess.CalledProcessError as e:
                print(e)
                sys.exit(1)
            except KeyboardInterrupt:
                sys.exit(1)

            if 'callback' in info:
                info['callback']()
            self.queue.task_done()
