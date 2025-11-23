<template>
  <div class="storybook-viewer">
    <div class="storybook-header">
      <h3 class="storybook-title">{{ title }}</h3>
      <p class="storybook-pages">{{ pages.length }} страниц</p>
    </div>

    <div class="pages-container">
      <div v-for="(page, index) in pages" :key="index" class="story-page fade-in">
        <div class="page-number">Страница {{ page.scene_number }}</div>

        <div v-if="page.image_path" class="page-image-container">
          <img
            :src="getImageUrl(page.image_filename)"
            :alt="`Иллюстрация ${page.scene_number}`"
            class="page-image"
            @error="handleImageError"
          />
        </div>
        <div v-else-if="page.error" class="page-error">
          <p>⚠️ Не удалось создать иллюстрацию</p>
        </div>
        <div v-else class="page-loading">
          <div class="spinner"></div>
          <p>Создание иллюстрации...</p>
        </div>

        <div class="page-text">{{ page.text }}</div>
      </div>
    </div>

    <div v-if="htmlPath" class="view-full">
      <a :href="getHtmlUrl()" target="_blank" class="btn btn-primary">
        📖 Открыть полную версию
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  pages: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'Нейросказка'
  },
  storybookPath: {
    type: String,
    required: true
  },
  htmlPath: {
    type: String,
    default: null
  }
})

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

const getImageUrl = (filename) => {
  if (!filename) return ''
  return `${apiBaseUrl}/static/${props.storybookPath}.${filename.split('.')[1]}`
}

const getHtmlUrl = () => {
  if (!props.htmlPath) return ''
  return `${apiBaseUrl}/static/${props.htmlPath}`
}

const handleImageError = (event) => {
  console.error('Failed to load image:', event.target.src)
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="400"%3E%3Crect fill="%23ddd" width="400" height="400"/%3E%3Ctext fill="%23999" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3EИзображение недоступно%3C/text%3E%3C/svg%3E'
}
</script>

<style scoped>
.storybook-viewer {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}

.storybook-header {
  text-align: center;
  margin-bottom: 2rem;
}

.storybook-title {
  font-size: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.storybook-pages {
  color: var(--color-gray-400);
  font-size: 0.9rem;
}

.pages-container {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.story-page {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-xl);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.story-page:hover {
  transform: translateY(-4px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.page-number {
  font-size: 0.875rem;
  color: var(--color-gray-400);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.page-image-container {
  width: 100%;
  margin-bottom: 1.5rem;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.page-image {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease;
}

.story-page:hover .page-image {
  transform: scale(1.02);
}

.page-loading,
.page-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: var(--color-gray-400);
  gap: 1rem;
}

.page-error {
  color: var(--color-warning);
}

.page-text {
  font-size: 1.125rem;
  line-height: 1.8;
  color: var(--color-gray-200);
  text-align: justify;
}

.view-full {
  margin-top: 3rem;
  text-align: center;
}

@media (max-width: 768px) {
  .story-page {
    padding: 1.5rem;
  }

  .storybook-title {
    font-size: 1.5rem;
  }

  .page-text {
    font-size: 1rem;
  }
}
</style>
