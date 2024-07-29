<template>
  <div id="app">
    <h1>UAV Monitoring and Task Execution Platform</h1>
    <!-- Add Drone Component -->
    <AddDrone :droneName="droneName" @update:droneName="droneName = $event" :addDrone="addDrone" />
    <!-- Drone Operations Component -->
    <DroneOperations
      :drones="drones"
      :showDrones="showDrones"
      :showTasks="showTasks"
      :toggleDrones="toggleDrones"
      :toggleTasks="toggleTasks"
      :toggleTaskDetails="toggleTaskDetails"
    />
    <!-- Task Operations Component -->
    <TaskOperations
      :allTasks="allTasks"
      :showTaskList="showTaskList"
      :showTaskDetails="showTaskDetails"
      :selectedTask="selectedTask"
      :taskId="taskId"
      :taskMessage="taskMessage"
      :newlyCapturedImages="newlyCapturedImages"
      @update:taskId="taskId = $event"
      :toggleTaskList="toggleTaskList"
      :toggleTaskDetails="toggleTaskDetails"
      :executeTask="executeTask"
    />
    <!-- Create Task Component -->
    <CreateTask
      :newTask="newTask"
      @update:newTask="newTask = $event"
      :showTaskForm="showTaskForm"
      :drones="drones"
      :toggleTaskForm="toggleTaskForm"
      :createTask="createTask"
      :fetchDronesOnFocus="fetchDronesOnFocus"
    />
    <!-- Assign Drone to Task Component -->
    <AssignDroneToTask
      :selectedDroneId="selectedDroneId"
      @update:selectedDroneId="selectedDroneId = $event"
      :selectedTaskId="selectedTaskId"
      @update:selectedTaskId="selectedTaskId = $event"
      :drones="drones"
      :allTasks="allTasks"
      :fetchDronesOnFocus="fetchDronesOnFocus"
      :fetchTasksOnFocus="fetchTasksOnFocus"
      :assignDroneToTask="assignDroneToTask"
    />
  </div>
</template>

<script>
import axios from 'axios';
import AddDrone from './AddDrone.vue';
import DroneOperations from './DroneOperations.vue';
import TaskOperations from './TaskOperations.vue';
import CreateTask from './CreateTask.vue';
import AssignDroneToTask from './AssignDroneToTask.vue';

export default {
  components: {
    AddDrone,
    DroneOperations,
    TaskOperations,
    CreateTask,
    AssignDroneToTask,
  },
  data() {
    return {
      drones: [],
      newTask: {
        name: '',
        description: '',
        assignedDrones: [],
      },
      droneName: '',
      taskId: null,
      taskMessage: '',
      taskIdForImages: null,
      taskImages: [],
      newlyCapturedImages: [],
      showDrones: false,
      showTasks: [],
      allTasks: [],
      selectedDroneId: '',
      selectedTaskId: '',
      showTaskForm: false,
      showTaskList: false,
      selectedTask: null,
      showTaskDetails: false,
    };
  },
  methods: {
    // Fetch tasks when the task dropdown is focused
    fetchTasksOnFocus() {
      if (this.allTasks.length === 0) {
        this.fetchAllTasks();
      }
    },
    // Fetch drones when the drone dropdown is focused
    fetchDronesOnFocus() {
      if (this.drones.length === 0) {
        this.getDrones();
      }
    },
    // Toggle the visibility of the drone list
    toggleDrones() {
      if (!this.showDrones) {
        this.getDrones();
      }
      this.showDrones = !this.showDrones;
    },
    // Toggle the visibility of the task form
    toggleTaskForm() {
      this.showTaskForm = !this.showTaskForm;
    },
    // Fetch the list of drones from the server
    getDrones() {
      axios
        .get('http://127.0.0.1:5000/api/drones')
        .then((response) => {
          this.drones = response.data;
          this.showTasks = new Array(this.drones.length).fill(false);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // Add a new drone
    addDrone() {
      if (!this.droneName.trim()) {
        alert('Please enter a drone name.');
        return;
      }
      axios
        .post('http://127.0.0.1:5000/api/drones', { name: this.droneName })
        .then((response) => {
          this.drones.push(response.data);
          this.showTasks.push(false);
          this.droneName = '';
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // Toggle the visibility of tasks for a specific drone
    toggleTasks(index) {
      this.$set(this.showTasks, index, !this.showTasks[index]);
    },
    // Execute a specific task by ID
    executeTask(id) {
      if (!id) {
        alert('Please enter a valid task ID.');
        return;
      }
      axios
        .post(`http://127.0.0.1:5000/api/tasks/${id}/execute`)
        .then((response) => {
          this.fetchAllTasks();
          this.taskMessage = response.data.message;
          this.newlyCapturedImages = response.data.images.slice(-5);
          this.taskImages = [];
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            alert('Task not found. Please enter a valid task ID.');
          } else {
            console.error(error);
          }
        });
    },
    // Fetch images for a specific task by ID
    getTaskImages() {
      if (!this.taskIdForImages) {
        alert('Please enter a valid task ID.');
        return;
      }
      axios
        .get(`http://127.0.0.1:5000/api/tasks/${this.taskIdForImages}/images`)
        .then((response) => {
          this.taskImages = response.data.images;
          this.newlyCapturedImages = [];
        })
        .catch((err) => {
          alert("There is an error, make sure everything's correct!");
          console.error(err);
        });
    },
    // Fetch all tasks from the server
    fetchAllTasks() {
      axios
        .get('http://127.0.0.1:5000/api/tasks')
        .then((response) => {
          this.allTasks = response.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // Assign a drone to a specific task
    assignDroneToTask() {
      if (!this.selectedDroneId || !this.selectedTaskId) {
        alert('Please select both a drone and a task.');
        return;
      }
      axios
        .put(`http://127.0.0.1:5000/api/tasks/${this.selectedTaskId}/assign`, {
          drone_id: this.selectedDroneId,
        })
        .then(() => {
          alert('Task successfully assigned to drone.');
          this.fetchAllTasks();
          this.getDrones();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // Create a new task
    createTask() {
      const taskData = {
        name: this.newTask.name,
        description: this.newTask.description,
        drone_ids: this.newTask.assignedDrones,
      };

      axios
        .post('http://127.0.0.1:5000/api/tasks', taskData)
        .then((response) => {
          this.fetchAllTasks();
          console.log('Task created successfully:', response.data);
          alert('Created successfully.');
          this.newTask = {
            name: '',
            description: '',
            assignedDrones: [],
          };
          this.showTaskForm = false;
        })
        .catch((error) => {
          console.error('Error creating task:', error);
        });
    },
    // Toggle the visibility of the task list
    toggleTaskList() {
      this.showTaskList = !this.showTaskList;
    },
    // Toggle the visibility of task details
    toggleTaskDetails(task) {
      this.showTaskDetails = !!task;
      this.selectedTask = task;

      if (task && task.images) {
        this.selectedTask.images = task.images;
      } else {
        this.selectedTask.images = [];
      }
    },
  },
  mounted() {
    this.fetchAllTasks();
    this.getDrones();
  },
};
</script>