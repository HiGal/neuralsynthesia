<template>
  <div id="app">
    <ParticleBackground />
    <HomePage />
  </div>
</template>

<script setup>
import HomePage from './components/HomePage.vue'
import ParticleBackground from './components/ParticleBackground.vue'
</script>

<style>
#app {
  position: relative;
  width: 100%;
  min-height: 100vh;
}
</style>
