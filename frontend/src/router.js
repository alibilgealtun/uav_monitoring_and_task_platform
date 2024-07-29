import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/Home.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
