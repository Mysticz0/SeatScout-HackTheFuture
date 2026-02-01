
VIDEO_FILES = {
    'A1': 'static/booth_A1_free.mp4',
}

OCCUPANCY_CRITERIA = {
    'OCCUPIED_min_people': 1, 
    'OCCUPIED_min_duration_seconds': 30,
    'VACANT_people_duration_seconds': 30, 
    'check_interval_seconds': 2
}

HOST = '0.0.0.0'
PORT = 5000
DEBUG = True

INITIAL_SPACES = {
    'A1': {'floor': 1, 'status': 'free', 'person_count': 0},
    'A2': {'floor': 1, 'status': 'occupied', 'person_count': 1},
    'A3': {'floor': 1, 'status': 'occupied', 'person_count': 3},
    'A4': {'floor': 1, 'status': 'occupied', 'person_count': 1},
    'A5': {'floor': 1, 'status': 'occupied', 'person_count': 2},
    'A6': {'floor': 1, 'status': 'occupied', 'person_count': 1},
    'A7': {'floor': 1, 'status': 'occupied', 'person_count': 4},
    'A8': {'floor': 1, 'status': 'occupied', 'person_count': 1},
    'A9': {'floor': 1, 'status': 'occupied', 'person_count': 5},
    'A10': {'floor': 1, 'status': 'occupied', 'person_count': 2}
}
