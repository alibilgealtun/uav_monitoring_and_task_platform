<!-- src/App.vue -->
<template>
  <div id="app">
    <header>
      <nav>
        <a href="https://droneqube.com.tr/">
        <img src="@/assets/images/logo.png" alt="Logo" class="logo" />
        </a>
        <div class="nav-links">
          <router-link to="/drones"><img src="@/assets/images/drone.png" alt="drone"></router-link>
          <router-link to="/tasks"><img src="@/assets/images/task.png" alt="task"></router-link>
          <router-link to="/images"><img src="@/assets/images/image.png" alt="image"></router-link>
        </div>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>
