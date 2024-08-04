<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>Image URL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="image in images" :key="image.id">
          <td>
            <a :href="'http://'+image.image_url" target="_blank">http://{{ image.image_url }}</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  props: {
    taskId: Number,
    images: Array,
  },
}
</script>

<style scoped>
table {
  width: 70%;
  border-collapse: collapse;
  margin: 1rem auto;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 1rem;
  border: 1px solid #ddd;
}

thead {
  background-color: #f4f4f4;
}

img {
  width: 100px;
  height: auto;
}
</style>
