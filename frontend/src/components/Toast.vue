<template>
    <transition name="fade">
      <div v-if="toastVisible" class="toast">
        {{ toastMessage }}
      </div>
    </transition>
  </template>
  
  <script>
  import { inject } from "vue";
  
  export default {
    name: "Toast",
    setup() {
      const toastMessage = inject("toastMessage"); // ✅ Pravilno injektamo toast message
      const toastVisible = inject("toastVisible"); // ✅ Pravilno injektamo toast vidnost
  
      return { toastMessage, toastVisible };
    },
  };
  </script>
  
  <style scoped>
  .toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #007bff;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
  }
  
  /* Animacija za fade-in/fade-out */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  </style>
  