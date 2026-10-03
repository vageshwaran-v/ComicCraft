import os
import torch

from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline

load_dotenv()

# Stable Diffusion model
MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

# Use GPU if available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading Stable Diffusion...")
print("Device:", DEVICE)

# Load the Stable Diffusion pipeline
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
)

pipe = pipe.to(DEVICE)

# Memory optimization for smaller GPUs
if DEVICE == "cuda":
    pipe.enable_attention_slicing()

print("Stable Diffusion loaded successfully!")


def generate_image(image_prompt, panel_number):

    os.makedirs("static/panels", exist_ok=True)

    filename = f"panel_{panel_number}.png"

    filepath = os.path.join(
        "static",
        "panels",
        filename
    )

    full_prompt = f"""
Comic book illustration.

{image_prompt}

High quality comic book art,
consistent character appearance,
clear facial expression,
dynamic composition,
detailed environment,
cinematic lighting,
colorful illustration,
professional comic style.
"""

    print(f"Generating image for panel {panel_number}...")

    image = pipe(
        prompt=full_prompt,
        width=512,
        height=512,
        num_inference_steps=25,
        guidance_scale=7.5
    ).images[0]

    image.save(filepath)

    print(f"Panel {panel_number} saved: {filepath}")

    return f"/static/panels/{filename}"