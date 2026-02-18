import requests
import numpy as np
from PIL import Image
import io
import sys

def test_api():
    base_url = "http://localhost:8000"
    
    print(f"Checking API at {base_url}...")
    
    # 1. Test Home
    print(f"\n[1/2] GET {base_url}/")
    try:
        resp = requests.get(f"{base_url}/")
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Success! Response: {resp.json()}")
        else:
            print(f"Failed. Response: {resp.text}")
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure the Docker container is running and port 8000 is mapped.")
        return

    # 2. Test Predict
    print(f"\n[2/2] POST {base_url}/predict")
    try:
        # Create a simple dummy image (blue square)
        img = Image.new('RGB', (32, 32), color = 'blue')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        files = {'file': ('test_image.png', buf, 'image/png')}
        resp = requests.post(f"{base_url}/predict", files=files)
        
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Success! Response: {resp.json()}")
        else:
            print(f"Failed. Response: {resp.text}")
            
    except Exception as e:
        print(f"Prediction request failed: {e}")

if __name__ == "__main__":
    try:
        test_api()
    except ImportError:
        print("Error: Required libraries (requests, numpy, pillow) not found.")
        print("Please install them using: pip install requests numpy pillow")
