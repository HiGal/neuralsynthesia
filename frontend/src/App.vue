<template>
  <div id="app">
    <HomePage></HomePage>
    <VueRecordAudio @result="onResult"/>
    <div class="audio-player" v-if="record">
      <AudioPlayer v-if="record" v-bind:record="record"></AudioPlayer>
    </div>
    <h1>{{ text }}</h1>
  </div>
</template>

<script>
import HomePage from "./components/HomePage";
import AudioPlayer from "./components/AudioPlayer";
import VueRecord from "@codekraft-studio/vue-record";
import Vue from "vue";

Vue.use(VueRecord)

export default {
  name: 'App',
  data() {
    return {
      record: {},
      text: ""
    }
  },
  components: {
    HomePage,
    AudioPlayer
  },
  methods: {
    onResult(data) {

      var requestOptions = {
        method: "POST",
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Authorization": `Bearer ${process.env.VUE_APP_IAM_TOKEN}`
        },
        mode: "cors",
        body: data
      };
      console.log(requestOptions);
      fetch("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?topic=general&lang=ru-RU&profanityFilter=true&folderId=b1gn0q0hhm383i8vomic",
          requestOptions).then(
          response => response.json()
      ).then(
          json => {
            this.text = json.result
          }
      );
      this.record = window.URL.createObjectURL(data)
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  background-color: black;
}
</style>
