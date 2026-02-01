import torch
torch.serialization.add_safe_globals([torch.nn.Module])

from ultralytics import YOLO
import cv2
import os
import time

class PersonDetection:
    def __init__(self):
    #------------AI STARTS HERE------------
        print("Loading AI model...")
        self.model = YOLO('yolov8n.pt')
        print("AI model ready!")
        self.trackers = {}
    #------------AI ENDS HERE--------------

    def countPeopleAndBags(self, frame):
        #analyzes single video frames & counts num of people detected using YOLOv8
        results = self.model(frame, verbose=False)
        
        people = 0
        
        #loop through all detected objects in frame (people counting)
        for box in results[0].boxes:
            classId = int(box.cls[0])
            if classId == 0: #class 0 in dataset means it is a person
                people += 1
        
        return people
    
    def checkVideoAtTime(self, videoPath, seconds):
        #enables time checking through pre-recorded videos used for demo of program
        if not os.path.exists(videoPath):
            return 0
        #made using youtube with explanation from AI
        cap = cv2.VideoCapture(videoPath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frameNum = int(seconds * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret: #if cant read fram return 0
            return 0
        #count people in frame
        return self.countPeopleAndBags(frame)
    
    def turnRedCheck(self, spaceId, peopleCount):
        #turn red on app after specific criterion are met
        now = time.time()
    
        if spaceId not in self.trackers:
            self.trackers[spaceId] = {'personStart': None, 'emptyStart': None}
        tracker = self.trackers[spaceId]
    
        if peopleCount >= 1:
            if tracker['personStart'] is None:
                tracker['personStart'] = now
            
            duration = now - tracker['personStart']
            return duration >= 10
        else:
            tracker['personStart'] = None
            return False
        
    def turnGreenCheck(self, spaceId, peopleCount):
        #same as function above but to turn green instead
        now = time.time()
        
        if spaceId not in self.trackers:
            self.trackers[spaceId] = {'personStart': None, 'emptyStart': None}
        
        tracker = self.trackers[spaceId]
        
        if peopleCount == 0:
            if tracker['emptyStart'] is None:
                tracker['emptyStart'] = now
            
            duration = now - tracker['emptyStart']
            return duration >= 30
        else:
            tracker['emptyStart'] = None
            return False
        
    def reset(self, spaceId):
        #reset all tracking timers
        if spaceId in self.trackers:
            self.trackers[spaceId] = {'personStart': None, 'emptyStart': None}
