from flask import Flask, jsonify, request
from flask_cors import CORS
from models import SpaceManager
from ai_detector import PersonDetection
from config import VIDEO_FILES, OCCUPANCY_CRITERIA
import threading
import time

app = Flask(__name__)
CORS(app)

spaceManager = SpaceManager()
detector = PersonDetection()

@app.route('/')
def home():
    return jsonify({'message': 'SeatScout Backend Running!'})

@app.route('/check-all-spaces')
def check_all_spaces():
    spaces = spaceManager.getAll()
    return jsonify(spaces)

@app.route('/check-space/<space_id>')
def check_space(space_id):
    space = spaceManager.getOne(space_id)
    if space:
        return jsonify(space)
    return jsonify({'error': 'Space not found'}), 404

@app.route('/reserve-space/<space_id>', methods=['POST'])
def reserve_space(space_id):
    space = spaceManager.getOne(space_id)
    
    if not space:
        return jsonify({'error': 'Space not found'}), 404
    
    if space['status'] == 'occupied':
        return jsonify({'error': 'Space is occupied'}), 400
    
    reservation_time = time.time()
    reservation_end = reservation_time + (10 * 60)
    
    spaceManager.update(space_id, 
                       status='reserved', 
                       reserved_until=reservation_end,
                       reservation_time=reservation_time)
    
    return jsonify({
        'message': f'Space {space_id} reserved for 10 minutes',
        'reserved_until': reservation_end,
        'space': spaceManager.getOne(space_id)
    })

@app.route('/cancel-reservation/<space_id>', methods=['POST'])
def cancel_reservation(space_id):
    space = spaceManager.getOne(space_id)
    
    if not space:
        return jsonify({'error': 'Space not found'}), 404
    
    spaceManager.update(space_id, 
                       status='free', 
                       reserved_until=None,
                       reservation_time=None)
    
    return jsonify({
        'message': f'Reservation for {space_id} cancelled',
        'space': spaceManager.getOne(space_id)
    })

def check_reservations():
    while True:
        current_time = time.time()
        spaces = spaceManager.getAll()
        
        for space_id, space in spaces.items():
            if space['status'] == 'reserved':
                reserved_until = space.get('reserved_until', 0)
                if current_time >= reserved_until:
                    spaceManager.update(space_id, 
                                       status='free',
                                       reserved_until=None,
                                       reservation_time=None)
                    print(f"Reservation expired for {space_id}")
        
        time.sleep(10)

reservation_thread = threading.Thread(target=check_reservations, daemon=True)
reservation_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)