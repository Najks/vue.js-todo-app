<template>
  <div class="form-container">
    <h2>Registracija</h2>
    <form @submit.prevent="registerUser">
      <label>Uporabniško ime:</label>
      <input type="text" v-model="username" required />

      <label>Geslo:</label>
      <input type="password" v-model="password" required />

      <button type="submit">Registriraj se</button>
    </form>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "RegisterView",
  data() {
    return {
      username: "",
      password: "",
      message: "",
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/auth/register",
          {
            username: this.username,
            password: this.password,
          }
        );
        this.message = response.data.message;
      } catch (error) {
        this.message =
          error.response?.data?.message || "Napaka pri registraciji.";
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  text-align: center;
  max-width: 600px;
  margin: 80px auto;
  padding: 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.1);
  transition: 0.3s ease-in-out;
}

input {
  width: 100%;
  padding: 5px;
  margin-top: 5px;
  margin-bottom: 13px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input:focus {
  outline: none;
  border-color: #007bff;
}

input::placeholder {
  color: #ccc;
}

button {
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

button:hover {
  background: #0056b3;
  cursor: pointer;
}

label {
  font-size: 18px;
  color: #666;
}
</style>