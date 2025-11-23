<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content fade-in">
          <h1 class="hero-title">
            <span class="text-gradient">Нейросказки</span>
          </h1>
          <p class="hero-subtitle">
            Начните рассказ голосом, и AI создаст иллюстрированную книгу
          </p>
          <div class="hero-features">
            <div class="feature">
              <span class="feature-icon">🎤</span>
              <span>Голосовой ввод</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🤖</span>
              <span>AI генерация текста</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🎨</span>
              <span>Красивые иллюстрации</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="main-content">
      <div class="container">
        <!-- Voice Recorder -->
        <div v-if="!state.isGeneratingText && !state.isGeneratingStorybook && !state.storybookGenerated" class="recorder-section">
          <VoiceRecorder ref="voiceRecorder" @recorded="handleAudioRecorded" />
        </div>

        <!-- Text Generation -->
        <div v-if="state.isGeneratingText" class="status-section fade-in">
          <div class="status-card">
            <div class="spinner"></div>
            <h3>Генерация истории...</h3>
            <p>AI пишет продолжение вашей истории</p>
          </div>
        </div>

        <!-- Story Text -->
        <div v-if="state.storyGenerated && !state.isGeneratingStorybook" class="story-section fade-in">
          <div class="story-card">
            <h3>Ваша история готова!</h3>
            <div class="story-text">{{ state.storyText }}</div>
            <p class="story-meta">
              <em>— Нейроавтор, {{ new Date().getFullYear() }}</em>
            </p>
            <div class="story-info">
              📚 Будет создано {{ state.scenes.length }} иллюстраций
            </div>
          </div>
        </div>

        <!-- Storybook Generation -->
        <div v-if="state.isGeneratingStorybook" class="status-section fade-in">
          <div class="status-card">
            <div class="spinner"></div>
            <h3>Создание иллюстраций...</h3>
            <p>AI рисует картинки для каждой сцены</p>
            <div class="progress-info">
              Это может занять 1-2 минуты
            </div>
          </div>
        </div>

        <!-- Storybook Display -->
        <div v-if="state.storybookGenerated" class="storybook-section fade-in">
          <StorybookViewer
            :pages="state.storybookPages"
            :title="state.startStory"
            :storybook-path="state.startStory"
            :html-path="state.htmlPath"
          />

          <div class="actions">
            <button @click="resetApp" class="btn btn-primary">
              🎤 Создать новую историю
            </button>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="state.error" class="error-section fade-in">
          <div class="error-card">
            <h3>❌ Произошла ошибка</h3>
            <p>{{ state.error }}</p>
            <button @click="resetApp" class="btn btn-primary">
              Попробовать снова
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import VoiceRecorder from './VoiceRecorder.vue'
import StorybookViewer from './StorybookViewer.vue'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'
const voiceRecorder = ref(null)

const state = reactive({
  isGeneratingText: false,
  isGeneratingStorybook: false,
  storyGenerated: false,
  storybookGenerated: false,
  storyText: '',
  startStory: '',
  scenes: [],
  storybookPages: [],
  htmlPath: '',
  error: null
})

const handleAudioRecorded = async (audioBlob) => {
  try {
    state.error = null
    state.isGeneratingText = true

    // Upload audio and generate text
    const response = await fetch(`${apiBaseUrl}/get_audio`, {
      method: 'POST',
      body: audioBlob
    })

    if (!response.ok) {
      throw new Error('Не удалось обработать аудио')
    }

    const data = await response.json()

    state.storyText = data.result
    state.startStory = data.start_story
    state.scenes = data.scenes
    state.isGeneratingText = false
    state.storyGenerated = true

    // Auto-start storybook generation after a short delay
    setTimeout(() => {
      generateStorybook()
    }, 2000)

  } catch (error) {
    console.error('Error processing audio:', error)
    state.error = error.message || 'Не удалось обработать запись. Попробуйте еще раз.'
    state.isGeneratingText = false
    if (voiceRecorder.value) {
      voiceRecorder.value.setProcessing(false)
    }
  }
}

const generateStorybook = async () => {
  try {
    state.isGeneratingStorybook = true

    const response = await fetch(`${apiBaseUrl}/generate_storybook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        scenes: state.scenes,
        start_story: state.startStory
      })
    })

    if (!response.ok) {
      throw new Error('Не удалось создать книгу')
    }

    const data = await response.json()

    state.storybookPages = data.pages
    state.htmlPath = data.html_path
    state.isGeneratingStorybook = false
    state.storybookGenerated = true

    if (voiceRecorder.value) {
      voiceRecorder.value.setProcessing(false)
    }

  } catch (error) {
    console.error('Error generating storybook:', error)
    state.error = error.message || 'Не удалось создать книгу. Попробуйте еще раз.'
    state.isGeneratingStorybook = false
    if (voiceRecorder.value) {
      voiceRecorder.value.setProcessing(false)
    }
  }
}

const resetApp = () => {
  state.isGeneratingText = false
  state.isGeneratingStorybook = false
  state.storyGenerated = false
  state.storybookGenerated = false
  state.storyText = ''
  state.startStory = ''
  state.scenes = []
  state.storybookPages = []
  state.htmlPath = ''
  state.error = null

  if (voiceRecorder.value) {
    voiceRecorder.value.setProcessing(false)
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  padding: 2rem 0;
}

.hero {
  padding: 4rem 0;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  margin-bottom: 1rem;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: var(--color-gray-300);
  margin-bottom: 3rem;
  line-height: 1.6;
}

.hero-features {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-lg);
  font-size: 1rem;
  color: var(--color-gray-200);
}

.feature-icon {
  font-size: 1.5rem;
}

.main-content {
  padding: 3rem 0;
}

.recorder-section,
.status-section,
.story-section,
.storybook-section,
.error-section {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.status-card,
.story-card,
.error-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-xl);
  padding: 3rem;
  text-align: center;
  max-width: 600px;
  width: 100%;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.status-card h3,
.story-card h3,
.error-card h3 {
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.status-card p {
  color: var(--color-gray-300);
  margin-bottom: 1rem;
}

.progress-info {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: var(--color-gray-400);
}

.story-text {
  background: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  margin: 1.5rem 0;
  text-align: left;
  line-height: 1.8;
  color: var(--color-gray-200);
  font-size: 1.125rem;
}

.story-meta {
  text-align: right;
  color: var(--color-gray-400);
  font-style: italic;
  margin-bottom: 1rem;
}

.story-info {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
  border-radius: var(--radius-lg);
  color: white;
  font-weight: 600;
}

.actions {
  margin-top: 3rem;
  text-align: center;
}

.error-card {
  background: rgba(245, 101, 101, 0.1);
  border-color: var(--color-error);
}

.error-card h3 {
  color: var(--color-error);
  background: none;
  -webkit-background-clip: unset;
  -webkit-text-fill-color: unset;
}

.error-card p {
  color: var(--color-gray-200);
  margin-bottom: 1.5rem;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.125rem;
  }

  .hero-features {
    flex-direction: column;
    align-items: center;
  }

  .status-card,
  .story-card,
  .error-card {
    padding: 2rem 1.5rem;
  }

  .story-text {
    font-size: 1rem;
  }
}
</style>
