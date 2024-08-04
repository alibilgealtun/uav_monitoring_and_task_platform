import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});

function handleResponseStatus(response, successMessage, errorMessage) {
  if (response.status === 200 || response.status === 201) {
    alert(successMessage);
  } else {
    console.error(`${errorMessage} with status ${response.status}`);
    alert(`An error occurred: ${errorMessage}.`);
  }
}

export default {
  async getDrones(page = 1, perPage = 10) {
    try {
      const response = await api.get('/drones', { params: { page, per_page: perPage } });
      return response.data;
    } catch (err) {
      console.error("Error fetching drones:", err);
    }
  },
  async getTasks() {
    try {
      const response = await api.get('/tasks');
      return response.data;
    } catch (err) {
      console.error("Error fetching tasks:", err);
    }
  },
  async executeTask(id) {
    if (!id) {
      alert('Please enter a valid task ID.');
      return;
    }
    const username = prompt("Enter your username: (admin)");
    const password = prompt("Enter your password: (admin)");
    const authHeader = 'Basic ' + btoa(`${username}:${password}`);

    try {
      const response = await api.post(`/tasks/${id}/execute`, null, {
        headers: { 'Authorization': authHeader }
      });
      //handleResponseStatus(response, `Task ${id} executed successfully!`, `Task execution failed`);
      return response.data;

    } catch (error) {
      console.error("Error executing task: ", error);
      alert(`An unexpected error occurred while executing task ${id}. Please try again later.`);
      throw error;
    }
  },
  async addDrone(droneName) {
    try {
      const response = await api.post('/drones', { name: droneName });
      handleResponseStatus(response, `Drone ${droneName} added successfully!`, `Failed to add drone`);
    } catch (error) {
      console.error("Error adding drone: ", error);
      alert(`An unexpected error occurred while adding drone ${droneName}. Please try again later.`);
      throw error;
    }
  },
  async createTask(taskData) {
    try {
      const response = await api.post('/tasks', taskData);
      handleResponseStatus(response, `Task created successfully!`, `Failed to create task`);
    } catch (error) {
      console.error('Error creating task:', error);
      alert(`An unexpected error occurred while creating the task. Please try again later.`);
      throw error;
    }
  },
  async assignTask(taskId, assignedDrones) {
    try {
      const response = await api.put(`/tasks/${taskId}/assign`, { drone_ids: assignedDrones });
      handleResponseStatus(response, `Drones are edited for task ${taskId} successfully!`, `Failed to assign drones`);
    } catch (error) {
      console.error("Error assigning drones: ", error);
      alert(`An unexpected error occurred while assigning drones to task ${taskId}. Please try again later.`);
      throw error;
    }
  },
  async getImages(taskId) {
    try {
      const response = await api.get(`/tasks/${taskId}/images`);
      return response.data;
    } catch (err) {
      console.error("Error fetching images:", err);
    }
  },

  async getTasksWithImages() {
    try {
      const tasks = await this.getTasks();
      return await Promise.all(tasks.map(async (task) => {
        const imagesResponse = await this.getImages(task.id);
        return { ...task, images: imagesResponse || [] };
      }));
    } catch (err) {
      console.error("Error fetching tasks with images:", err);
      throw err;
    }
  }




};
