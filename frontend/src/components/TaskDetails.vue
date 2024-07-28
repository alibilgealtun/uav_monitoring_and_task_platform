<template>
  <div>
    <h1>Task Details</h1>
    <div v-if="task">
      <h2>{{ task.name }}</h2>
      <p>{{ task.description }}</p>
      <ul>
        <li v-for="drone in task.assignedDrones" :key="drone.id">{{ drone.name }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      task: null,
    };
  },
  created() {
    this.fetchTaskDetails();
  },
  methods: {
    fetchTaskDetails() {
      const taskId = this.$route.params.id; // Retrieve the task ID from the route
      axios.get(`http://127.0.0.1:5000/api/tasks/${taskId}`)
        .then(response => {
          this.task = response.data;
        })
        .catch(error => {
          console.error('Error fetching task details:', error);
        });
    }
  }
}
</script>
