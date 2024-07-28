import Vue from 'vue';
import App from './components/HomePage.vue';
import router from './router';
import './assets/styles.css';

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
