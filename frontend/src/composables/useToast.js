import {ref} from 'vue'

export function useToast() {
    const message = ref('')
    const isVisible = ref(false)

    function showToast(msg, duration = 3000) {
        message.value = msg 
        isVisible.value = true
        setTimeout(() => {
            isVisible.value = false
        }, duration)
    }

    return {
        message,
        isVisible,
        showToast
    };
}