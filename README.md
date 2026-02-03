# HackTheFuture

# SeatScout - Booth Occupancy Monitoring System

An AI-powered booth occupancy monitoring application that uses computer vision to detect and track booth availability in real-time.

## 🚀 Features

- Real-time booth occupancy detection using AI/ML
- Android mobile app for monitoring booth status
- Color-coded booth availability (Green = Available, Yellow = Reserved, Red = Occupied)
- 10-second booth reservation system (short reservation time for demonstration purposes)
- Automatic status updates every 2 seconds

## 📋 Prerequisites

### Backend (Python)
- Python 3.7+
- Flask
- ngrok account (for exposing localhost)

### Frontend (Android)
- Android Studio
- Android device or emulator
- Minimum SDK: API 24 (Android 7.0)

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/seatscout.git
cd seatscout
```

### 2. Backend Setup (Python)

#### Install Dependencies

```bash
cd python-backend
pip install -r requirements.txt
```

#### Run the Flask Server

```bash
python3 app.py
```

The server will start on `http://localhost:5000`

You should see:
```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

### 3. Expose Backend with ngrok

Open a **new terminal** and run:

```bash
ngrok http 5000
```

You'll see output like:
```
Forwarding    https://unformalistic-unlikely-glady.ngrok-free.app -> http://localhost:5000
```

**Copy the HTTPS URL** (e.g., `https://unformalistic-unlikely-glady.ngrok-free.app`)

### 4. Start AI Monitoring

Open **another new terminal** and run:

```bash
curl -X POST http://localhost:5000/demo/start-monitoring
```

This initializes the AI detection system for booth monitoring.

### 5. Update Android App

#### Update the Backend URL

1. Open the Android project in Android Studio
2. Navigate to `FirstFragment.java`
3. Find the `BASE_URL` variable (around line 28)
4. Replace with your ngrok URL:

```java
private static final String BASE_URL = "https://your-ngrok-url.ngrok-free.app/";
```

**Important:** Don't forget the trailing `/` at the end!

### 6. Run the Android App

1. Connect an Android device or start an emulator
2. Click the **Run** button (▶️) in Android Studio
3. Select your device
4. Wait for the app to install and launch

## 🎯 How to Use

### Reserving a Booth

1. **Select a booth** by tapping on any booth card
2. **Click "Reserve Booth"** button
3. The booth will turn **yellow** and be reserved for 10 seconds
4. You'll see a toast message: "Booth reserved for 10 seconds!"

### Booth Status Colors

- 🟢 **Green** - Available (0 people)
- 🟡 **Yellow** - Reserved (10-second reservation)
- 🔴 **Red** - Occupied (people detected)

### Automatic Updates

- The app automatically refreshes booth status every **2 seconds**
- Reservations expire after **10 seconds** and return to available

## 📁 Project Structure

```
seatscout/
├── android-app/                 # Android Studio project
│   ├── app/
│   │   └── src/
│   │       └── main/
│   │           ├── java/
│   │           │   └── com/example/seatscout_android_app/
│   │           │       ├── MainActivity.java
│   │           │       ├── FirstFragment.java
│   │           │       ├── ApiService.java
│   │           │       └── models/
│   │           └── res/
│   │               └── layout/
│   │                   ├── activity_main.xml
│   │                   └── fragment_first.xml
│   └── build.gradle
│
└── python-backend/              # Flask backend
    ├── app.py                   # Main Flask application
    ├── models.py                # Space management
    ├── ai_detector.py           # AI/ML detection
    ├── config.py                # Configuration
    └── requirements.txt         # Python dependencies
```

## 🔧 API Endpoints

### Backend API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/check-all-spaces` | GET | Get status of all booths |
| `/check-space/<space_id>` | GET | Get status of specific booth |
| `/reserve-space/<space_id>` | POST | Reserve a booth for 10 minutes |
| `/cancel-reservation/<space_id>` | POST | Cancel booth reservation |
| `/demo/start-monitoring` | POST | Start AI monitoring system |

### Example API Call

```bash
# Check all booth statuses
curl http://localhost:5000/check-all-spaces

# Reserve booth A1
curl -X POST http://localhost:5000/reserve-space/A1
```

## 🐛 Troubleshooting

### App crashes with NullPointerException
- Make sure the backend is running
- Verify the ngrok URL is correct in `FirstFragment.java`
- Check that `/demo/start-monitoring` has been called

### Booth colors don't update
1. Check Android Studio Logcat for errors
2. Verify backend is returning data:
   ```bash
   curl http://localhost:5000/check-all-spaces
   ```
3. Make sure ngrok is still running (URLs expire)

### 500 Internal Server Error
- Restart the Flask server
- Check Python console for error messages
- Verify all dependencies are installed

### ngrok URL expired
- ngrok free tier URLs expire after a few hours
- Run `ngrok http 5000` again to get a new URL
- Update the `BASE_URL` in `FirstFragment.java`

## 🔄 Development Workflow

### Daily Development Routine

**Terminal 1 - Flask Server:**
```bash
cd python-backend
python3 app.py
```

**Terminal 2 - ngrok:**
```bash
ngrok http 5000
# Copy the new URL and update FirstFragment.java
```

**Terminal 3 - Start Monitoring:**
```bash
curl -X POST http://localhost:5000/demo/start-monitoring
```

**Android Studio:**
- Update BASE_URL with new ngrok URL
- Run app on device/emulator

## 📝 Configuration

### Change Reservation Duration

Edit `app.py`:

```python
# Change from 10 minutes to 15 minutes
reservation_end = reservation_time + (15 * 60)  # 15 minutes
```

### Change Update Frequency

Edit `FirstFragment.java`:

```java
// Change from 5 seconds to 10 seconds
handler.postDelayed(this, 10000);  // Update every 10 seconds
```

### Number of Booths

Edit `config.py` to add/remove booths:

```python
INITIAL_SPACES = {
    'A1': {},
    'A2': {},
    # Add more booths here
}
```

## 📱 Testing

### Test Booth Reservation Flow
1. Select booth A1
2. Click "Reserve Booth"
3. Verify booth turns yellow
4. Wait 10 minutes
5. Verify booth returns to green

### Test Multiple Reservations
1. Try to reserve an already reserved booth
2. Should show error: "Booth is already reserved"



**Built with Android Studio, Flask, and YOLOv8 Computer Vision AI**
