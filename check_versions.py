import tensorflow as tf
import keras
try:
    print(f"TF Version: {tf.__version__}")
except:
    pass
try:
    print(f"Keras Version: {keras.__version__}")
except:
    pass
try:
    print(f"TF Keras Version: {tf.keras.__version__}")
except:
    pass
