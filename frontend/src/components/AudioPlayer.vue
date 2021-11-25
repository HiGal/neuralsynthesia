<template>
  <div class="recorded-audio">
      <div class="audio-container"><audio v-bind:src="record" controls /></div>
  </div>
</template>

<script>
export default {
  props: {
    record: Object
  }
}
</script>

<style scoped>

</style>