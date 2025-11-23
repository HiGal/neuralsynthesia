import os
import requests
from typing import List, Tuple


class LLMStoryGenerator:
    """Modern LLM-based story generator using Nebius API."""

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initialize the LLM story generator.

        Args:
            api_key: Nebius API key (or set NEBIUS_API_KEY env var)
            base_url: Nebius API base URL (or set NEBIUS_BASE_URL env var)
        """
        self.api_key = api_key or os.environ.get('NEBIUS_API_KEY')
        self.base_url = base_url or os.environ.get('NEBIUS_BASE_URL', 'https://api.studio.nebius.ai/v1')

        if not self.api_key:
            raise ValueError("API key must be provided or set in NEBIUS_API_KEY environment variable")

    def generate_story(self, start_phrase: str, max_tokens: int = 500, temperature: float = 0.8) -> str:
        """
        Generate a story continuation based on the starting phrase.

        Args:
            start_phrase: The beginning of the story
            max_tokens: Maximum number of tokens to generate
            temperature: Creativity level (0.0-2.0, higher = more creative)

        Returns:
            Generated story text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Create a prompt that encourages creative storytelling
        system_prompt = """Ты креативный писатель детских историй. Твоя задача - создавать увлекательные, яркие и образные истории для детей.
Используй простой язык, интересные персонажи и захватывающий сюжет.
История должна быть подходящей для детей и содержать 4-6 сцен, которые можно проиллюстрировать."""

        payload = {
            "model": "meta-llama/Llama-3.3-70B-Instruct",  # Modern powerful model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Продолжи эту историю: {start_phrase}"}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            generated_text = result['choices'][0]['message']['content']

            # Combine the start phrase with the generated continuation
            full_story = f"{start_phrase} {generated_text}"
            return full_story.strip()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to generate story: {str(e)}")

    def split_into_scenes(self, story: str, sentences_per_scene: int = 2) -> List[str]:
        """
        Split the story into scenes for illustration.

        Args:
            story: The full story text
            sentences_per_scene: Number of sentences per scene

        Returns:
            List of scene descriptions
        """
        # Split by common sentence endings
        import re
        sentences = re.split(r'[.!?]+\s+', story)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Group sentences into scenes
        scenes = []
        for i in range(0, len(sentences), sentences_per_scene):
            scene = ' '.join(sentences[i:i + sentences_per_scene])
            if scene:
                scenes.append(scene)

        return scenes


def translate_text(text: str, target_lang: str = 'en') -> str:
    """
    Translate text to target language using a simple translation approach.
    For production, consider using a dedicated translation API.

    Args:
        text: Text to translate
        target_lang: Target language code

    Returns:
        Translated text
    """
    try:
        import translators as ts
        return ts.google(text, from_language='ru', to_language=target_lang)
    except Exception as e:
        # Fallback: return original text if translation fails
        print(f"Translation failed: {e}")
        return text


if __name__ == '__main__':
    # Test the story generator
    generator = LLMStoryGenerator()

    test_prompt = "Однажды в волшебном лесу"
    print(f"Generating story from: {test_prompt}")

    story = generator.generate_story(test_prompt)
    print(f"\nGenerated story:\n{story}")

    scenes = generator.split_into_scenes(story)
    print(f"\nSplit into {len(scenes)} scenes:")
    for i, scene in enumerate(scenes, 1):
        print(f"\nScene {i}: {scene}")
