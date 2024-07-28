<template>
  <div id="app">
    <h1>UAV Monitoring and Task Execution Platform</h1>

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
                  Task ID: {{ task.id }}
                  <button @click="executeTask(task.id)">Execute Task</button>
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      drones: [],
      droneName: "",
      taskId: null,
      taskMessage: "",
      taskIdForImages: null,
      taskImages: [],
      showDrones: false,
      showTasks: [] // Array to track the visibility of tasks for each drone
    };
  },
  methods: {
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
          this.taskImages = response.data;
        })
        .catch(err => {
          console.error(err);
        });
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
h1 {
  margin-bottom: 30px;
}
h2, h3, h4 {
  margin-top: 20px;
}
input[type="text"], input[type="number"] {
  margin-right: 10px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  margin-top: 10px;
  padding: 10px 15px;
  font-size: 14px;
  color: white;
  background-color: #42b983;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #369d72;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 5px 0;
}
</style>
