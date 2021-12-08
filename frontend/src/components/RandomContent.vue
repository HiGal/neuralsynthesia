<template>
  <div class="container">
    <b-row class="my-2 justify-content-left">
      <b-col lg="6">
        <div class="row ">
          <h5 class="text-white" v-if="text_loaded">
            <i>"{{ text }}"</i>
          </h5>
        </div>
      </b-col>
      <b-col lg="6">
        <video controls autoplay loop width="512">
          <source :src="video_path" type="video/webm">
        </video>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import VideoPlayer from "@/components/VideoPlayer";

export default {
  name: "RandomContent",
  components: {VideoPlayer},
  data() {
    return {
      text: "gdgagdsag",
      text_loaded: false
    }
  },
  props: {
    random_data: String
  },
  methods: {
    readTextFile() {

    }
  },
  created() {
    var requestOptions={
        headers: {
                    'Accept': 'application/json'
                  }
      }
    this.video_path = `http://localhost:5000/static/${this.random_data}.webm`
    this.text_path = `http://localhost:5000/static/${this.random_data}.txt`
    this.text_loaded = false
    fetch(this.text_path, requestOptions)
        .then(response => response.json())
        .then(data => {
          this.text_loaded = true
          this.text = data.text
        })
    // var request = new XMLHttpRequest();
    // request.open('GET', this.text_path, true);
    // request.send(null);
    // request.onreadystatechange = function () {
    //   if (request.readyState === 4 && request.status === 200) {
    //     var type = request.getResponseHeader('Content-Type');
    //     if (type.indexOf("text") !== 1) {
    //       this.text = request.responseText;
    //       this.text_loaded = true;
    //       console.log(this.text)
    //     }
    //   }
    // }

    this.$forceUpdate();
  }

}
</script>

<style scoped>

</style>