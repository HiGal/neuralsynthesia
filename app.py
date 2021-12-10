import sys
from flask import Flask, redirect, request, url_for, jsonify, send_from_directory
import requests
from flask_cors import CORS
import os
import random

sys.path.append("feed_forward_vqgan_clip")
from src.vqgan_clip import load_gpt_model, load_vqgan_model, load_perceptor, generate_sentence
from src.vqgan_clip import generate_video as _generate_video

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {'origins': '*'}})


@app.route("/")
def home():
    return redirect("/random")


@app.route("/random")
def random_video():
    video = random.choice(os.listdir("results/"))
    return video


@app.route("/get_audio", methods=["POST"])
def get_audio():
    os.environ['IAM_TOKEN'] = requests.post("https://iam.api.cloud.yandex.net/iam/v1/tokens",
                                            json={
                                                "yandexPassportOauthToken": os.environ.get('OAUTH')
                                            }).json()['iamToken']
    print(os.environ.get('IAM_TOKEN'))
    print(os.environ.get('FOLDER_ID'))
    data = request.data
    with open("voice.opus", "wb") as f:
        f.write(data)

    os.system("ffmpeg -i voice.opus -f wav - | oggenc -o voice.ogg -")

    with open("voice.ogg", "rb") as f:
        data = f.read()
    responseData = requests.post("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize",
                                 params={
                                     "topic": "general",
                                     "folderId": os.environ.get('FOLDER_ID'),
                                     "lang": "ru-RU",
                                     "profanityFilter": True
                                 },
                                 headers={
                                     "Authorization": f"Bearer {os.environ.get('IAM_TOKEN')}",
                                     "Content-Type": "audio/ogg"
                                 }, data=data)

    decodedData = responseData.json()
    return redirect(url_for("generate_text", start_story=decodedData["result"]))


@app.route("/generate_text")
def generate_text():
    start_story = request.args["start_story"]
    sentences, generated_sentence = generate_sentence(start_story, gpt3, tokenizer, n_grams=6)
    os.makedirs(f"results/{start_story}", exist_ok=True)
    with open(f"results/{start_story}/{start_story}.txt", "w") as f:
        f.write(generated_sentence)
    generated_speech = requests.post("https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize",
                                     params={
                                         "text": generated_sentence,
                                         "folderId": os.environ.get('FOLDER_ID'),
                                         "lang": "ru-RU",
                                         "voice": "ermil",
                                         "emotion": "neutral"
                                     },
                                     headers={
                                         "Authorization": f"Bearer {os.environ.get('IAM_TOKEN')}",
                                     })
    with open(f"results/{start_story}/{start_story}.ogg", "wb") as f:
        f.write(generated_speech.content)
    return jsonify({"result": generated_sentence, "start_story": f"{start_story}", "sentences": sentences})


@app.route("/generate_video", methods=["POST"])
def generate_video():
    data = request.json
    sentences = data['sentences']
    start_story = data['start_story']
    _generate_video(sentences, f"results/{start_story}/{start_story}.webm", vqgan_model, mlp_mixer, perceptor)
    return jsonify({"video_path": f"{start_story}"})


@app.route("/static/get_random")
def return_random_text():
    folders = os.listdir("results")
    print({"folder": random.choice(folders)})
    return jsonify({"folder": random.choice(folders)})


@app.route("/static/<file>")
def return_static(file):
    folder, format = file.split(".")
    if format == "txt":
        with open(f"results/{folder}/{file}", "r") as f:
            return jsonify({"text": f.read()})
    return send_from_directory("results", f"{folder}/{file}")


if __name__ == '__main__':
    tokenizer, gpt3 = load_gpt_model("rugpt3small_based_on_gpt2")
    vqgan_model, mlp_mixer, _ = load_vqgan_model("feed_forward_vqgan_clip/cc12m_32x1024_mlp_mixer.th")
    perceptor = load_perceptor()
    app.run(load_dotenv=True, host="0.0.0.0")
