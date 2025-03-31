import pandas as pd
import numpy as np
import joblib
from fairlearn.metrics import MetricFrame, demographic_parity_difference, equalized_odds_difference
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Load saved model
ensemble_model = joblib.load('ensemble_model_downsampled.pkl')

# Load dataset (Ensure it includes Gender and Race for fairness audit)
df = pd.read_csv('Full_Dataset.csv')

# Load precomputed test embeddings
X_test_embeddings = np.load('X_test_embeddings.npy')  # Ensure embeddings are saved separately
y_test = pd.read_csv('y_test.csv')  # Load corresponding test labels

# Get model predictions
y_pred = ensemble_model.predict(X_test_embeddings)

# Fairness Audit for Gender and Race
sensitive_attrs = ['Gender', 'Race']

for attr in sensitive_attrs:
    if attr in df.columns:
        print(f"\n🔎 Fairness Audit for {attr}:")
        for group in df[attr].unique():
            group_idx = df[df[attr] == group].index
            
            if len(group_idx) > 0:
                y_true = y_test.iloc[group_idx]
                y_pred_group = y_pred[group_idx]
                
                tn, fp, fn, tp = confusion_matrix(y_true, y_pred_group).ravel()
                
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # Handle division by zero
                fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
                
                print(f"{attr} = {group}:")
                print(f"  - Accuracy: {accuracy_score(y_true, y_pred_group):.4f}")
                print(f"  - False Positive Rate (FPR): {fpr:.4f}")
                print(f"  - False Negative Rate (FNR): {fnr:.4f}")

# Disparate Impact Ratio Calculation
def disparate_impact(y_pred, sensitive_attr):
    """Calculate Disparate Impact Ratio (DIR) for each sensitive attribute."""
    for attr in sensitive_attr:
        print(f"\n⚖️ Disparate Impact Analysis for {attr}:")
        base_rate = None
        
        for group in df[attr].unique():
            group_idx = df[df[attr] == group].index
            
            if len(group_idx) > 0:
                selection_rate = y_pred[group_idx].mean()
                
                if base_rate is None:
                    base_rate = selection_rate  # First group is the reference
                
                dir_ratio = selection_rate / base_rate if base_rate > 0 else 0
                
                print(f"{attr} = {group}: Selection Rate = {selection_rate:.4f}, DIR = {dir_ratio:.4f}")

# Perform Disparate Impact Analysis
disparate_impact(y_pred, ['Gender', 'Race'])

# Fairlearn Metrics for Equalized Odds and Demographic Parity
def fairness_metrics(y_true, y_pred, sensitive_feature):
    metric_frame = MetricFrame(
        metrics={
            'Accuracy': accuracy_score,
            'Precision': precision_score,
            'Recall': recall_score,
            'F1 Score': f1_score,
        },
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive_feature
    )
    print(f"\n📊 Fairness Metrics by {sensitive_feature}:")
    print(metric_frame.by_group)
    
    # Compute fairness disparities
    demographic_parity = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_feature)
    equalized_odds = equalized_odds_difference(y_true, y_pred, sensitive_features=sensitive_feature)
    
    print(f"\n⚖️ Fairness Disparity Metrics for {sensitive_feature}:")
    print(f"  - Demographic Parity Difference: {demographic_parity:.4f}")
    print(f"  - Equalized Odds Difference: {equalized_odds:.4f}")

# Evaluate fairness for Gender and Race
for attr in ['Gender', 'Race']:
    fairness_metrics(y_test, y_pred, df[attr])