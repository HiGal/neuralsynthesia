from flask import Flask, redirect, request, url_for, jsonify, send_from_directory
import requests
from flask_cors import CORS
import os
import random
import json
from pathlib import Path

from src.llm_generator import LLMStoryGenerator
from src.image_generator import StorybookGenerator

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r"/*": {'origins': '*'}})


@app.route("/")
def home():
    return redirect("/random")


@app.route("/random")
def random_storybook():
    """Get a random storybook."""
    storybooks = [d for d in os.listdir("results/") if os.path.isdir(f"results/{d}")]
    if not storybooks:
        return jsonify({"error": "No storybooks available"}), 404
    return jsonify({"folder": random.choice(storybooks)})


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
    """Generate a story from the starting phrase."""
    start_story = request.args["start_story"]

    try:
        # Generate story using modern LLM
        story = story_generator.generate_story(start_story, max_tokens=500)

        # Split into scenes for illustration
        scenes = story_generator.split_into_scenes(story, sentences_per_scene=2)

        # Create output directory
        story_dir = f"results/{start_story}"
        os.makedirs(story_dir, exist_ok=True)

        # Save the full story
        with open(f"{story_dir}/story.txt", "w", encoding="utf-8") as f:
            f.write(story)

        # Save scenes as JSON
        with open(f"{story_dir}/scenes.json", "w", encoding="utf-8") as f:
            json.dump(scenes, f, ensure_ascii=False, indent=2)

        # Generate speech (keep existing Yandex TTS)
        try:
            generated_speech = requests.post(
                "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize",
                params={
                    "text": story,
                    "folderId": os.environ.get('FOLDER_ID'),
                    "lang": "ru-RU",
                    "voice": "ermil",
                    "emotion": "neutral"
                },
                headers={
                    "Authorization": f"Bearer {os.environ.get('IAM_TOKEN')}",
                }
            )
            with open(f"{story_dir}/story.ogg", "wb") as f:
                f.write(generated_speech.content)
        except Exception as e:
            print(f"Speech synthesis failed: {e}")

        return jsonify({
            "result": story,
            "start_story": start_story,
            "scenes": scenes,
            "num_scenes": len(scenes)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate_storybook", methods=["POST"])
def generate_storybook():
    """Generate illustrated storybook pages."""
    data = request.json
    scenes = data.get('scenes', [])
    start_story = data.get('start_story', 'untitled')

    if not scenes:
        return jsonify({"error": "No scenes provided"}), 400

    try:
        story_dir = f"results/{start_story}"

        # Generate illustrations for each scene
        storybook_pages = storybook_generator.create_storybook(
            scenes=scenes,
            output_dir=story_dir,
            story_title=start_story,
            translate_to_english=True
        )

        # Create HTML storybook
        html_path = f"{story_dir}/storybook.html"
        storybook_generator.create_html_storybook(
            storybook_pages=storybook_pages,
            story_title=start_story,
            output_path=html_path
        )

        # Save storybook metadata
        with open(f"{story_dir}/storybook.json", "w", encoding="utf-8") as f:
            json.dump(storybook_pages, f, ensure_ascii=False, indent=2)

        return jsonify({
            "storybook_path": start_story,
            "pages": storybook_pages,
            "html_path": f"{start_story}/storybook.html"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    # Initialize generators
    story_generator = LLMStoryGenerator()
    storybook_generator = StorybookGenerator()

    # Create results directory if it doesn't exist
    Path("results").mkdir(exist_ok=True)

    print("Starting NeuralSynthesia server...")
    print("Story Generator: LLama-3.3-70B via Nebius")
    print("Image Generator: Flux Schnell via Nebius")

    app.run(host="0.0.0.0", port=5000, debug=True)
