<template>
  <div class="tableDiv">
    <h1>Tasks Table</h1>
    <div class="createTask">
      <button @click="showTaskForm = true">Create Task</button>
    </div>
    <CreateTask
      :showTaskForm="showTaskForm"
      :fetchDrones="fetchDrones"
      @close-modal="showTaskForm = false"
      @task-created="fetchTasks"
    />
    <table>
      <thead>
        <tr>
          <th>Task ID</th>
          <th>Task Name</th>
          <th>Description</th>
          <th>Drones</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id">
          <td>{{ task.id }}</td>
          <td>{{ task.name }}</td>
          <td>{{ task.description }}</td>
          <td v-if="task">
            {{ droneIdsJoin(task) }}
          </td>
          <td>
            <button @click="executeTask(task.id)">Execute</button>
            <span class="spacer"></span>
            <button @click="openAssignModal(task.id)" id="assignButton">Assign/Edit Drones</button>
          </td>
        </tr>
      </tbody>
    </table>
    <AssignTask
      :show="showAssignModal"
      :taskId="currentTaskId"
      :fetch-drones="fetchDrones"
      @close-modal="closeAssignModal"
      @task-updated="fetchTasks"
    />
  </div>
</template>

<script>
import api from '../api';
import CreateTask from './CreateTask.vue';
import AssignTask from "@/components/AssignTask.vue";

export default {
  components: {
    CreateTask,
    AssignTask
  },
  data() {
    return {
      tasks: [],
      showTaskForm: false,
      showAssignModal: false,
      currentTaskId: null,
    };
  },
  methods: {
    droneIdsJoin(task) {
      return task?.drones?.join(', ') || 'Not assigned yet! 👀';
    },
    openAssignModal(taskId) {
      this.currentTaskId = taskId;
      this.showAssignModal = true;
    },
    closeAssignModal() {
      this.showAssignModal = false;
      this.currentTaskId = null;
    },
    async fetchTasks() {
      try {
        this.tasks = await api.getTasks();
      } catch (err) {
        console.error("Error fetching tasks:", err);
      }
    },
    async fetchDrones() {
      try {
        const response = await api.getDrones();
        return response.drones; // Return the list of drones
      } catch (err) {
        console.error("Error fetching drones:", err);
        return [];
      }
    },
    async executeTask(taskId) {
      try {
        const response = await api.executeTask(taskId);
        const images = response.images;

        if (images && images.length > 0) {
          // slice because last 5 images are the new ones.
          const imageUrls = images.slice(-5).map(image => image.image_url).join('\n');
            alert(`Executed successfully! Image URLs:\n${imageUrls}`);
        }
      } catch (err) {
        console.error("Error executing task", err);
      }
    },
  },
  mounted() {
    this.fetchTasks();
  },
};
</script>

<style scoped>
.tableDiv {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
}

.createTask {
  display: flex;
  align-content: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.createTask button {
  padding: 15px;
  font-size: 15px;
}

#assignButton {
  background-color: #3A7734;
}

table {
  width: 70%;
  border-collapse: collapse;
  margin: 1rem auto;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f9;
}

td button {
  padding: 0.5rem;
  margin: 0.2rem;
}

.spacer {
  display: inline-block;
  width: 5px;
}
</style>
