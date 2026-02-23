#!/usr/bin/env python3
"""BlackRoad Computer Vision Platform — image analysis pipeline."""
import os, json, base64, urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def analyze_image_b64(b64_image: str, model: str = "llava", prompt: str = "Describe this image.") -> str:
    """Analyze an image using a multimodal Ollama model."""
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "images": [b64_image],
        "stream": False
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read()).get("response", "")

def analyze_file(path: str, prompt: str = "Describe this image.") -> str:
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return analyze_image_b64(b64, prompt=prompt)

def classify_world_screenshot(path: str) -> dict:
    """Specialized: classify a world artifact screenshot."""
    result = analyze_file(path, prompt=(
        "What type of world is this? Answer with one of: "
        "cyberpunk, solarpunk, quantum, ancient, neural, void, crystal. "
        "Then describe what you see in one sentence."
    ))
    lines = result.strip().split("\\n")
    world_type = lines[0].strip().lower() if lines else "unknown"
    description = lines[1].strip() if len(lines) > 1 else result
    return {"type": world_type, "description": description}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(json.dumps(classify_world_screenshot(sys.argv[1]), indent=2))
    else:
        print("Usage: python3 vision_pipeline.py <image_path>")

