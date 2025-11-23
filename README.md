# NeuralSynthesia 📖✨

**AI-Powered Interactive Storybook Generator**

NeuralSynthesia transforms voice input into beautiful illustrated storybooks using cutting-edge AI technology. Simply speak a story starter in Russian, and watch as modern language models weave it into a complete narrative, then bring it to life with stunning AI-generated illustrations.

## 🌟 Features

- **Voice-to-Story**: Speak your story idea and let AI expand it into a full narrative
- **Modern LLM**: Powered by Meta's Llama-3.3-70B model via Nebius AI
- **Beautiful Illustrations**: Each scene illustrated using Flux Schnell, the fastest high-quality image generation model
- **Illustrated Storybooks**: Creates beautiful HTML storybooks with images and text
- **Audio Narration**: Text-to-speech conversion for audio storytelling (via Yandex TTS)
- **Russian Language**: Optimized for Russian language input and output

## 🏗️ Architecture

### Modern Stack (Current)

```
Voice Input (Russian)
    ↓
Yandex Speech-to-Text API
    ↓
Llama-3.3-70B (via Nebius) → Story Generation
    ↓
Scene Extraction → Multiple scenes for illustration
    ↓
Translation (Russian → English)
    ↓
Flux Schnell (via Nebius) → Image Generation for each scene
    ↓
HTML Storybook Generator
    ↓
Illustrated Storybook (HTML + Images)
```

### Technology Components

1. **LLM Text Generation**:
   - Model: `meta-llama/Llama-3.3-70B-Instruct`
   - Provider: Nebius AI Platform
   - Purpose: Creative story writing from prompts

2. **Image Generation**:
   - Model: `black-forest-labs/FLUX.1-schnell`
   - Provider: Nebius AI Platform
   - Purpose: High-quality storybook illustrations (optimized for speed with 1-4 inference steps)

3. **Speech Processing**:
   - STT: Yandex SpeechKit (Speech-to-Text)
   - TTS: Yandex SpeechKit (Text-to-Speech)

4. **Web Framework**:
   - Backend: Flask (Python)
   - CORS enabled for frontend integration

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- ffmpeg (for audio processing)
- Nebius AI API key
- Yandex Cloud credentials (for STT/TTS)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HiGal/neuralsynthesia.git
   cd neuralsynthesia
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg

   # macOS
   brew install ffmpeg

   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```bash
   # Nebius AI API
   NEBIUS_API_KEY=your_nebius_api_key_here
   NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1

   # Yandex Cloud (for STT/TTS)
   OAUTH=your_yandex_oauth_token
   FOLDER_ID=your_yandex_folder_id
   ```

   **Getting API Keys:**
   - **Nebius**: Sign up at [Nebius AI Studio](https://studio.nebius.ai/)
   - **Yandex Cloud**: Create account at [Yandex Cloud](https://cloud.yandex.com/)

### Running the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📡 API Endpoints

### 1. Generate Story from Voice

**POST** `/get_audio`
- Upload voice recording (OPUS format)
- Returns: Redirects to `/generate_text` with transcribed text

### 2. Generate Story Text

**GET** `/generate_text?start_story=<text>`
- Generates complete story from starting phrase
- Returns: Story text, scenes array, and saves to results folder

Example response:
```json
{
  "result": "Full story text...",
  "start_story": "Однажды в волшебном лесу",
  "scenes": ["Scene 1 text", "Scene 2 text", ...],
  "num_scenes": 5
}
```

### 3. Generate Illustrated Storybook

**POST** `/generate_storybook`

Request body:
```json
{
  "scenes": ["Scene 1 text", "Scene 2 text", ...],
  "start_story": "story_title"
}
```

Returns:
```json
{
  "storybook_path": "story_title",
  "pages": [
    {
      "scene_number": 1,
      "text": "Scene text",
      "image_path": "results/story_title/page_01.png",
      "image_filename": "page_01.png"
    },
    ...
  ],
  "html_path": "story_title/storybook.html"
}
```

### 4. View Random Storybook

**GET** `/random`
- Returns a random storybook folder name

### 5. Get Storybook Files

**GET** `/static/<folder>.<format>`
- Access generated storybook files (images, HTML, audio, etc.)

## 📁 Project Structure

```
neuralsynthesia/
├── app.py                      # Main Flask application
├── src/
│   ├── llm_generator.py       # LLM story generation (Llama-3.3)
│   ├── image_generator.py     # Image generation (Flux Schnell)
│   ├── gpt3.py               # [Legacy] Old GPT-2 implementation
│   ├── vqgan_clip.py         # [Legacy] Old VQGAN+CLIP video generation
│   └── utils.py              # Utility functions
├── results/                   # Generated storybooks
│   └── <story_title>/
│       ├── story.txt         # Full story text
│       ├── scenes.json       # Scene breakdown
│       ├── story.ogg         # Audio narration
│       ├── page_01.png       # Scene illustrations
│       ├── page_02.png
│       ├── storybook.html    # Complete storybook
│       └── storybook.json    # Metadata
├── frontend/                  # Vue.js frontend (optional)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
└── README.md               # This file
```

## 🎨 Example Usage

### Using the API

```python
import requests

# 1. Generate story
response = requests.get(
    'http://localhost:5000/generate_text',
    params={'start_story': 'Однажды в волшебном лесу'}
)
story_data = response.json()

# 2. Generate illustrations
response = requests.post(
    'http://localhost:5000/generate_storybook',
    json={
        'scenes': story_data['scenes'],
        'start_story': story_data['start_story']
    }
)
storybook = response.json()

# 3. View the storybook
print(f"Storybook ready: http://localhost:5000/static/{storybook['html_path']}")
```

### Command Line Testing

Test individual components:

```bash
# Test LLM story generation
cd src
python llm_generator.py

# Test image generation
python image_generator.py
```

## 🔧 Configuration

### Story Generation Parameters

Edit `src/llm_generator.py`:
- `max_tokens`: Story length (default: 500)
- `temperature`: Creativity (0.0-2.0, default: 0.8)
- `sentences_per_scene`: Sentences per illustration (default: 2)

### Image Generation Parameters

Edit `src/image_generator.py`:
- `width`/`height`: Image dimensions (default: 1024x1024)
- `num_inference_steps`: Quality vs speed (1-4 for Schnell, default: 4)

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t neuralsynthesia .

# Run the container
docker run -p 5000:5000 \
  -e NEBIUS_API_KEY=your_key \
  -e OAUTH=your_yandex_oauth \
  -e FOLDER_ID=your_folder_id \
  neuralsynthesia
```

Or use docker-compose:

```bash
docker-compose up
```

## 🧪 Development

### Legacy Code

The original implementation used:
- **Text Generation**: rugpt3small (GPT-2 based Russian model)
- **Image Generation**: VQGAN+CLIP with MLP mixer
- **Output Format**: Video files (.webm)

These files are preserved in `src/` for reference:
- `src/gpt3.py` - Old GPT-2 implementation
- `src/vqgan_clip.py` - Old VQGAN+CLIP video generation

### Migration Notes

**Key Changes:**
1. Replaced local GPT-2 model with cloud-based Llama-3.3-70B
2. Replaced VQGAN+CLIP video generation with Flux Schnell image generation
3. Changed output from video to illustrated HTML storybooks
4. Removed heavy ML dependencies (PyTorch, CLIP, etc.)
5. Simplified to API-based architecture (no local model loading)

**Benefits:**
- 📉 Reduced dependencies from 100+ packages to <10
- 🚀 No GPU required on server (uses Nebius cloud GPUs)
- 💰 Pay-per-use pricing instead of infrastructure costs
- 📈 Better quality with latest models (Llama-3.3, Flux)
- 🎨 More flexible output format (HTML storybooks)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Nebius AI** - LLM and image generation infrastructure
- **Meta AI** - Llama-3.3-70B language model
- **Black Forest Labs** - Flux Schnell image generation model
- **Yandex Cloud** - Speech recognition and synthesis services

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `/docs`

## 🔮 Future Improvements

- [ ] Support for multiple languages
- [ ] Custom illustration styles
- [ ] Interactive storybook editor
- [ ] Export to PDF/ePub formats
- [ ] Voice cloning for personalized narration
- [ ] Character consistency across scenes
- [ ] Mobile app integration

---

**Made with ❤️ using AI**
