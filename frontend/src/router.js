import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/Home.vue';
import TaskDetails from './components/TaskDetails.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/tasks/:id', name: 'TaskDetails', component: TaskDetails },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
