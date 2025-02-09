<template>
    <slot></slot>
  </template>
  
  <script>
  import { ref, provide, onMounted } from "vue";
  
  export default {
    name: "UserContextProvider",
    setup() {
      const user = ref(localStorage.getItem("username") || null);
      const user_id = ref(localStorage.getItem("user_id") || null);
  
      function login(username, user_id) {
        localStorage.setItem("username", username);
        user.value = username;
        localStorage.setItem("user_id", user_id);
      }
  
      function logout() {
        localStorage.removeItem("username");
        localStorage.removeItem("user_id");
        user.value = null;
      }
  
      provide("user", user);
      provide("login", login);
      provide("logout", logout);
      provide("user_id", user_id);
  
      onMounted(() => {
        user.value = localStorage.getItem("username") || null;
      });
  
      return { user, login, logout, user_id };
    },
  };
  </script>
  