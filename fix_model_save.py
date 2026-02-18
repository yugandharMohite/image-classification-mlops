import tensorflow as tf
import os

try:
    print("Loading model from model/image_classifier.h5...")
    model = tf.keras.models.load_model("model/image_classifier.h5")
    print("Model loaded successfully.")
    
    # Save as Keras v3 format
    keras_path = "model/image_classifier_clean.keras"
    model.save(keras_path)
    print(f"Saved model to {keras_path}")
    
    # Save as H5 format (legacy) - forcing a pure save might fix config dicts
    h5_path = "model/image_classifier_clean.h5"
    model.save(h5_path)
    print(f"Saved model to {h5_path}")
    
except Exception as e:
    print(f"Error: {e}")
