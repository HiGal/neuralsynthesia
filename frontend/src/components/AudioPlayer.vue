<template>
  <div class="recorded-audio">
    <div class="audio-container" style="display: none">
      <audio v-bind:src="record" autoplay/>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    record: String
  },
  created() {
    this.record = "http://localhost:5000/static/" + this.record + ".ogg"
    this.$forceUpdate()
  }
}
</script>

<style scoped>

</style>