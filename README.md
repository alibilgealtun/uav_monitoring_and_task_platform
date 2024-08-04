# UAV Monitoring and Task Platform

This project is a web-based UAV monitoring and task execution platform built with a Flask backend and a Vue.js frontend. The platform allows users to create and assign tasks to drones, execute tasks, and view the results.

## Features

- Create, assign, and manage tasks for drones
- Execute tasks and view the associated images
- Paginated list of drones and their tasks

## Prerequisites

- Docker and Docker Compose installed

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Clone the Repository
   ```bash
   git clone https://github.com/alibilgealtun/uav_monitoring_and_task_platform.git
   cd uav_monitoring_and_task_platform
   ```
### Build and Run the Application
   ```bash
   docker-compose up --build
   ```

### Access the frontend and backend applications in your browser:
- Frontend UI: http://localhost:8080
- Backend API: http://localhost:5000
- Minio UI: http://localhost:9001/login
- Minio Username: miniouser123
- Minio Password: miniokey123



