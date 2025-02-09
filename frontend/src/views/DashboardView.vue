<template>
  <div class="dashboard">
    <h2>Dobrodošel, {{ username }}!</h2>
    <p>Tukaj preveri svoje podatke in objave</p>

    <router-link to="/create" class="btn"> Dodaj Opravilo</router-link>
    <GetTask />
  </div>
</template>

<script>
import { inject } from "vue";
import GetTask from "@/components/GetTask.vue";
export default {
  name: "Dashboard",
  components: {
    GetTask 
  },
  setup() {
      const username = localStorage.getItem("username");
      const logout = inject("logout");

      return { username, logout };
  },
};
</script>

<style scoped>
/* 🏠 Glavni kontejner */
.dashboard {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.08);
  text-align: center;
}

/* 📝 Naslov */
h2 {
  font-size: 40px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

/* 📌 Podnaslov */
p {
  font-size: 22px;
  color: #666;
  margin-bottom: 20px;
}

/* ➕ Gumb za dodajanje */
.btn {
  display: inline-block;
  background: #007bff;
  color: #fff;
  padding: 10px 16px;
  text-decoration: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
  border: none;
}

.btn:hover {
  background: #0056b3;
}
</style>
