<template>
  <div>
    <div class="header" height="100%">
      <Jumbotron/>
    </div>
    <div class="container">
      <b-row class="my-2">
        <b-col lg="6">

          <div class="row justify-content-center">
            <h4 class="text-white" v-if="loading_text">
              Генерация текста
              <div class="d-flex justify-content-center">
                <Loader/>
              </div>
            </h4>
            <h5 class="text-white" v-else-if="is_text_generated">
              <i>{{ text }}</i>
              <p class="text-right my-3"><i>—— Нейрописатель Неизвестный, 2021</i></p>
              <AudioPlayer :record="start_story"></AudioPlayer>
            </h5>

          </div>


        </b-col>

        <b-col lg="6">
          <div class="row justify-content-center">
            <h4 class="text-white" v-if="loading_video">
              Генерация видео
              <div class="d-flex justify-content-center">
                <Loader/>
              </div>
            </h4>
            <VideoPlayer v-else-if="is_video_generated" :video_path="video_path"/>
          </div>
        </b-col>

      </b-row>

    </div>
    <div class="container">
      <div class="d-flex justify-content-center">
        <h2 class="text-white">Удерживайте для записи</h2>
      </div>
      <div class="d-flex justify-content-center">
        <VueRecordAudio @result="onResult"/>
      </div>
    </div>
  </div>
</template>

<script>
import Loader from "./Loader";
import VideoPlayer from "./VideoPlayer";
import AudioPlayer from "@/components/AudioPlayer";
import Jumbotron from "@/components/Jumbotron";
// import RandomContent from "@/components/RandomContent";

export default {
  name: "HomePage",
  data() {
    return {
      random_data: "",
      random_data_loaded: false,
      record: {},
      text: "",
      video_path: "",
      start_story: "",
      sentences: [],
      loading_text: false,
      loading_video: false,
      is_text_generated: false,
      is_video_generated: false,

    }
  },
  components: {
    Jumbotron,
    AudioPlayer,
    Loader,
    VideoPlayer
  },
  methods: {
    onResult(data) {
      this.loading_text = true
      this.is_video_generated = false
      this.is_text_generated = false
      SharedStore.data.audioEnded = false
      this.audioEnded = false
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
    },

  },
  created() {
    // this.random_data_loaded = false
    // var requestOptions = {
    //   headers: {
    //     'Accept': 'application/json'
    //   }
    // }
    // fetch("http://localhost:5000/static/get_random", requestOptions)
    //     .then(response => response.json())
    //     .then(data => {
    //
    //       this.random_data = data.folder;
    //       this.random_data_loaded = true;
    //       console.log(this.random_data)
    //     })
  }

}
</script>

<style scoped>

</style>