import os
import queue

class Fileloader:
    # Store all files name of the folder
    allFileNames = queue.Queue()
    # Directory of the folder
    parentDir = None

    # Get all filename of folder and add to a queue
    def __init__(self, path) -> None:
        self.parentDir = path
        for filePath in os.listdir(path):
            if filePath.endswith('*.png') or filePath.endswith('*.jpeg'):
                self.allFileNames.put(filePath)
    
    # Return the image path
    def load_next(self):
        if not self.allFileNames.empty():
            return self.parentDir + self.allFileNames.get()

def get_fileLoader(path):
    return Fileloader(path)