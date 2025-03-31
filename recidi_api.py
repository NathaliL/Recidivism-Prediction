from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from lime.lime_tabular import LimeTabularExplainer
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import firebase_admin
from firebase_admin import credentials, firestore
import re

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "recidivision_secrect_token"
jwt = JWTManager(app)

cred = credentials.Certificate("firebase/recidivision-6101d-firebase-adminsdk-fbsvc-68941f42fa.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

try:
    model = joblib.load('ensemble_model_downsampled.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

try:
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertModel.from_pretrained('bert-base-uncased')
except Exception as e:
    print(f"Error loading BERT model: {e}")
    tokenizer, bert_model = None, None

def get_embeddings(text):
    if tokenizer is None or bert_model is None:
        raise ValueError("BERT tokenizer/model not loaded properly.")

    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        output = bert_model(**inputs)
    embedding = output.last_hidden_state[:, 0, :].numpy()
    return embedding 


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user_ref = db.collection("users").document(username)
    if user_ref.get().exists:
        return jsonify({"error": "User already exists"}), 409

    user_ref.set({"password": password})
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user_ref = db.collection("users").document(username)
    user = user_ref.get()

    if user.exists and user.to_dict().get("password") == password:
        access_token = create_access_token(identity=username)
        return jsonify({"message": "Login successful", "token": access_token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        required_fields = ["gender", "race", "age_at_release", "education_level", 
                           "supervision_risk_score_first", "residence_puma", "jobs_per_year"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        user_inputs = [
            data["gender"], 
            data["race"], 
            data["age_at_release"], 
            data["education_level"], 
            data["supervision_risk_score_first"], 
            data["residence_puma"], 
            data["jobs_per_year"]
        ]

        user_input_text = " ".join(map(str, user_inputs))

        embedding = get_embeddings(user_input_text)

        if model is None:
            return jsonify({"error": "Model not loaded properly."}), 200

        prediction = model.predict(embedding)
        prediction_label = 'High Risk of Recidivism' if prediction[0] == 1 else 'Low Risk of Recidivism'

        feature_names = [f'feature_{i}' for i in range(embedding.shape[1])]
        explainer = LimeTabularExplainer(training_data=np.random.rand(10, embedding.shape[1]),
                                         mode='classification',
                                         feature_names=feature_names,
                                         class_names=['Non-Recidivist', 'Recidivist'])
        exp = explainer.explain_instance(embedding.flatten(), model.predict_proba, num_features=7)
        explanation = exp.as_list()
        probabilities = model.predict_proba(embedding)[0]

        feature_map = [
            "Gender", "Race", "Age at Release", "Education Level",
            "Supervision Risk Score", "Residence PUMA", "Jobs per Year"
        ]

        explanation_text = f"Based on the information provided, the person is predicted to be a {prediction_label}.\n"

        feature_importance = {}

        for feature, importance in explanation:
            match = re.match(r"feature_(\d+)", feature)
            if match:
                feature_index = int(match.group(1)) % len(feature_map)
                feature_name = feature_map[feature_index]

                if feature_name not in feature_importance or abs(importance) > abs(feature_importance[feature_name]):
                    feature_importance[feature_name] = importance

        for feature_name, importance in feature_importance.items():
            explanation_text += f"The person's {feature_name} had a {importance * 100:.2f}% influence on the prediction.\n"

        return jsonify({
            "prediction": prediction_label,
            "explanation_text": explanation_text,
            "probabilities": {
                "Non-Recidivist": round(probabilities[0] * 100, 2),
                "Recidivist": round(probabilities[1] * 100, 2)
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
