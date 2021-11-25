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
        body: data
      };
      console.log(requestOptions);
      fetch("http://localhost:5000/get_audio", requestOptions)
          .then(a=>a.json())
          .then(data => {this.text = data.result});
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
