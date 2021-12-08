<template>
 <div class="d-flex justify-content-center">
    <video controls autoplay loop width="512">
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
    console.log("sfaojggsgasjg",this.video_path)
    this.video_path = "http://localhost:5000/static/" + this.video_path + ".webm"
    this.$forceUpdate()
  }
}
</script>

<style scoped>

</style>