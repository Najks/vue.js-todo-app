<template>
  <div class="task">
    <template v-if="isEditing">
      <input
        type="text"
        v-model="editableText"
        ref="editInput"
      />
      <div class="buttons">
        <button class="save-btn" @click="saveEdit">💾</button>
        <button class="cancel-btn" @click="cancelEdit">❌</button>
      </div>
    </template>
    <template v-else>
      <p>{{ taskText }}</p>
      <div class="task-buttons">
        <button v-if="!taskDone" class="done-btn" @click="markAsDone">✔</button>
        <button v-if="taskDone" class="undo-btn" @click="undoTask">🔄</button>
        <button class="delete-btn" @click="deleteTask">🗑</button>
        <button class="edit-btn" @click="startEditing">✏️</button>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, watch, nextTick, inject } from "vue";
import axios from "axios";

export default {
  name: "TaskItem",
  props: {
    taskId: Number,
    taskText: String,
    taskDone: Boolean,
  },
  setup(props, { emit }) {
    const isEditing = ref(false);
    const editableText = ref(props.taskText);
    const originalText = ref(props.taskText);
    const editInput = ref(null);
    const showToast = inject("showToast");
    const API_URL = process.env.VUE_APP_API_URL;
    console.log("📌 API_URL:", API_URL);

    function startEditing() {
      isEditing.value = true;
      originalText.value = props.taskText;
      nextTick(() => editInput.value?.focus());
    }

    async function saveEdit() {
      if (editableText.value.trim() === "") {
        editableText.value = originalText.value;
        isEditing.value = false;
        return;
      }

      try {
        await axios.put(`${API_URL}/api/todos/${props.taskId}`, {
          task: editableText.value,
        });

        emit("taskUpdated", props.taskId, editableText.value);
        isEditing.value = false;
        showToast("✅ Opravilo uspešno posodobljeno!");
      } catch (error) {
        console.error("❌ Napaka pri shranjevanju:", error);
      }
    }

    function cancelEdit() {
      editableText.value = originalText.value;
      isEditing.value = false;
    }

    async function markAsDone() {
      try {
        await axios.put(`${API_URL}/api/todos/${props.taskId}`, {
          done: true,
        });
        emit("taskUpdated", props.taskId, props.taskText, true);
        showToast("✔ Opravilo označeno kot opravljeno!");
      } catch (error) {
        console.error("❌ Napaka pri označevanju kot opravljeno:", error);
      }
    }

    async function undoTask() {
      try {
        await axios.put(`${API_URL}/api/todos/${props.taskId}`, {
          done: false,
        });
        emit("taskUpdated", props.taskId, props.taskText, false);
        showToast("🔄 Opravilo označeno kot nedokončano!");
      } catch (error) {
        console.error("❌ Napaka pri razveljavitvi opravila:", error);
      }
    }

    async function deleteTask() {
      try {
        await axios.delete(`${API_URL}/api/todos/${props.taskId}`);
        emit("taskDeleted", props.taskId);
        showToast("🗑 Opravilo izbrisano!");
      } catch (error) {
        console.error("❌ Napaka pri brisanju opravila:", error);
      }
    }

    watch(() => props.taskText, (newText) => {
      editableText.value = newText;
      originalText.value = newText;
    });

    return {
      isEditing,
      editableText,
      startEditing,
      saveEdit,
      cancelEdit,
      editInput,
      markAsDone,
      undoTask,
      deleteTask,
    };
  },
};
</script>

<style scoped>
.task {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  margin: 8px 0;
  background: #ffffff;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.08);
  transition: 0.2s ease-in-out;
}

.task:hover {
  background: #f5f5f5;
  border-color: #007bff;
  transform: scale(1.02);
}

.task-buttons {
  display: flex;
  gap: 6px;
}

button {
  padding: 6px 10px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

/* Stil za gumbe */
.done-btn {
  background: #28a745;
  color: white;
}

.undo-btn {
  background: #ffc107;
  color: white;
}

.delete-btn {
  background: #dc3545;
  color: white;
}

.edit-btn {
  background: #007bff;
  color: white;
}

button:hover {
  filter: brightness(90%);
}
</style>
