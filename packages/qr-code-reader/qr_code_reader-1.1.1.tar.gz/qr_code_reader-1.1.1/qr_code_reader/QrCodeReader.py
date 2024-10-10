import sys
from time import sleep
import queue


class QRCodeReader:
    def __init__(self, queue):
        self.queue = queue

    def Read(self):
        
        try:
            codebarre = str(input())
            if self.queue.empty() and codebarre != "":
                self.queue.put(codebarre)
                return self.queue.get()
            else:
                return None
        except EOFError:
            return None  # Return None or some default value
        except KeyboardInterrupt:
            print("[INFO] Cleaning up...")
            return None  # Return None or some default value
