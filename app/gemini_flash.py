import json
import os
import time

from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Primary model + fallback models
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]


def generate_outline(
    prompt,
    character,
    setting,
    tone,
    art_style
):

    instruction = f"""
You are a professional comic book writer.

Create a comic story outline with EXACTLY 5 panels.

User information:

Story idea:
{prompt}

Main character:
{character}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Return ONLY valid JSON.

The JSON must have this structure:

{{
    "panels": [
        {{
            "panel_number": 1,
            "title": "Panel title",
            "scene_description": "What happens in this panel",
            "image_prompt": "Detailed prompt for generating the comic image"
        }}
    ]
}}

Rules:

- Exactly 5 panels.
- Keep the same main character throughout.
- Make the story have a beginning, middle and ending.
- Image prompts should describe the character, environment, action and art style.
- Do not use markdown.
"""

    last_error = None

    for model in MODELS:

        print(f"Trying Gemini model: {model}")

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=instruction
                )

                text = response.text.strip()

                # Remove markdown code fences if Gemini adds them
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

                data = json.loads(text)

                print(f"Successfully generated outline using {model}")

                return data["panels"]

            except errors.ServerError as e:

                last_error = e

                print(
                    f"{model} unavailable. "
                    f"Retry {attempt + 1}/3..."
                )

                time.sleep(2 ** attempt)

            except json.JSONDecodeError as e:

                print("Gemini returned invalid JSON.")
                print("Response was:")
                print(response.text)

                last_error = e
                break

            except Exception as e:

                print(f"Error with {model}: {e}")

                last_error = e
                break

    raise last_error