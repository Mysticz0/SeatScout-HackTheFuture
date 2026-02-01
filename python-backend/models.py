import time 
import random
from config import INITIAL_SPACES

class SpaceManager:
    def __init__(self):
        self.spaces = {}
        for spaceId, data in INITIAL_SPACES.items():
            self.spaces[spaceId] = {'space_id': spaceId,
                'status': 'available',
                'person_count': 0,
                'reserved_until': None,
                'reservation_time': None
            }
        self.videoStartTime = None
    #get space values
    def getAll(self):
        return self.spaces
    #get IDs
    def getOne(self, spaceId):
        return self.spaces.get(spaceId)
    
    #------------AI STARTS HERE------------
    def update(self, spaceId, **changes):
        if spaceId in self.spaces:
            self.spaces[spaceId].update(changes)
            return True
        return False
    #------------AI ENDS HERE--------------

    #functions for video playing, getting data, etc.
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