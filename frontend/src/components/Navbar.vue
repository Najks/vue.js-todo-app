<template>
  <nav class="navbar">
    <a href="/" class="home-link">
      <h1>Moja TODO aplikacija</h1>
    </a>

    <div class="nav-links">
      <template v-if="user">
        <span class="user">Pozdravljen, {{ user }}!</span>
        <button @click="logout" class="logout-btn">Odjava</button>
      </template>
      <template v-else>
        <router-link to="/register" class="nav-link">Registracija</router-link>
        <router-link to="/login" class="nav-link">Prijava</router-link>
      </template>
    </div>
  </nav>
</template>
  
  <script>
  import { inject } from "vue";
  
  export default {
    name: "Navbar",
    setup() {
      const user = inject("user");
      const logout = inject("logout");
  
      return { user, logout };
    },
  };
  </script>
  
  <style scoped>
/* 📌 Glavni navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: linear-gradient(135deg, #004ea3, #002a5e);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000; /* Poskrbimo, da bo navbar vedno na vrhu */
  border-radius: 5px;
}

/* 📌 Linki v navbarju */
.nav-links {
  display: flex;
  align-items: center;
}

/* 📌 Linki in tekst */
.nav-link, .home-link {
  text-decoration: none;
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-right: 20px;
}

.nav-link:hover {
  text-decoration: underline;
}

/* 📌 Uporabniško ime */
.user {
  font-size: 18px;
  font-weight: bold;
  margin-right: 20px;
  color: white;
}

/* 📌 Gumb za odjavo */
.logout-btn {
  background: #ff4d4d;
  color: white;
  padding: 7px 14px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s ease-in-out;
}

.logout-btn:hover {
  background: #e60000;
}
</style>