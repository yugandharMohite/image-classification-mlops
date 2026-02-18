from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import sys

app = FastAPI()

# Enable CORS for robust access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load model
model = None
try:
    print("Attempting to load model from model/image_classifier_clean.keras...")
    model = tf.keras.models.load_model("model/image_classifier_clean.keras")
    print("Model loaded successfully.")
    # Print summary to verify
    model.summary()
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model: {e}")
    # Don't exit, let the app run so we can debug via API
    pass

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

@app.get("/")
def home():
    status = "Model loaded" if model else "Model NOT loaded"
    return {"message": "Image Classification API is running", "model_status": status}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model is not loaded. Check server logs."}
        
    try:
        # Read image
        contents = await file.read()
        try:
            img = Image.open(io.BytesIO(contents))
        except Exception as e:
             return {"error": f"Invalid image file: {e}"}

        # Preprocess
        img = img.resize((32, 32))
        img = np.array(img) / 255.0  # Normalize
        img = img.reshape(1, 32, 32, 3)
        
        # Predict
        pred = model.predict(img)
        class_idx = int(pred.argmax())
        confidence = float(pred.max())
        
        return {
            "class": class_names[class_idx],
            "confidence": confidence
        }
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
