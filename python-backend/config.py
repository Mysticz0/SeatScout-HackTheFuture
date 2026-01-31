
VIDEO_FILES = {
    'A1': 'static/demo_videos/booth_A1_free.mp4',
    'A2': 'static/demo_videos/booth_A2_laying_down.mp4',
    'A3': 'static/demo_videos/booth_A3_three_people.mp4'
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
    'A3': {'floor': 1, 'status': 'occupied', 'person_count': 3}
}
