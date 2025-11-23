<template>
  <div class="voice-recorder">
    <div class="recorder-container">
      <button
        @mousedown="startRecording"
        @mouseup="stopRecording"
        @touchstart="startRecording"
        @touchend="stopRecording"
        :disabled="isProcessing"
        :class="['record-button', { 'recording': isRecording, 'disabled': isProcessing }]"
      >
        <div class="record-icon">
          <div v-if="isRecording" class="pulse-ring"></div>
          <svg v-if="!isRecording" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" y1="19" x2="12" y2="23"/>
            <line x1="8" y1="23" x2="16" y2="23"/>
          </svg>
          <div v-else class="recording-dot"></div>
        </div>
        <span class="record-text">
          {{ isRecording ? 'Отпустите чтобы остановить' : 'Удерживайте для записи' }}
        </span>
      </button>

      <div v-if="isRecording" class="recording-indicator">
        <div class="timer">{{ recordingTime }}с</div>
        <div class="wave">
          <div class="wave-bar" v-for="n in 5" :key="n"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['recorded'])

const isRecording = ref(false)
const isProcessing = ref(false)
const recordingTime = ref(0)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const stream = ref(null)
let recordingInterval = null

onMounted(async () => {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ audio: true })
  } catch (error) {
    console.error('Error accessing microphone:', error)
    alert('Не удалось получить доступ к микрофону. Пожалуйста, разрешите доступ.')
  }
})

onUnmounted(() => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
  }
  if (recordingInterval) {
    clearInterval(recordingInterval)
  }
})

const startRecording = async () => {
  if (!stream.value || isProcessing.value) return

  try {
    audioChunks.value = []
    recordingTime.value = 0

    mediaRecorder.value = new MediaRecorder(stream.value, {
      mimeType: 'audio/webm;codecs=opus'
    })

    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }

    mediaRecorder.value.onstop = async () => {
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/opus' })
      emit('recorded', audioBlob)
      clearInterval(recordingInterval)
    }

    mediaRecorder.value.start()
    isRecording.value = true

    recordingInterval = setInterval(() => {
      recordingTime.value++
      if (recordingTime.value >= 30) {
        stopRecording()
      }
    }, 1000)
  } catch (error) {
    console.error('Error starting recording:', error)
    alert('Не удалось начать запись')
  }
}

const stopRecording = () => {
  if (!isRecording.value || !mediaRecorder.value) return

  mediaRecorder.value.stop()
  isRecording.value = false
  isProcessing.value = true
  clearInterval(recordingInterval)
}

const setProcessing = (value) => {
  isProcessing.value = value
}

defineExpose({ setProcessing })
</script>

<style scoped>
.voice-recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.recorder-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.record-button {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem 3rem;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  border: none;
  border-radius: var(--radius-xl);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-xl);
  user-select: none;
}

.record-button:hover:not(.disabled) {
  transform: translateY(-4px);
  box-shadow: 0 25px 50px -12px rgba(102, 126, 234, 0.5);
}

.record-button:active:not(.disabled) {
  transform: translateY(-2px);
}

.record-button.recording {
  background: linear-gradient(135deg, var(--color-error) 0%, var(--color-warning) 100%);
  animation: pulse 2s infinite;
}

.record-button.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.record-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid white;
  border-radius: 50%;
  animation: pulse-ring 1.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}

@keyframes pulse-ring {
  0% {
    transform: scale(0.8);
    opacity: 1;
  }
  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

.recording-dot {
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

.record-text {
  font-size: 1rem;
  text-align: center;
  max-width: 200px;
}

.recording-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.timer {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-error);
  font-variant-numeric: tabular-nums;
}

.wave {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 40px;
}

.wave-bar {
  width: 4px;
  background: linear-gradient(to top, var(--color-primary), var(--color-accent));
  border-radius: 2px;
  animation: wave 1s ease-in-out infinite;
}

.wave-bar:nth-child(1) { animation-delay: 0s; }
.wave-bar:nth-child(2) { animation-delay: 0.1s; }
.wave-bar:nth-child(3) { animation-delay: 0.2s; }
.wave-bar:nth-child(4) { animation-delay: 0.3s; }
.wave-bar:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
  0%, 100% {
    height: 10px;
  }
  50% {
    height: 40px;
  }
}

@media (max-width: 768px) {
  .record-button {
    padding: 1.5rem 2rem;
  }

  .record-icon {
    width: 48px;
    height: 48px;
  }

  .record-text {
    font-size: 0.875rem;
  }
}
</style>
