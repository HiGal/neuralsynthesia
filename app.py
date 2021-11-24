import sys
from flask import Flask, redirect, request
import os
import random

sys.path.append("feed_forward_vqgan_clip")
from src.vqgan_clip import load_gpt_model, load_vqgan_model, load_perceptor, generate_sentence, generate_video

app = Flask(__name__)


@app.route("/")
def home():
    return redirect("/random")


@app.route("/random")
def random_video():
    video = random.choice(os.listdir("results/"))
    return video


@app.route("/generate/<start_story>")
def generate(start_story):
    sentences, generated_sentence = generate_sentence(start_story, gpt3, tokenizer, n_grams=6)
    os.makedirs(f"results/{start_story}", exist_ok=True)
    with open(f"results/{start_story}/{start_story}.txt", "w") as f:
        f.write(generated_sentence)
    generate_video(sentences, f"results/{start_story}/{start_story}.mp4", vqgan_model, mlp_mixer, perceptor)
    return generated_sentence


if __name__ == '__main__':
    tokenizer, gpt3 = load_gpt_model("rugpt3small_based_on_gpt2")
    vqgan_model, mlp_mixer, _ = load_vqgan_model("feed_forward_vqgan_clip/cc12m_32x1024_mlp_mixer.th")
    perceptor = load_perceptor()
    app.run()
