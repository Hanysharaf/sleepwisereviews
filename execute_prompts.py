import os
import re
import time
import requests
import base64
from pathlib import Path
from dotenv import load_dotenv

# Set paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR
PROMPTS_FILE = PROJECT_DIR / "automation" / "data" / "ig_image_prompts.txt"
ENV_FILE = PROJECT_DIR / "automation" / ".env"

load_dotenv(ENV_FILE)

GEMINI_IMAGEN_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
API_KEY = os.getenv("GOOGLE_AI_API_KEY")

def generate_image(prompt):
    response = requests.post(
        GEMINI_IMAGEN_URL,
        params={"key": API_KEY},
        json={
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1, "aspectRatio": "1:1"},
        },
        timeout=60,
    )
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None
        
    predictions = response.json().get("predictions", [])
    if not predictions:
        print("Error: No predictions returned.")
        return None
        
    return base64.b64decode(predictions[0]["bytesBase64Encoded"])

def main():
    if not API_KEY:
        print("Error: GOOGLE_AI_API_KEY not found in .env")
        return

    if not PROMPTS_FILE.exists():
        print(f"Error: Prompts file not found at {PROMPTS_FILE}")
        return

    content = PROMPTS_FILE.read_text(encoding="utf-8")
    
    # Regex to find all blocks
    # Format:
    # IG-XXX | Type
    # SAVE PATH: path
    # PROMPT: text
    
    pattern = re.compile(
        r"(IG-\d+)\s*\|\s*.*?\nSAVE PATH:\s*(.*?)\nPROMPT:\s*(.*?)(?=\n\n|\n-|$)",
        re.DOTALL
    )
    
    matches = pattern.findall(content)
    print(f"Found {len(matches)} prompts to execute.")
    
    success_count = 0
    failure_count = 0
    
    for ig_id, save_path, prompt in matches:
        prompt = prompt.strip()
        save_path = save_path.strip()
        
        # Replace O:\MyFiles with the correct OneDrive path if needed
        save_path = save_path.replace(r"O:\MyFiles", r"C:\Users\Hany\OneDrive - Petroleum Air Services")
        
        out_path = Path(save_path)
        
        if out_path.exists():
            print(f"[{ig_id}] Skipping, image already exists: {out_path.name}")
            continue
            
        print(f"[{ig_id}] Generating image...")
        
        image_bytes = generate_image(prompt)
        if image_bytes:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(image_bytes)
            print(f"[{ig_id}] Saved to {out_path}")
            success_count += 1
        else:
            print(f"[{ig_id}] Failed to generate image.")
            failure_count += 1
            # If rate limit hit (429), we stop
            break
            
        # Add a sleep to prevent hitting limits too rapidly
        print("Waiting 5 seconds before next request...")
        time.sleep(5)
        
    print(f"\nExecution finished. Generated: {success_count}, Failed: {failure_count}")

if __name__ == "__main__":
    main()
