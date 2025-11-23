import os
import requests
import base64
from typing import List, Dict
from pathlib import Path
import time


class FluxImageGenerator:
    """Image generator using Flux Schnell model via Nebius API."""

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the Flux image generator.

        Args:
            api_key: Nebius API key (or set NEBIUS_API_KEY env var)
            base_url: Nebius API base URL (or set NEBIUS_BASE_URL env var)
        """
        self.api_key = api_key or os.environ.get('NEBIUS_API_KEY')
        self.base_url = base_url or os.environ.get('NEBIUS_BASE_URL', 'https://api.studio.nebius.ai/v1')

        if not self.api_key:
            raise ValueError("API key must be provided or set in NEBIUS_API_KEY environment variable")

    def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 4,
        seed: int = None
    ) -> bytes:
        """
        Generate an image from a text prompt using Flux Schnell.

        Args:
            prompt: Text description of the image
            width: Image width (default 1024)
            height: Image height (default 1024)
            num_inference_steps: Number of denoising steps (Schnell is optimized for 1-4 steps)
            seed: Random seed for reproducibility

        Returns:
            Image data as bytes
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Enhance the prompt for storybook-style illustrations
        enhanced_prompt = f"Children's storybook illustration, vibrant colors, friendly style: {prompt}"

        payload = {
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": enhanced_prompt,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps
        }

        if seed is not None:
            payload["seed"] = seed

        try:
            response = requests.post(
                f"{self.base_url}/images/generations",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()

            # Handle base64 encoded image
            if 'data' in result and len(result['data']) > 0:
                image_data = result['data'][0]

                # Check if it's base64 or URL
                if 'b64_json' in image_data:
                    return base64.b64decode(image_data['b64_json'])
                elif 'url' in image_data:
                    # Download from URL
                    img_response = requests.get(image_data['url'])
                    img_response.raise_for_status()
                    return img_response.content

            raise Exception("No image data in response")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate image: {str(e)}")

    def save_image(self, image_data: bytes, output_path: str):
        """
        Save image data to a file.

        Args:
            image_data: Image bytes
            output_path: Path to save the image
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as f:
            f.write(image_data)


class StorybookGenerator:
    """Generate illustrated storybook pages from a story."""

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the storybook generator.

        Args:
            api_key: Nebius API key
            base_url: Nebius API base URL
        """
        self.image_generator = FluxImageGenerator(api_key, base_url)

    def create_storybook(
        self,
        scenes: List[str],
        output_dir: str,
        story_title: str,
        translate_to_english: bool = True
    ) -> List[Dict[str, str]]:
        """
        Create an illustrated storybook from scenes.

        Args:
            scenes: List of scene descriptions
            output_dir: Directory to save images
            story_title: Title of the story (used for filenames)
            translate_to_english: Whether to translate prompts to English for better results

        Returns:
            List of dictionaries with scene text and image path
        """
        from .llm_generator import translate_text

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        storybook_pages = []

        for i, scene in enumerate(scenes):
            print(f"Generating illustration {i+1}/{len(scenes)}...")

            # Translate to English for better image generation if needed
            prompt = scene
            if translate_to_english:
                try:
                    prompt = translate_text(scene, 'en')
                except Exception as e:
                    print(f"Translation failed, using original: {e}")
                    prompt = scene

            # Generate image
            try:
                image_data = self.image_generator.generate_image(
                    prompt=prompt,
                    width=1024,
                    height=1024,
                    num_inference_steps=4
                )

                # Save image
                image_filename = f"page_{i+1:02d}.png"
                image_path = os.path.join(output_dir, image_filename)
                self.image_generator.save_image(image_data, image_path)

                storybook_pages.append({
                    'scene_number': i + 1,
                    'text': scene,
                    'image_path': image_path,
                    'image_filename': image_filename
                })

                # Small delay to avoid rate limiting
                time.sleep(0.5)

            except Exception as e:
                print(f"Failed to generate image for scene {i+1}: {e}")
                # Continue with other scenes even if one fails
                storybook_pages.append({
                    'scene_number': i + 1,
                    'text': scene,
                    'image_path': None,
                    'image_filename': None,
                    'error': str(e)
                })

        return storybook_pages

    def create_html_storybook(
        self,
        storybook_pages: List[Dict[str, str]],
        story_title: str,
        output_path: str
    ):
        """
        Create an HTML file displaying the storybook.

        Args:
            storybook_pages: List of page dictionaries
            story_title: Title of the story
            output_path: Path to save HTML file
        """
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{story_title}</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5dc;
        }}
        h1 {{
            text-align: center;
            color: #333;
            font-size: 2.5em;
            margin-bottom: 40px;
        }}
        .page {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .page-number {{
            color: #888;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .page img {{
            width: 100%;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .page-text {{
            font-size: 1.2em;
            line-height: 1.8;
            color: #333;
            text-align: justify;
        }}
        .error {{
            color: #d9534f;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <h1>{story_title}</h1>
"""

        for page in storybook_pages:
            html_content += f"""
    <div class="page">
        <div class="page-number">Страница {page['scene_number']}</div>
"""
            if page.get('image_filename'):
                html_content += f"""        <img src="{page['image_filename']}" alt="Иллюстрация {page['scene_number']}">
"""
            elif page.get('error'):
                html_content += f"""        <p class="error">Не удалось создать иллюстрацию: {page['error']}</p>
"""

            html_content += f"""        <div class="page-text">{page['text']}</div>
    </div>
"""

        html_content += """
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)


if __name__ == '__main__':
    # Test the image generator
    generator = FluxImageGenerator()

    test_prompt = "A magical forest with friendly animals and colorful flowers"
    print(f"Generating image from: {test_prompt}")

    image_data = generator.generate_image(test_prompt)
    generator.save_image(image_data, "test_output.png")
    print("Image saved to test_output.png")
