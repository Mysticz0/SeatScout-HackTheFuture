import time 
import random
from config import INITIAL_SPACES

class SpaceManager:
    def __init__(self):
        self.spaces = {}
        for spaceId, data in INITIAL_SPACES.items():
            self.spaces[spaceId] = {
                'reserved_until': None,
                'reservation_time': None
            }
        self.videoStartTime = None
    
    def getAll(self):
        return self.spaces
    
    def getOne(self, spaceId):
        return self.spaces.get(spaceId)
    
    #------------AI STARTS HERE------------
    def update(self, spaceId, **changes):
        if spaceId in self.spaces:
            self.spaces[spaceId].update(changes)
            return True
        return False
    #------------AI ENDS HERE--------------

    def startVideo(self):
        self.videoStartTime = time.time()
    
    def getVideoTime(self):
        if self.videoStartTime is None:
            return 0
        return time.time() - self.videoStartTime
    
    def stopVideo(self):
        self.videoStartTime = None
    
    def tieBreaker(self, names):
        return random.choice(names)