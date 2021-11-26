<template>
  <div class="header">

    <h1>Нейросказки</h1>
    <VueRecordAudio @result="onResult"/>
    <Loader v-if="loading"/>
    <h1 v-if="text">
      {{ text }}
      <VideoPlayer v-bind:video_path="video_path"/>
    </h1>

  </div>
</template>

<script>
import Loader from "./Loader";
import VideoPlayer from "./VideoPlayer";

export default {
  name: "HomePage",
  data() {
    return {
      record: {},
      text: "",
      video_path: "",
      loading: false
    }
  },
  components: {
    Loader,
    VideoPlayer
  },
  methods: {
    onResult(data) {
      this.loading=true
      var requestOptions = {
        method: "POST",
        body: data
      };
      console.log(requestOptions);
      fetch("http://localhost:5000/get_audio", requestOptions)
          .then(a => a.json())
          .then(data => {
            this.text = data.result
            this.video_path = data.video_path
            this.loading = false
          });
      this.record = window.URL.createObjectURL(data)
    }
  }
}
</script>

<style>
.header {
  color: whitesmoke;
}
</style>