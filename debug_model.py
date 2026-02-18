import tensorflow as tf
import os
import sys

print(f"Python Version: {sys.version}")
print(f"TensorFlow Version: {tf.__version__}")

model_path = "model/image_classifier.h5"

if os.path.exists(model_path):
    print(f"Found model file at: {os.path.abspath(model_path)}")
    try:
        # Attempt to load the model
        model = tf.keras.models.load_model(model_path)
        print("Success: Model loaded!")
        
        # Print input shape to confirm
        print(f"Model Input Shape: {model.input_shape}")
    except Exception as e:
        print("FAILURE: Could not load model.")
        print(f"Error details: {e}")
else:
    print(f"FAILURE: Model file not found at {model_path}")
