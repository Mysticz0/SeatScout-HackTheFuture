from flask import Flask, jsonify, request
from flask_cors import CORS
from models import SpaceManager
from ai_detector import PersonDetection
from config import VIDEO_FILES, OCCUPANCY_CRITERIA
import threading
import time

#initialize flask & enable CORS for android app reqs.
app = Flask(__name__)
CORS(app)

#initialize handling booth data, initialize YOLOv8 detection
spaceManager = SpaceManager()
detector = PersonDetection()

@app.route('/')
def home():
    #confirm backend running on http server
    return jsonify({'message': 'SeatScout Backend Running!'})

@app.route('/check-all-spaces')
def check_all_spaces():
    #android app checks this endpoint periodically to update booth colours
    spaces = spaceManager.getAll()
    return jsonify(spaces)

@app.route('/check-space/<space_id>')
def check_space(space_id):
    #check status of specific space via space ID ie) A1, A2, A3...
    space = spaceManager.getOne(space_id)
    if space:
        return jsonify(space)
    return jsonify({'error': 'Space not found'}), 404

@app.route('/reserve-space/<space_id>', methods=['POST'])
def reserve_space(space_id):
    #reserve a study space for 10 mins, booth turns yellow after it expires
    space = spaceManager.getOne(space_id)
    
    if not space:
        return jsonify({'error': 'Space not found'}), 404
    
    if space['status'] == 'occupied':
        return jsonify({'error': 'Space is occupied'}), 400
    
    reservation_time = time.time()
    reservation_end = reservation_time + (10)
    
    spaceManager.update(space_id, status='reserved', reserved_until=reservation_end, reservation_time=reservation_time)
    
    return jsonify({
        'message': f'Space {space_id} reserved for 10 seconds', #for demo purposes 10 seconds
        'reserved_until': reservation_end, 'space': spaceManager.getOne(space_id)
    })

@app.route('/cancel-reservation/<space_id>', methods=['POST'])
def cancel_reservation(space_id):
    #cancel booking above ==> space returns to green status (free)
    space = spaceManager.getOne(space_id)
    
    if not space:
        return jsonify({'error': 'Space not found'}), 404
    
    spaceManager.update(space_id, status='free', reserved_until=None, reservation_time=None)
    
    return jsonify({
        'message': f'Reservation for {space_id} cancelled',
        'space': spaceManager.getOne(space_id)
    })

def check_reservations():
    while True:
        current_time = time.time()
        spaces = spaceManager.getAll()
        
        for space_id, space in spaces.items():
            if space.get('status') == 'reserved':
                reserved_until = space.get('reserved_until', 0)
                if current_time >= reserved_until: #if not at booth & reservation done, turn to green
                    spaceManager.update(space_id, status='free', reserved_until=None, reservation_time=None)
                    print(f"Reservation expired for {space_id}")
        
        time.sleep(10) #check every 10 seconds

#----------AI STARTS HERE----------#
reservation_thread = threading.Thread(target=check_reservations, daemon=True)
reservation_thread.start()
#----------AI ENDS HERE----------#

monitoring = False 

def monitor_loop():
    global monitoring
    
    print("\nMonitoring A1 video...")
    
    while monitoring:
        #----------AI STARTS HERE----------#
        video_time = spaceManager.getVideoTime()
        people = detector.checkVideoAtTime(VIDEO_FILES['A1'], video_time)
        
        space = spaceManager.getOne('A1')
        status = space['status']
        #----------AI ENDS HERE----------#

        #once detected start displaying vid time, num detected, status of booth
        if people > 0:
            print(f"====== 🚨 {video_time:.0f}s |||| PEOPLE DETECTED: {people} |||| BOOTH STATUS: {status} 🚨 ======")
        else:
            print(f"====== {video_time:.0f}s | PEOPLE: {people} | STATUS: {status} ======")
        
        #update count for people at booth (in video)
        spaceManager.update('A1', person_count=people)
        
        #check to turn red or not
        should_turn_red = detector.turnRedCheck('A1', people)
        if people > 0:
            tracker = detector.trackers.get('A1', {})
            person_duration = tracker.get('personStart')
            if person_duration:
                elapsed = time.time() - person_duration
                print(f"====== PERSON PRESENT FOR: {elapsed:.1f}s (need 10s to turn RED) ======")
        
        if status != 'occupied' and detector.turnRedCheck('A1', people):
            spaceManager.update('A1', status='occupied')
            print("✅✅✅ ====== A1 <=====> RED (Occupied) ====== ✅✅✅")
            print(f"   New status: {spaceManager.getOne('A1')}")

        # RED → GREEN: occupied → available (empty for 30s)
        elif status == 'occupied' and detector.turnGreenCheck('A1', people):
            spaceManager.update('A1', status='available')
            print("✅✅✅ ====== A1 <=====> GREEN (Available) ====== ✅✅✅")
            print(f"   New status: {spaceManager.getOne('A1')}")

        time.sleep(2)

#----------AI STARTS HERE----------#
@app.route('/demo/init', methods=['POST'])
def init_demo():
    # Reset A1 only
    spaceManager.update('A1', status='available', person_count=0)
    detector.reset('A1')
    
    return jsonify({'success': True, 'spaces': spaceManager.getAll()})
#----------AI ENDS HERE----------#

@app.route('/demo/start-monitoring', methods=['POST'])
def start_monitoring():
    global monitoring
    
    if not monitoring:
        spaceManager.startVideo()
        monitoring = True
        thread = threading.Thread(target=monitor_loop, daemon=True) #line used from former piece of AI code above
        thread.start()
    
    return jsonify({'success': True, 'message': 'AI monitoring started'})

@app.route('/demo/stop-monitoring', methods=['POST'])
def stop_monitoring():
    global monitoring
    monitoring = False
    spaceManager.stopVideo()
    
    return jsonify({'success': True, 'message': 'AI monitoring stopped'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)