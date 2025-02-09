<template>
  <UserContextProvider>
    <Navbar />
    <router-view />
    <Toast /> <!-- ✅ Dodano, da je Toast vedno prisoten -->
  </UserContextProvider>
</template>

<script>
import { provide } from "vue";
import Navbar from "./components/Navbar.vue";
import UserContextProvider from "./components/UserContextProvider.vue";
import Toast from "@/components/Toast.vue";
import { useToast } from "@/composables/useToast"; // ✅ Pravilno uvozi toast composable

export default {
  name: "App",
  components: {
    Navbar,
    UserContextProvider,
    Toast
  },
  setup() {
    const { message, isVisible, showToast } = useToast(); // ✅ Inicializiraj toast sistem

    // ✅ Provide toast podatke v celotni aplikaciji
    provide("toastMessage", message);
    provide("toastVisible", isVisible);
    provide("showToast", showToast);

    return {};
  },
};
</script>

<style>
body {
  background-image: url("./assets/page-turner.svg");
  background-size: cover;
  font-family: "Poppins", sans-serif;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  
}
</style>