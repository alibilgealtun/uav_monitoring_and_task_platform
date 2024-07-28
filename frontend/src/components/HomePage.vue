<template>
  <div id="app">
    <h1>UAV Monitoring and Task Execution Platform</h1>
    <div>
      <h2>Create New Task</h2>
      <form @submit.prevent="createTask">
        <div>
          <label for="taskName">Task Name:</label>
          <input type="text" v-model="newTask.name" id="taskName" required />
        </div>
        <div>
          <label for="taskDescription">Description:</label>
          <textarea v-model="newTask.description" id="taskDescription"></textarea>
        </div>
        <div>
          <label for="assignedDrones">Assign Drones:</label>
          <select v-model="newTask.assignedDrones" id="assignedDrones" @focus="fetchDronesOnFocus" multiple>
            <option v-for="drone in drones" :key="drone.id" :value="drone.id">
              {{ drone.name }}
            </option>
          </select>
        </div>
        <button type="submit">Create Task</button>
      </form>
    </div>
    <div>
      <h2>Drone Operations</h2>
      <button @click="toggleDrones">{{ showDrones ? 'Hide Drones' : 'Get Drones' }}</button>
      <div v-if="showDrones && drones.length">
        <h3>Available Drones:</h3>
        <ul>
          <li v-for="(drone, index) in drones" :key="drone.id">
            {{ drone.name }}
            <button @click="toggleTasks(index)">
              {{ showTasks[index] ? 'Hide Tasks' : 'Show Tasks' }}
            </button>
            <div v-if="showTasks[index]">
              <h4>Tasks for {{ drone.name }}</h4>
              <ul>
                <li v-for="task in drone.tasks" :key="task.id">
                  Task: {{ task.name }}
                  <button @click="viewTaskDetails(task.id)">Details</button>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>
      <div>
        <input type="text" v-model="droneName" placeholder="Enter drone name" />
        <button @click="addDrone">Add Drone</button>
      </div>
    </div>

    <div>
      <h2>Task Operations</h2>
      <div>
        <input type="number" v-model="taskId" placeholder="Enter task ID" />
        <button @click="executeTask(taskId)">Execute Task</button>
      </div>
      <div v-if="taskMessage">
        <h3>Task Execution Result:</h3>
        <p>{{ taskMessage }}</p>
        <div v-if="newlyCapturedImages.length">
          <h3>Generated Images:</h3>
          <ul class="image-gallery">
            <li v-for="image in newlyCapturedImages" :key="image.id">
              <img :src="image.image_url" alt="Task Image" />
            </li>
          </ul>
        </div>
      </div>
      <div>
        <input type="number" v-model="taskIdForImages" placeholder="Enter task ID for images" />
        <button @click="getTaskImages">Get Task Images</button>
      </div>
      <div v-if="taskImages.length">
        <h3>Task Images:</h3>
        <ul>
          <li v-for="image in taskImages" :key="image.id">
            <a :href="image.image_url" target="_blank">View Image</a>
          </li>
        </ul>
      </div>
    </div>

    <div>
      <h2>Assign Drone to Task</h2>
      <div>
        <label for="selectDrone">Select Drone:</label>
        <select v-model="selectedDroneId" id="selectDrone" @focus="fetchDronesOnFocus">
          <option disabled value="">Select a drone</option>
          <option v-for="drone in drones" :key="drone.id" :value="drone.id">{{ drone.name }}</option>
        </select>
      </div>
      <div>
        <label for="selectTask">Select Task:</label>
        <select v-model="selectedTaskId" id="selectTask" @focus="fetchTasksOnFocus">
          <option disabled value="">Select a task</option>
          <option v-for="task in allTasks" :key="task.id" :value="task.id">Task: {{ task.name }}</option>
        </select>
      </div>
      <button @click="assignDroneToTask">Assign Drone to Task</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
   setup() {
    const router = useRouter();

    const viewTaskDetails = (taskId) => {
      router.push({ name: 'TaskDetails', params: { id: taskId } });
    };

    return {
      viewTaskDetails,
    };
  },
  data() {
    return {
      drones: [],
      newTask: {
        name: '',
        description: '',
        assignedDrones: []
      },
      droneName: "",
      taskId: null,
      taskMessage: "",
      taskIdForImages: null,
      taskImages: [], // Images retrieved by "Get Task Images"
      newlyCapturedImages: [], // New images captured by "Execute Task"
      showDrones: false,
      showTasks: [], // Array to track the visibility of tasks for each drone
      allTasks: [], // All available tasks
      selectedDroneId: "",
      selectedTaskId: ""
    };
  },
  methods: {
    fetchTasksOnFocus() {
      if (this.allTasks.length === 0) {
        this.fetchAllTasks();
      }
    },
    fetchDronesOnFocus() {
      if (this.drones.length === 0) {
        this.getDrones();
      }
    },
    toggleDrones() {
      if (!this.showDrones) {
        this.getDrones();
      }
      this.showDrones = !this.showDrones;
    },
    getDrones() {
      axios.get('http://127.0.0.1:5000/api/drones')
        .then(response => {
          this.drones = response.data;
          this.showTasks = new Array(this.drones.length).fill(false);
        })
        .catch(err => {
          console.error(err);
        });
    },
    addDrone() {
      if (!this.droneName.trim()) {
        alert("Please enter a drone name.");
        return;
      }
      axios.post('http://127.0.0.1:5000/api/drones', { name: this.droneName })
        .then(response => {
          this.drones.push(response.data);
          this.showTasks.push(false);
          this.droneName = "";
        })
        .catch(err => {
          console.error(err);
        });
    },
    toggleTasks(index) {
      this.$set(this.showTasks, index, !this.showTasks[index]);
    },
    executeTask(id) {
      if (!id) {
        alert("Please enter a valid task ID.");
        return;
      }
      axios.post(`http://127.0.0.1:5000/api/tasks/${id}/execute`)
        .then(response => {
          this.taskMessage = response.data.message;
          this.newlyCapturedImages = response.data.images;  // Update newly captured images
          this.taskImages = [];
        })
        .catch(err => {
          console.error(err);
        });
    },
    getTaskImages() {
      if (!this.taskIdForImages) {
        alert("Please enter a valid task ID.");
        return;
      }
      axios.get(`http://127.0.0.1:5000/api/tasks/${this.taskIdForImages}/images`)
        .then(response => {
          this.taskImages = response.data; // Update task images
          this.newlyCapturedImages = []; // Clear newly captured images
        })
        .catch(err => {
          console.error(err);
        });
    },
    fetchAllTasks() {
      axios.get('http://127.0.0.1:5000/api/tasks')
        .then(response => {
          this.allTasks = response.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    assignDroneToTask() {
      if (!this.selectedDroneId || !this.selectedTaskId) {
        alert("Please select both a drone and a task.");
        return;
      }
      axios.put(`http://127.0.0.1:5000/api/tasks/${this.selectedTaskId}/assign`, {
        drone_id: this.selectedDroneId
      })
      .then(() => {
        alert('Task successfully assigned to drone.');
        this.fetchAllTasks(); // Refresh tasks after assignment
      })
      .catch(err => {
        console.error(err);
      });
    },
    createTask() {
      const taskData = {
        name: this.newTask.name,
        description: this.newTask.description,
        drone_id: this.newTask.assignedDrones[0] || null // Assuming you are assigning only one drone
      };

      axios.post('http://127.0.0.1:5000/api/tasks', taskData)
        .then(response => {
          console.log('Task created successfully:', response.data);
          alert("Created successfully.");
          this.newTask = {
            name: '',
            description: '',
            assignedDrones: []
          }; // Reset the form
        })
        .catch(error => {
          console.error('Error creating task:', error);
        });
    },

  },
  mounted() {
    this.fetchAllTasks();
    this.getDrones();
  }
}
</script>
