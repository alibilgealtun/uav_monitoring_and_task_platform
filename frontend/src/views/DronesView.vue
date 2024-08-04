<!-- src/views/DronesView.vue -->
<template>
    <DronesTable />
</template>

<script>
import DronesTable from '../components/DronesTable.vue';

export default {
  components: {
    DronesTable,
  },
  data() {
    return {
      droneName: '',
    };
  },
  methods: {

  },
};
</script>
