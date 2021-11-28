<template>
  <div class="header">
    <h1>Нейросказки</h1>
    <VueRecordAudio @result="onResult"/>
    <h2 v-if="loading_text">
      Генерация текста
      <div>
        <Loader/>
      </div>
    </h2>
    <h1 v-else-if="is_text_generated">
      {{ text }}
      <AudioPlayer :record="start_story"></AudioPlayer>
    </h1>
    <h2 v-if="loading_video">
      Генерация видео
      <div>
        <Loader/>
      </div>
    </h2>
    <VideoPlayer v-else-if="is_video_generated" :video_path="video_path"/>


  </div>
</template>

<script>
import Loader from "./Loader";
import VideoPlayer from "./VideoPlayer";
import AudioPlayer from "@/components/AudioPlayer";

export default {
  name: "HomePage",
  data() {
    return {
      record: {},
      text: "",
      video_path: "",
      start_story: "",
      sentences: [],
      loading_text: false,
      loading_video: false,
      is_text_generated: false,
      is_video_generated: false
    }
  },
  components: {
    AudioPlayer,
    Loader,
    VideoPlayer
  },
  methods: {
    onResult(data) {
      this.loading_text = true
      this.is_video_generated = false
      this.is_text_generated = false
      var requestOptions = {
        method: "POST",
        body: data
      };
      console.log(requestOptions);
      fetch("http://localhost:5000/get_audio", requestOptions)
          .then(response => response.json())
          .then(data => {
            this.text = data.result
            this.start_story = data.start_story
            this.sentences = data.sentences
            this.loading_text = false
            this.loading_video = true
            this.is_text_generated = true
          })
          .then(() => {
                var requestOptions = {
                  method: "POST",
                  headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                  },
                  body: JSON.stringify({
                    "sentences": this.sentences,
                    "start_story": this.start_story
                  })
                }
                console.log(requestOptions)
                fetch("http://localhost:5000/generate_video", requestOptions)
                    .then(response => response.json())
                    .then(data => {
                      this.video_path = data.video_path
                      this.is_video_generated = true
                      this.loading_video = false
                    })
              }
          )
    }
  }
}
</script>

<style>
.header {
  color: whitesmoke;
}
</style>