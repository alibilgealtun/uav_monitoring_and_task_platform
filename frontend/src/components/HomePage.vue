<template>
  <div id="app">
    <h1>UAV Monitoring and Task Execution Platform</h1>


    <div>
      <h2>Adding drones</h2>
        <input type="text" v-model="droneName" placeholder="Enter drone name" />
        <button @click="addDrone">Add Drone</button>
      </div>

    <!-- Drone Operations Section -->
    <div>
      <h2>Get Drones</h2>

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
                  <button @click="toggleTaskDetails(task)">Details</button>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>

    </div>

        <!-- Task Operations Section -->
    <div>
      <h2>Task Operations</h2>
      <button @click="toggleTaskList">List Tasks</button>
      <div v-if="showTaskList" class="task-list-frame">
        <h3>All Tasks</h3>
        <ul>
          <li v-for="task in allTasks" :key="task.id">
           (Task ID:  {{ task.id }})   <strong>{{ task.name }}</strong>: {{ task.description }}
            <button @click="toggleTaskDetails(task)">Details</button>
          </li>
        </ul>
      </div>
     <div v-if="showTaskDetails" class="task-details-frame">
      <h3>Task Details</h3>
      <p><strong>Task ID:</strong> {{ selectedTask.id}}</p>
      <p><strong>Name:</strong> {{ selectedTask.name }}</p>
      <p><strong>Description:</strong> {{ selectedTask.description }}</p>
      <p><strong>Drone ID:</strong> {{ selectedTask.drone_id }}</p>

      <p><strong>Images:</strong></p>
      <ul class="image-gallery" v-if="selectedTask.images.length">
        <li v-for="image in selectedTask.images" :key="image.id">
          <a :href="image.image_url" target="_blank">{{ image.image_url }}</a>
        </li>
      </ul>

      <button @click="toggleTaskDetails(null)">Close Details</button>
    </div>


      <h2> Executing Specific Task </h2>
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
    <a :href="image.image_url" target="_blank">{{ image.image_url }}</a>
  </li>
</ul>

        </div>
      </div>


    </div>

    <!-- Create New Task Section -->
    <div>
      <h2>Create New Task</h2>
      <button @click="toggleTaskForm">
        {{ showTaskForm ? 'Hide Task Form' : 'Create New Task' }}
      </button>
      <form v-if="showTaskForm" @submit.prevent="createTask">
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

    <!-- Assign Drone to Task Section -->
    <h2>Assign Drone to Task</h2>

    <div id="assignDroneDiv">
      <div class="selecting">
        <label for="selectDrone">Select Drone:</label>
        <select v-model="selectedDroneId" id="selectDrone" @focus="fetchDronesOnFocus">
          <option disabled value="">Select a drone</option>
          <option v-for="drone in drones" :key="drone.id" :value="drone.id">{{ drone.name }}</option>
        </select>
      </div>
      <div class="selecting">
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

export default {
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
      taskImages: [],
      newlyCapturedImages: [],
      showDrones: false,
      showTasks: [],
      allTasks: [],
      selectedDroneId: "",
      selectedTaskId: "",
      showTaskForm: false,
      showTaskList: false,
      selectedTask: null,
      showTaskDetails: false,
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
    toggleTaskForm() {
      this.showTaskForm = !this.showTaskForm;
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
        this.fetchAllTasks();
        this.taskMessage = response.data.message;
        this.newlyCapturedImages = response.data.images.slice(-5);
        this.taskImages = [];
      })
      .catch(error => {
        if (error.response && error.response.status === 404) {
          alert("Task not found. Please enter a valid task ID.");
        } else {
          console.error(error);
        }
      });
  },
    getTaskImages() {
      if (!this.taskIdForImages) {
        alert("Please enter a valid task ID.");
        return;
      }
      axios.get(`http://127.0.0.1:5000/api/tasks/${this.taskIdForImages}/images`)
        .then(response => {
          this.taskImages = response.data.images;
          this.newlyCapturedImages = [];
        })
        .catch(err => {
          alert("There is an error, make sure everything's correct!");
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
        this.fetchAllTasks();
        this.getDrones();
      })
      .catch(err => {
        console.error(err);
      });
    },
    createTask() {
      const taskData = {
        name: this.newTask.name,
        description: this.newTask.description,
        drone_ids: this.newTask.assignedDrones
      };

    axios.post('http://127.0.0.1:5000/api/tasks', taskData)
        .then(response => {
          this.fetchAllTasks();
          console.log('Task created successfully:', response.data);
          alert("Created successfully.");
          this.newTask = {
            name: '',
            description: '',
            assignedDrones: []
          };
          this.showTaskForm = false;
        })
        .catch(error => {
          console.error('Error creating task:', error);
        });
    },
    toggleTaskList() {
      this.showTaskList = !this.showTaskList;
    },
    toggleTaskDetails(task) {
       this.showTaskDetails = !!task;
      this.selectedTask = task;

      if (task && task.images) {
        this.selectedTask.images = task.images;
      } else {
        this.selectedTask.images = [];
  }
    }
  },
  mounted() {
    this.fetchAllTasks();
    this.getDrones();
  }
}
</script>

<style scoped>
.task-list-frame, .task-details-frame {
  border: 1px solid #ccc;
  padding: 16px;
  margin-top: 16px;
  max-height: 300px;
  overflow-y: auto;
  background-color: #f9f9f9;
}
</style>
