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

# Use the model that successfully generated the outline.
MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash"
]


def generate_story(
    prompt,
    character,
    setting,
    tone,
    panels
):

    panel_information = json.dumps(
        panels,
        indent=2
    )

    instruction = f"""
You are writing a professional 5-panel comic.

Original story idea:
{prompt}

Main character:
{character}

Setting:
{setting}

Tone:
{tone}

Panel outline:
{panel_information}

Create narration and dialogue for each panel.

Return ONLY valid JSON in this format:

{{
    "panels": [
        {{
            "panel_number": 1,
            "caption": "Short caption",
            "narration": "Narration for the panel",
            "dialogue": "Character dialogue"
        }}
    ]
}}

Rules:

- Exactly 5 panels.
- Match the provided panel outline.
- Keep the story coherent.
- Keep dialogue short enough for a comic.
- Use the requested tone.
- Do not use markdown.
"""

    last_error = None

    for model in MODELS:

        print(f"Trying story generation with Gemini model: {model}")

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=instruction
                )

                text = response.text.strip()

                # Remove markdown code fences
                text = text.replace("```json", "")
                text = text.replace("```", "")
                text = text.strip()

                data = json.loads(text)

                print(
                    f"Successfully generated story using {model}"
                )

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