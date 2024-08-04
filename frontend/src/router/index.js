import { createRouter, createWebHistory } from 'vue-router';
import DronesView from '../views/DronesView.vue';
import TasksView from '../views/TasksView.vue';
import ImagesView from '../views/ImagesView.vue';

const routes = [
  { path: '/', redirect: '/drones' },
  { path: '/drones', component: DronesView },
  { path: '/tasks', component: TasksView },
  { path: '/images', component: ImagesView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
