<template>
  <div>
    <h2>Create New Task</h2>
    <button @click="toggleTaskForm">
      {{ showTaskForm ? 'Hide Task Form' : 'Create New Task' }}
    </button>
    <form v-if="showTaskForm" @submit.prevent="handleCreateTask">
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
        <select v-model="localNewTask.assignedDrones" id="assignedDrones" @focus="fetchDronesOnFocus" multiple>
          <option v-for="drone in drones" :key="drone.id" :value="drone.id">
            {{ drone.name }}
          </option>
        </select>
      </div>
      <button type="submit">Create Task</button>
    </form>
  </div>
</template>

<script>
export default {
  props: ['newTask', 'showTaskForm', 'drones', 'toggleTaskForm', 'createTask', 'fetchDronesOnFocus'],
  data() {
    return {
      localNewTask: { ...this.newTask },
    };
  },
  methods: {
    handleCreateTask() {
      this.$emit('update:newTask', this.localNewTask);
      this.createTask();
    },
  },
};
</script>