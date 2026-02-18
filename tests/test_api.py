import pytest
import requests
import json
from PIL import Image
import io
import numpy as np

# Test configuration
API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test if API is running"""
    response = requests.get(f"{API_BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["model_status"] == "Model loaded"

def test_predict_endpoint():
    """Test prediction endpoint with a sample image"""
    # Create a simple test image (32x32 RGB)
    img = Image.new('RGB', (32, 32), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    files = {'file': ('test.png', img_byte_arr, 'image/png')}
    response = requests.post(f"{API_BASE_URL}/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "class" in data
    assert "confidence" in data
    assert data["class"] in ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                              'dog', 'frog', 'horse', 'ship', 'truck']
    assert 0 <= data["confidence"] <= 1

def test_predict_invalid_file():
    """Test prediction with invalid file"""
    files = {'file': ('test.txt', io.BytesIO(b'not an image'), 'text/plain')}
    response = requests.post(f"{API_BASE_URL}/predict", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "error" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
