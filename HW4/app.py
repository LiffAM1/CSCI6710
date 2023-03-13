from flask import Flask, request, jsonify
import tensorflow_decision_forests as tfdf
import tensorflow as tf
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    print(data)
    sample = buildSample(
        int(bool(data.get('romanianAccent') == True)),
        int(bool(data.get('easternAccent') == True)),
        int(bool(data.get('garlic') == True)),
        int(bool(data.get('shadow') == True)),
        int(data.get('complexion')))
    print(sample)
    predictions = model.predict(sample)
    print(predictions)
    class_predictions = classes[round(predictions[0][0])]

    print(f"Predicted: {class_predictions}")

    return jsonify(class_predictions)
    

def buildSample(romanianAccent, easternAccent, garlic, shadow, complexion):
    sample = dict()
    sample['romanianAccent'] = np.array([romanianAccent])
    sample['easternAccent'] = np.array([easternAccent])
    sample['garlic'] = np.array([garlic])
    sample['shadow'] = np.array([shadow])
    sample['complexion'] = np.array([complexion])
    return sample

def train():
    dataset_df = pd.read_csv("vampire_data.csv")

    label = "vampire"

    classes = dataset_df[label].unique().tolist()
    print(f"Label classes: {classes}")

    train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(dataset_df, label=label)

    model = tfdf.keras.RandomForestModel(verbose=2)
    model.fit(train_ds, task=tfdf.keras.Task.CLASSIFICATION)
    return (model,classes)

model,classes = train()
