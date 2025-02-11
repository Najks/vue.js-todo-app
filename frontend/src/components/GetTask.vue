<template>



  <div class="task-list">
    <h3>📝 Moja opravila</h3>

    <!-- 📅 Navigacija med dnevi -->
    <div class="date-navigation">
      <button @click="prevDay" title="Prejšnji dan">
        <i>
          ⬅️
        </i> </button>
      <span>{{ formattedDate }}</span>
      <button @click="nextDay" title="Naslednji dan">
        <i>➡️</i>
      </button>
      <button @click="goToToday" class="today-btn" title="Današnji dan">
        📅 Danes
      </button>
    </div>

    <!-- 🔎 Iskalnik -->
    <input type="text" v-model="searchQuery" placeholder="Išči po opravilih..." class="search-box" />

    <!-- 📌 Filtri -->
    <div class="filters">
      <button @click="filter = 'all'" :class="{ active: filter === 'all' }">🔎 Vse</button>
      <button @click="filter = 'done'" :class="{ active: filter === 'done' }">✅ Dokončane</button>
      <button @click="filter = 'undone'" :class="{ active: filter === 'undone' }">⏳ Nedokončane</button>
    </div>

    <!-- 🔹 Prikaz opravil -->
    <transition-group name="fade">
      <div v-for="task in filteredTasks" :key="task.id" class="task-card" :class="{ completed: task.done }">
        <TaskItem :taskText="task.task" :taskId="task.id" :taskDone="task.done" :taskDate="task.date"
          @taskUpdated="updateTask" @taskDeleted="deleteTask" />
      </div>
    </transition-group>

    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios";
import TaskItem from "@/components/TaskItem.vue";
import { ref, onMounted, inject, computed, watch } from "vue";
import { format, subDays, addDays } from "date-fns";
import Toast from "./Toast.vue";

export default {
  name: "GetTask",
  components: {
    TaskItem,
  },
  setup() {
    const tasks = ref([]);
    const message = ref("");
    const user_id = inject("user_id");

    const searchQuery = ref("");
    const filter = ref("all");

    const selectedDate = ref(new Date());
    const formattedDate = computed(() => format(selectedDate.value, "yyyy-MM-dd"));

    const API_URL = process.env.VUE_APP_API_URL;
    async function getTasks() {
      if (!user_id.value) return;

      try {
        console.log(`📌 Pridobivam opravila za datum: ${formattedDate.value}`);
        const response = await axios.get(`${API_URL}/api/todos`, {
          params: {
            user_id: user_id.value,
            start_date: formattedDate.value,
            end_date: formattedDate.value
          },
        });

        tasks.value = response.data;
      } catch (error) {
        console.error("❌ Napaka pri pridobivanju opravil:", error);
      }
    }

    async function dropTask(event) {
      let taskText;
      if (typeof event === "string") {
        taskText = event;
      } else {
        taskText = event.dataTransfer.getData("text");
      }

      if (!taskText || !user_id.value) return;

      try {
        const payload = {
          task: taskText,
          done: false,
          user_id: user_id.value,
          date: formattedDate.value,
        }
        const response = await axios.post("${API_URL}/api/todos", payload);
        console.log("✅ Opravilo uspešno dodano!", response.data);
        tasks.value.push(response.data);

      } catch (error) {
        console.error("❌ Napaka pri dodajanju opravila:", error);
      }
    }

    function updateTask(taskId, newText, newDone) {
      const task = tasks.value.find((task) => task.id === taskId);
      if (task) {
        task.task = newText;
        task.done = newDone;
      }
    }

    function deleteTask(taskId) {
      tasks.value = tasks.value.filter((task) => task.id !== taskId);
      message.value = "🗑 Opravilo izbrisano!";
    }

    const filteredTasks = computed(() => {
      return tasks.value
        .filter((task) => task.task.toLowerCase().includes(searchQuery.value.toLowerCase()))
        .filter((task) => {
          if (filter.value === "done") return task.done;
          if (filter.value === "undone") return !task.done;
          return true;
        });
    });

    function prevDay() {
      selectedDate.value = subDays(selectedDate.value, 1);
    }

    function nextDay() {
      selectedDate.value = addDays(selectedDate.value, 1);
    }

    function goToToday() {
      selectedDate.value = new Date();
    }

    // 🛠 Pridobi opravila, ko se datum spremeni
    watch(formattedDate, getTasks);

    onMounted(getTasks);

    return { dropTask, tasks, message, updateTask, deleteTask, searchQuery, filter, filteredTasks, formattedDate, prevDay, nextDay, goToToday };
  },
};
</script>


<style scoped>
/* 📅 Navigacija med dnevi */
.date-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.date-navigation button {
  background: #007bff;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  margin: 0 5px;
}

.date-navigation button:hover {
  background: #0056b3;
}

.today-btn {
  background: #28a745;
}

.today-btn:hover {
  background: #218838;
}

/* 🔎 Iskalno polje */
.search-box {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

/* 📌 Filtrirni gumbi */
.filters {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.filters button {
  background: #ddd;
  padding: 8px 12px;
  margin: 0 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: 0.2s ease-in-out;
}

.filters button.active {
  background: #007bff;
  color: white;
}

.filters button:hover {
  background: #0056b3;
  color: white;
}

/* 📌 Opravila kot kartice */
.task-card {
  background: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  transition: 0.3s ease-in-out;
}

.task-card.completed {
  border-left: 6px solid #28a745;
  opacity: 0.7;
}

.task-card:hover {
  transform: scale(1.02);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.drop-zone {
  background: #f0f0f0;
  padding: 20px;
  margin: 20px 0;
  border-radius: 10px;
  border: 2px dashed #007bff;
  text-align: center;
  font-weight: bold;
  color: #007bff;
  transition: 0.2s;
}

.drop-zone:hover {
  background: #e0e0e0;
}
</style>
