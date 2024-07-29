# Web-based UAV Monitoring and Task Execution Platform

## Overview

This project is a web-based UAV monitoring and task execution platform designed to manage drone tasks and retrieve images captured during task execution. The platform includes functionalities for creating tasks, assigning tasks to drones, executing tasks, and retrieving associated images.


## Setup Instructions

### Environment Configuration

Before running the application, make sure to set up your environment variables:

**Create a `.env` file:**
- Copy the contents of the `.env.example` file (in the backend directory) to a new file named `.env`.
- Replace the placeholder values with your actual configuration details.


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
**Create Drones: Use the frontend to add drones.**
**Create Tasks: Define tasks and assign drones via the frontend.**
**Execute Tasks: Trigger task execution, which captures images.**
**View Task Details: Retrieve and view images captured during task execution.**


