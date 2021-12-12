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
              <p class="text-left "><i>{{ text }} ...</i></p>
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
    <div class="container" v-if="!loading_video && !loading_text">
      <div class="d-flex justify-content-center">
        <h2 class="text-white" v-if="!is_exception">Начните рассказ</h2>
        <h2 class="text-white" v-else>Речь не распознана. Повторите еще раз</h2>
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
var vad = require("../scripts/vad")
var audioContext;
var blob;

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
      is_listen: null,
      listen_functions: null,
      is_exception: false
    }
  },
  components: {
    Jumbotron,
    AudioPlayer,
    Loader,
    VideoPlayer
  },
  methods: {
    requestMic() {
      try {
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        audioContext = new AudioContext();
        audioContext.resume()
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
        navigator.getUserMedia({audio: true}, this.startUserMedia, this.handleMicConnectError);
      } catch (e) {
        this.handleUserMediaError();
      }
    },
    handleUserMediaError() {
      console.warn('Mic input is not supported by the browser.');
    },
    handleMicConnectError() {
      console.warn('Could not connect microphone. Possible rejected by the user or is blocked by the browser.');
    },
    startUserMedia(stream) {
      audioContext.resume()
      var options = {
        fftSize: 2048,
        bufferLen: 1024,
        smoothingTimeConstant: 0.6,
        minCaptureFreq: 100,         // in Hz
        maxCaptureFreq: 255,        // in Hz
        noiseCaptureDuration: 2000, // in ms
        minNoiseLevel: 0.6,         // from 0 to 1
        maxNoiseLevel: 1.0,         // from 0 to 1
        avgNoiseMultiplier: 1.2
      };
      this.listen_functions = vad(audioContext, stream, options, this.onResult)
    },
    onResult(data) {
      this.is_video_generated = false
      this.is_text_generated = false
      var requestOptions = {
        method: "POST",
        body: data
      };
      console.log(requestOptions);
      if (this.loading_text === false && this.loading_video === false) {
        this.is_exception = false
        this.loading_text = true
        fetch("http://localhost:5000/get_audio", requestOptions)
            .then(response => response.json())
            .then(data => {
              if (data.result === "Error") {
                this.is_exception = true
                this.loading_text = false
                this.start_story = null
              } else {
                this.listen_functions.disconnect()
                this.text = data.result
                this.start_story = data.start_story
                this.sentences = data.sentences
                this.loading_text = false
                this.loading_video = true
                this.is_text_generated = true
              }
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
                        if (data.video_path === "Error") {
                          this.is_exception = true
                        } else {
                          this.is_exception = false
                          this.video_path = data.video_path

                          this.is_video_generated = true
                          this.loading_video = false
                          this.listen_functions.connect()
                        }
                      })
                }
            )
      }
    },

  }
  ,
  created() {
    this.is_listen = true
    this.requestMic();
  }

}
</script>

<style scoped>

</style>