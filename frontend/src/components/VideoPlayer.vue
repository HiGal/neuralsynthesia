<template>
  <div>
    <video controls loop width="512">
      <source :src=video_path type="video/webm">
    </video>
  </div>
</template>

<script>
export default {
  props: {
    video_path: {
      type: String
    }
  },
  created() {
    console.log(this.video_path)
    this.video_path = "http://localhost:5000/static/" + this.video_path
  }
}
</script>

<style scoped>

</style>