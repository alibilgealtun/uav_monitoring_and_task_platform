<template>
  <div>
    <h2>Task Operations</h2>
    <button @click="toggleTaskList">List Tasks</button>
    <div v-if="showTaskList" class="task-list-frame">
      <h3>All Tasks</h3>
      <ul>
        <li v-for="task in allTasks" :key="task.id">
          (Task ID: {{ task.id }}) <strong>{{ task.name }}</strong>: {{ task.description }}
          <button @click="toggleTaskDetails(task)">Details</button>
        </li>
      </ul>
    </div>
    <div v-if="showTaskDetails" class="task-details-frame">
      <h3>Task Details</h3>
      <p><strong>Task ID:</strong> {{ selectedTask.id }}</p>
      <p><strong>Name:</strong> {{ selectedTask.name }}</p>
      <p><strong>Description:</strong> {{ selectedTask.description }}</p>
      <p><strong>Drone ID:</strong> {{ selectedTask.drone_id }}</p>
      <p><strong>Images:</strong></p>
      <ul class="image-gallery" v-if="selectedTask.images.length">
        <li v-for="image in selectedTask.images" :key="image.id">
          <a :href="image.image_url" target="_blank">{{ image.image_url }}</a>
        </li>
      </ul>
      <button @click="toggleTaskDetails(null)">Close Details</button>
    </div>
    <h2>Executing Specific Task</h2>
    <div>
      <input type="number" v-model="localTaskId" placeholder="Enter task ID" />
      <button @click="handleExecuteTask">Execute Task</button>
    </div>
    <div v-if="taskMessage">
      <h3>Task Execution Result:</h3>
      <p>{{ taskMessage }}</p>
      <div v-if="newlyCapturedImages.length">
        <h3>Generated Images:</h3>
        <ul class="image-gallery">
          <li v-for="image in newlyCapturedImages" :key="image.id">
            <a :href="image.image_url" target="_blank">{{ image.image_url }}</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'allTasks',
    'showTaskList',
    'showTaskDetails',
    'selectedTask',
    'taskId',
    'taskMessage',
    'newlyCapturedImages',
    'toggleTaskList',
    'toggleTaskDetails',
    'executeTask',
  ],
  data() {
    return {
      localTaskId: this.taskId,
    };
  },
  methods: {
    handleExecuteTask() {
      this.$emit('update:taskId', this.localTaskId);
      this.executeTask(this.localTaskId);
    },
  },
};
</script>

<style scoped>
.task-list-frame,
.task-details-frame {
  border: 1px solid #ccc;
  padding: 16px;
  margin-top: 16px;
  max-height: 300px;
  overflow-y: auto;
  background-color: #f9f9f9;
}
</style>