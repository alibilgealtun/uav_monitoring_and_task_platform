<template>
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
</template>

<script>
export default {
  props: ['drones', 'showDrones', 'showTasks', 'toggleDrones', 'toggleTasks', 'toggleTaskDetails'],
};
</script>