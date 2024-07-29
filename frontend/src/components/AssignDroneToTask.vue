<template>
  <div>
    <h2>Assign Drone to Task</h2>
    <div id="assignDroneDiv">
      <div class="selecting">
        <label for="selectDrone">Select Drone:</label>
        <select v-model="localSelectedDroneId" id="selectDrone" @focus="fetchDronesOnFocus">
          <option disabled value="">Select a drone</option>
          <option v-for="drone in drones" :key="drone.id" :value="drone.id">{{ drone.name }}</option>
        </select>
      </div>
      <div class="selecting">
        <label for="selectTask">Select Task:</label>
        <select v-model="localSelectedTaskId" id="selectTask" @focus="fetchTasksOnFocus">
          <option disabled value="">Select a task</option>
          <option v-for="task in allTasks" :key="task.id" :value="task.id">Task: {{ task.name }}</option>
        </select>
      </div>
      <button @click="handleAssignDroneToTask">Assign Drone to Task</button>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'selectedDroneId',
    'selectedTaskId',
    'drones',
    'allTasks',
    'fetchDronesOnFocus',
    'fetchTasksOnFocus',
    'assignDroneToTask',
  ],
  data() {
    return {
      localSelectedDroneId: this.selectedDroneId,
      localSelectedTaskId: this.selectedTaskId,
    };
  },
  methods: {
    handleAssignDroneToTask() {
      this.$emit('update:selectedDroneId', this.localSelectedDroneId);
      this.$emit('update:selectedTaskId', this.localSelectedTaskId);
      this.assignDroneToTask();
    },
  },
};
</script>