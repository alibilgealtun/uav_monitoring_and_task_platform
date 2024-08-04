<template>
  <div v-if="showTaskForm" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>Create Task</h2>
      <form @submit.prevent="handleCreateTask">
        <div>
          <label for="taskName">Task Name:</label>
          <input type="text" v-model="localNewTask.name" id="taskName" required />
        </div>
        <div>
          <label for="taskDescription">Description:</label>
          <textarea v-model="localNewTask.description" id="taskDescription"></textarea>
        </div>
        <div>
          <label for="assignedDrones">Assign Drones:</label>
          <select v-model="localNewTask.assignedDrones" id="assignedDrones" multiple>
            <option v-for="drone in drones" :key="drone.id" :value="drone.id">
              {{ drone.name }}
            </option>
          </select>
        </div>
        <button @click="close">Cancel</button>
        <span class="spacer"></span>
        <button type="submit">Create Task</button>

      </form>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  props: {
    showTaskForm: Boolean,
    fetchDrones: Function, // Add a prop to fetch drones
  },
  data() {
    return {
      localNewTask: {
        name: '',
        description: '',
        assignedDrones: [],
      },
      drones: [],
    };
  },
  methods: {
    async handleCreateTask() {
      const taskData = {
        name: this.localNewTask.name,
        description: this.localNewTask.description,
        drone_ids: this.localNewTask.assignedDrones,
      };
      try {
        await api.createTask(taskData);
        this.$emit('task-created');
        this.close();
      } catch (err) {
        console.error("Error creating task:", err);
      }
    },
    close() {
      this.$emit('close-modal');
    },
  },
  watch: {
    showTaskForm(newVal) {
      if (newVal) {
        this.fetchDrones().then(drones => {
          this.drones = drones;
        });
      }
    }
  }
};
</script>

<style>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  max-width: 500px;
  width: 100%;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  cursor: pointer;
}
.modal {
  background: white;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.close {
  font-size: 1.5rem;
  cursor: pointer;
}
button:last-child{
  background-color: blueviolet;
}
</style>
