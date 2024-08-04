<!-- src/views/TasksView.vue -->
<template>
    <TasksTable ref="tasksTable" />
</template>

<script>
import TasksTable from '../components/TasksTable.vue';

export default {
  components: {
    TasksTable,
  },
  data() {
    return {
      newTask: {
        name: '',
        description: '',
      },
    };
  },

};
</script>
