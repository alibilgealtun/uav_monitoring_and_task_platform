<template>
  <div v-if="show">
    <div class="modal-overlay" @click="close"></div>
    <div class="modal-content">
      <h2>Assign Drones to Task</h2>
      <div>
        <label for="assignedDrones">Assign Drones:</label>
        <select v-model="assignedDrones" id="assignedDrones" multiple>
          <option v-for="drone in drones" :key="drone.id" :value="drone.id">
            {{ drone.name }}
          </option>
        </select>
      </div>
      <button @click="close">Cancel</button>
      <span class="spacer"></span>
      <button @click="assignDrones">Assign</button>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  props: {
    show: Boolean,
    taskId: Number,
    fetchDrones: Function, // Add a prop for the fetchDrones method
  },
  data() {
    return {
      drones: [],
      assignedDrones: [],
    };
  },
  methods: {
    async assignDrones() {
      try {
        await api.assignTask(this.taskId, this.assignedDrones);
        this.$emit('task-updated');
        this.close();
      } catch (err) {
        console.error("Error assigning drones:", err);
      }
    },
    close() {
      this.$emit('close-modal');
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.fetchDrones().then(drones => {
          this.drones = drones;
        });
      }
    }
  }
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}
.modal-content {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>
