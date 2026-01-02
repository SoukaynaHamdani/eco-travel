# EcoVoyage Morocco - Quick Start Guide

## Running the Application

The application consists of two servers that need to be running:

1. **Backend API Server** (Port 8000)
2. **Frontend Web Server** (Port 8080)

### Option 1: Using the Startup Script

Run the `start_servers.bat` file:
```bash
.\start_servers.bat
```

This will open two separate terminal windows for the backend and frontend servers.

### Option 2: Manual Start

Open two separate terminal windows:

**Terminal 1 - Backend:**
```bash
cd c:\Users\achra\ai_agent
python -m uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd c:\Users\achra\ai_agent
python -m http.server 8080 --directory frontend
```

### Accessing the Application

Once both servers are running, open your browser and navigate to:
```
http://localhost:8080
```

### Stopping the Servers

Use the `stop_servers.bat` script or press `Ctrl+C` in each terminal window.

## Application URLs

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
