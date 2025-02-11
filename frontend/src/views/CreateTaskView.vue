<template>
    <div class="create-task">
      <h2>Dodaj novo opravilo</h2>
      <form @submit.prevent="createTask">
        <input type="text" v-model="task" placeholder="Vnesi opravilo" required />
        
        <input type="date" v-model="taskDate" placeholder=""/>

        <button type="submit">Dodaj</button>
      </form>
  
      <p v-if="message">{{ message }}</p>
    </div>
</template>
  
<script>
import axios from "axios";
import { ref, inject } from "vue";
import { useRouter } from "vue-router";
import { format } from "date-fns";

export default {
  name: "CreateTaskView",
  setup() {
    const task = ref("");
    const message = ref("");
    const router = useRouter();
    const user_id = inject("user_id");
    const task_date = ref(format(new Date(), "yyyy-MM-dd"));
    const API_URL = process.env.VUE_APP_API_URL;
    console.log("📌 API_URL:", API_URL);


    async function createTask() {
      try {
        if (!user_id || user_id.value === null) {
          console.error("❌ Uporabnik ni prijavljen!");
          message.value = "❌ Za dodajanje opravil se morate prijaviti!";
          return;
        }

        console.log("📌 DEBUG: Pošiljam opravilo na backend...");
        const payload = {
          task: task.value,
          done: false,
          user_id: user_id.value,
          date: task_date.value,
        };

        console.log("📌 JSON:", JSON.stringify(payload));

        const response = await axios.post(
          `${API_URL}/api/todos`,
          payload
        );

        console.log("✅ Opravilo uspešno dodano!", response.data);
        message.value = "✅ Opravilo uspešno dodano!";
        task.value = "";

        // Počakamo 1.5 sekunde, nato preusmerimo na dashboard
        setTimeout(() => {
          router.push("/dashboard");
        }, 1500);
      } catch (error) {
        console.error("❌ Napaka pri ustvarjanju opravila:", error.response);

        if (error.response) {
          message.value = `❌ Napaka: ${error.response.data.msg || error.response.data.message}`;
        } else {
          message.value = "❌ Prišlo je do napake!";
        }
      }
    }

    return { task, message, createTask };
  },
};
</script>
  
<style scoped>
.create-task {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

input {
  width: 80%;
  padding: 8px;
  margin: 10px 0;
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
}
</style>
