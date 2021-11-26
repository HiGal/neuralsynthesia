<template>
  <div id="app">
    <Background></Background>

    <HomePage></HomePage>

  </div>
</template>

<script>
import HomePage from "./components/HomePage";
import Background from "./components/Background";
import Loader from "./components/Loader";
import AudioPlayer from "./components/AudioPlayer";
import VideoPlayer from "./components/VideoPlayer";
import VueCoreVideoPlayer from 'vue-core-video-player'
import VueRecord from "@codekraft-studio/vue-record";
import Particles from "particles.vue"
import Vue from "vue";

Vue.use(VueRecord);
Vue.use(Particles);
Vue.use(VueCoreVideoPlayer)


export default {
  name: 'App',

  components: {
    HomePage,
    AudioPlayer,
    Background,
    Loader,
    VideoPlayer
  },

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
