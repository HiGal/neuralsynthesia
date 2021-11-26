<template>
  <div>
    <video controls loop width="50%">
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
  name: "VideoPlayer"
}
</script>

<style scoped>

</style>