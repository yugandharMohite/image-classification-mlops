"""
Export Model Metrics for Power BI Dashboard
This script exports training metrics, confusion matrix, and performance data
for visualization in Power BI.
"""

import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import mlflow

# Create output directory
os.makedirs('output', exist_ok=True)

# Class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

def load_cifar10_data():
    """Load CIFAR-10 test data"""
    def unpickle(file):
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict
    
    test_batch = unpickle('data/cifar-10-batches-py/test_batch')
    X_test = test_batch[b'data'].reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    y_test = np.array(test_batch[b'labels'])
    
    # Normalize
    X_test = X_test / 255.0
    
    return X_test, y_test

def export_mlflow_metrics():
    """Export MLflow experiment metrics"""
    try:
        experiment = mlflow.get_experiment_by_name("CIFAR10_Image_Classification_Lab")
        if experiment:
            runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
            runs.to_csv("output/mlflow_metrics.csv", index=False)
            print("[OK] Exported MLflow_metrics.csv")
        else:
            print("[WARNING] No MLflow experiment found")
    except Exception as e:
        print(f"[WARNING] Could not export MLflow metrics: {e}")

def export_confusion_matrix(y_true, y_pred):
    """Export confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    # Create DataFrame with class names
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    cm_df.to_csv("output/confusion_matrix.csv")
    
    # Also create long format for Power BI
    cm_long = []
    for i, true_class in enumerate(class_names):
        for j, pred_class in enumerate(class_names):
            cm_long.append({
                'True_Class': true_class,
                'Predicted_Class': pred_class,
                'Count': int(cm[i, j])
            })
    
    cm_long_df = pd.DataFrame(cm_long)
    cm_long_df.to_csv("output/confusion_matrix_long.csv", index=False)
    
    print("[OK] Exported confusion_matrix.csv")
    print("[OK] Exported confusion_matrix_long.csv")

def export_classification_report(y_true, y_pred):
    """Export classification report"""
    report = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv("output/classification_report.csv")
    
    print("[OK] Exported classification_report.csv")

def export_per_class_metrics(y_true, y_pred):
    """Export per-class accuracy and metrics"""
    metrics = []
    
    for i, class_name in enumerate(class_names):
        mask = y_true == i
        if mask.sum() > 0:
            accuracy = (y_pred[mask] == y_true[mask]).mean()
            total_samples = mask.sum()
            correct_predictions = (y_pred[mask] == y_true[mask]).sum()
            
            metrics.append({
                'Class': class_name,
                'Accuracy': accuracy,
                'Total_Samples': int(total_samples),
                'Correct_Predictions': int(correct_predictions),
                'Incorrect_Predictions': int(total_samples - correct_predictions)
            })
    
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv("output/per_class_metrics.csv", index=False)
    
    print("[OK] Exported per_class_metrics.csv")

def export_overall_metrics(y_true, y_pred):
    """Export overall model metrics"""
    accuracy = (y_pred == y_true).mean()
    
    metrics = {
        'Metric': ['Accuracy', 'Total_Samples', 'Correct_Predictions', 'Incorrect_Predictions'],
        'Value': [
            accuracy,
            len(y_true),
            (y_pred == y_true).sum(),
            (y_pred != y_true).sum()
        ]
    }
    
    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_csv("output/overall_metrics.csv", index=False)
    
    print("[OK] Exported overall_metrics.csv")

def main():
    """Main export function"""
    print("=" * 50)
    print("Exporting Model Metrics for Power BI")
    print("=" * 50)
    
    # Load model
    print("\n[*] Loading model...")
    try:
        model = tf.keras.models.load_model("model/image_classifier_clean.keras")
        print("[OK] Model loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return
    
    # Load test data
    print("\n[*] Loading test data...")
    try:
        X_test, y_test = load_cifar10_data()
        print(f"[OK] Loaded {len(X_test)} test samples")
    except Exception as e:
        print(f"[ERROR] Failed to load test data: {e}")
        return
    
    # Make predictions
    print("\n[*] Making predictions...")
    predictions = model.predict(X_test, verbose=0)
    y_pred = predictions.argmax(axis=1)
    print("[OK] Predictions complete")
    
    # Export metrics
    print("\n[*] Exporting metrics...")
    export_mlflow_metrics()
    export_confusion_matrix(y_test, y_pred)
    export_classification_report(y_test, y_pred)
    export_per_class_metrics(y_test, y_pred)
    export_overall_metrics(y_test, y_pred)
    
    print("\n" + "=" * 50)
    print("[SUCCESS] All metrics exported successfully!")
    print("=" * 50)
    print("\n[*] Files created in 'output/' directory:")
    print("   - mlflow_metrics.csv (if MLflow data available)")
    print("   - confusion_matrix.csv")
    print("   - confusion_matrix_long.csv (Power BI friendly)")
    print("   - classification_report.csv")
    print("   - per_class_metrics.csv")
    print("   - overall_metrics.csv")
    print("\n[TIP] Import these CSV files into Power BI for visualization")

if __name__ == "__main__":
    main()