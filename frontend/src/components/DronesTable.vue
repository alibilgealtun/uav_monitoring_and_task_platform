<template>
  <div>
    <h1>Drones Table</h1>
    <div class="addDroneDiv">
      <input v-model="droneName" placeholder="Drone Name" />
      <button @click="addDrone">Add Drone</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>Drone ID</th>
          <th>Drone Name</th>
          <th>Tasks</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="drone in drones" :key="drone.id">
          <td>{{ drone.id }}</td>
          <td>{{ drone.name }}</td>
          <td>
            <ul>
              <li v-for="task in drone.tasks" :key="task.id">
                {{ task.name }}
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="nextPageDiv">
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span class="spacer"></span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
        <span class="spacer"></span>

      <span>Page {{ currentPage }} of {{ totalPages }}</span>
    </div>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
    return {
      drones: [],
      droneName: '',
      currentPage: 1,
      totalPages: 1,
      perPage: 10,
    };
  },
  methods: {
    async addDrone() {
      if (!this.droneName.trim()) {
        alert("Please enter a drone name.");
        return;
      }
      try {
        await api.addDrone(this.droneName);
        this.droneName = '';
        await this.fetchDrones();
      } catch (err) {
        console.error("Error adding drone.", err);
      }
    },
    async fetchDrones(page = 1) {
      try {
        const response = await api.getDrones(page, this.perPage);
        this.drones = response.drones;
        this.currentPage = response.current_page;
        this.totalPages = response.pages;
      } catch (err) {
        console.error("Error fetching drones:", err);
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.fetchDrones(this.currentPage - 1);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.fetchDrones(this.currentPage + 1);
      }
    },
  },
  mounted() {
    this.fetchDrones();
  },
};
</script>


<style scoped>
.dronesTable {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.addDroneDiv {
  display: flex;
  justify-content: center;
  align-content: center;
}

.addDroneDiv button {
  margin-left: 15px;
  padding: 0 10px;
}

.addDroneDiv input {
  margin-top:10px;
  width: 15%;
}

table {
  width: 70%;
  margin: 1rem auto;
  border-collapse: collapse;
  background-color: white;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f9;
}

.nextPageDiv {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  align-content: center;
}

.spacer {
  display: inline-block;
  width: 5px;
}
.nextPageDiv span:last-child{
  margin-top:5px;
}
</style>
