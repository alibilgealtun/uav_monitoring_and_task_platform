<template>
  <div>
    <h1>Tasks and Images</h1>
    <div v-if="tasks.length">
      <div v-for="task in tasks" :key="task.id" class="task">
        <h2>Task ID: {{ task.id }}</h2>
        <ImagesTable :taskId="task.id" :images="task.images" />
      </div>
    </div>
    <div v-else>
      <p>No tasks found.</p>
    </div>
  </div>
</template>

<script>
import ImagesTable from '../components/ImagesTable.vue';
import api from "@/api";

export default {
  data() {
    return {
      tasks: [],
    };
  },
  components: {
    ImagesTable,
  },
  async created() {
    try {
      this.tasks = await api.getTasksWithImages();
    } catch (err) {
      console.error("Error fetching tasks with images:", err);
    }
  },
};
</script>

<style>
.task {
  margin-bottom: 2rem;
}
</style>
