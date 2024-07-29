<template>
  <div>
    <h2>Adding drones</h2>
    <input type="text" v-model="localDroneName" placeholder="Enter drone name" />
    <button @click="handleAddDrone">Add Drone</button>
  </div>
</template>

<script>
export default {
  props: ['droneName', 'addDrone'],
  data() {
    return {
      localDroneName: this.droneName,
    };
  },
  methods: {
    handleAddDrone() {
      this.$emit('update:droneName', this.localDroneName);
      this.addDrone();
    },
  },
};
</script>