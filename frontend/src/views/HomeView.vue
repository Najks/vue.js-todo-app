<template>
  <div class="home">
    <h2>Dobrodošli v TODO aplikaciji!</h2>
    <p>Upravljajte svoje naloge in ostanite organizirani.</p>

    <div class="buttons">
      <router-link v-if="!user" to="/register" class="btn">📝 Registracija</router-link>
      <router-link v-if="!user" to="/login" class="btn">🔐 Prijava</router-link>
      <router-link v-if="user" to="/dashboard" class="btn dashboard-btn">📋 Moj Dashboard</router-link>
    </div>
  </div>
</template>

<script>
import { inject } from "vue";

export default {
  name: "HomeView",
  setup() {
    const user = inject("user");
    return { user };
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  max-width: 600px;
  margin: 80px auto;
  padding: 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.1);
  transition: 0.3s ease-in-out;
}

h2 {
  font-size: 24px;
  color: #333;
  font-weight: bold;
  margin-bottom: 10px;
}


p {
  font-size: 16px;
  color: #666;
  margin-bottom: 20px;
}


.buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}


.btn {
  display: inline-block;
  padding: 12px 18px;
  background: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  transition: 0.3s ease-in-out;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}


.dashboard-btn {
  background: #007bff;
}


.btn:hover {
  background: #0056b3;
  transform: scale(1.05);
}

.dashboard-btn:hover {
  background: #007bff;;
}
</style>
