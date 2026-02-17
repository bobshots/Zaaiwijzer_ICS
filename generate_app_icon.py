import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from PIL import Image

# --- CONFIGURATIE ---
PROJECT_ID = "gen-lang-client-0479848401" 
LOCATION = "us-central1"
OUTPUT_FOLDER = "icons" # Relative to script execution in pwa folder
ICON_NAME = "seedling" # Base name

# --- HET SCRIPT ---

def generate_icon():
    print("--- Starten met het genereren van app icoon ---")
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")
    
    prompt = """Generate a single, high-quality PNG image file with a transparent background based on the following description:

A very simple and clear icon of a generic seedling sprouting from soil, designed for maximum recognizability as an app icon. The art style must be 1950s retro-futuristic "Atompunk", like an illustration from a vintage manual, with a subtle paper grain texture. The design must be a single, bold silhouette with an extra bold black outline. Use a happy, cheerful expression if applicable, or just a very clear, bold sprout. High-contrast, blocky colors. Vibrant green sprout on dark soil."""

    try:
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            negative_prompt="text, words, letters, signature"
        )
        
        if not response.images:
            raise ValueError("Geen afbeelding gegenereerd.")

        image = response.images[0]
        filepath_512 = os.path.join(OUTPUT_FOLDER, "icon-512.png")
        image.save(location=filepath_512, include_generation_parameters=False)
        print(f"✅ SUCCESS: 'icon-512.png' opgeslagen")
        
        # Resize to 192x192
        img = Image.open(filepath_512)
        img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
        filepath_192 = os.path.join(OUTPUT_FOLDER, "icon-192.png")
        img_192.save(filepath_192)
        print(f"✅ SUCCESS: 'icon-192.png' opgeslagen")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    generate_icon()
