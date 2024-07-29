# Web-based UAV Monitoring and Task Execution Platform

## Overview

This project is a web-based UAV monitoring and task execution platform designed to manage drone tasks and retrieve images captured during task execution. The platform includes functionalities for creating tasks, assigning tasks to drones, executing tasks, and retrieving associated images.

## Features

### Backend (Python Flask)
- **Flask Application**: Serves as the backend for the UAV monitoring platform.
- **RESTful API**:
  - `GET /api/drones`: Retrieve a list of drones with basic information.
  - `POST /api/tasks`: Create a new task with details such as task name, description, and assigned drone(s).
  - `GET /api/tasks/:id`: Retrieve details of a specific task, including associated drone(s).
  - `POST /api/tasks/:id/execute`: Execute a task, triggering image capture by the assigned drone(s). Five random noisy images are generated and stored during this execution.
  - `GET /api/tasks/:id/images`: Retrieve images captured during the execution of a task.

- **Database Schema**:
  - **Drone**: Stores information about drones.
  - **Task**: Manages tasks, associated with one or more drones.
  - **Image**: Stores images captured during task execution.
  - **Relationships**: One-to-many relationship between Drone and Task tables.

### Frontend (Vue.js)
- **Task Management**: Create tasks, assign drones to tasks, and execute tasks.
- **Task Details**: View task details, including associated drones and captured images.
- **Image Retrieval**: Retrieve and display images captured during task execution.

## Setup Instructions

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/)
- [Node.js 14+](https://nodejs.org/en/download/)
- [MinIO](https://min.io/)

### Backend Setup
1. **Navigate to the backend directory**:
   ```bash
   cd backend
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Run flask**:
   ```bash
   python run.py


### Frontend Setup
1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
2. **Install dependencies**:
   ```bash
   npm install
3. **Run the frontend application**:
   ```bash
   npm run serve
4. **The frontend server will start, and you can access it via the URL provided by the terminal (typically http://localhost:8080).**

### Minio Setup 
1. **Download MinIO from the official website.**
2. **Run Minio**
   ```bash
   .\minio.exe server C:\minio --console-address :9001
3. **MinIO will start, and the console can be accessed at http://localhost:9001.**


### Usage
# Create Drones: Use the frontend to add drones.
# Create Tasks: Define tasks and assign drones via the frontend.
# Execute Tasks: Trigger task execution, which captures images.
# View Task Details: Retrieve and view images captured during task execution.


