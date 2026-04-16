import numpy as np
import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, precision_recall_curve

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X_train = np.load(os.path.join(base_dir, 'data', 'X_train.npy'))
y_train = np.load(os.path.join(base_dir, 'data', 'y_train.npy'))
X_test = np.load(os.path.join(base_dir, 'data', 'X_test.npy'))
y_test = np.load(os.path.join(base_dir, 'data', 'y_test.npy'))

print("Training RF...")
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

print("Predicting...")
preds = rf.predict(X_test)
probs = rf.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, preds)
prec = precision_score(y_test, preds)
rec = recall_score(y_test, preds)
f1 = f1_score(y_test, preds)
cm = confusion_matrix(y_test, preds)

print(f"Metrics: Acc={acc}, Prec={prec}, Rec={rec}, F1={f1}")
print(f"CM: {cm}")

feature_names = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 
    'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root', 
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 
    'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate', 
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]
importances = rf.feature_importances_
top_indices = np.argsort(importances)[::-1][:4]

features = []
icons = ['data_array', 'protocol', 'lan', 'blur_on']
for i, idx in enumerate(top_indices):
    features.append({
        'name': feature_names[idx].replace('_', ' ').title(),
        'score': float(importances[idx]),
        'icon': icons[i]
    })

p, r, t = precision_recall_curve(y_test, probs)
# Sample 10 points
indices = np.linspace(0, len(p)-1, 10, dtype=int)
pr_curve = [{'precision': float(p[i]), 'recall': float(r[i])} for i in indices]

out = {
    'accuracy': float(acc),
    'precision': float(prec),
    'recall': float(rec),
    'f1': float(f1),
    'cm': {
        'tn': int(cm[0][0]),
        'fp': int(cm[0][1]),
        'fn': int(cm[1][0]),
        'tp': int(cm[1][1])
    },
    'top_features': features,
    'pr_curve': pr_curve
}

with open(os.path.join(base_dir, 'data', 'metrics.json'), 'w') as f:
    json.dump(out, f, indent=4)
print("Saved to data/metrics.json")
