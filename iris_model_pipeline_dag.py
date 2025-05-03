from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib
import os

# Define paths
MODEL_PATH = "/tmp/iris_logistic_model.pkl"
PREDICTIONS_PATH = "/tmp/iris_predictions.csv"

# Task 1: Load Iris dataset
def load_data():
    iris = load_iris()
    X = iris.data.tolist()  # Convert NumPy array to list
    y = iris.target.tolist()  # Convert NumPy array to list
    target_names = iris.target_names.tolist()  # Convert NumPy array to list
    return X, y, target_names

# Task 2: Train logistic regression model
def train_model(ti):
    X, y, _ = ti.xcom_pull(task_ids='load_data')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    ti.xcom_push(key='X_test', value=X_test)
    ti.xcom_push(key='y_test', value=y_test)

# Task 3: Evaluate model
def evaluate_model(ti):
    X_test, y_test = ti.xcom_pull(key='X_test', task_ids='train_model'), ti.xcom_pull(key='y_test', task_ids='train_model')
    model = joblib.load(MODEL_PATH)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

# Task 4: Make predictions
def make_predictions(ti):
    _, _, target_names = ti.xcom_pull(task_ids='load_data')
    model = joblib.load(MODEL_PATH)
    sample_data = [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]  # Sample inputs
    predictions = model.predict(sample_data)
    pred_df = pd.DataFrame({
        'Sample': [f"Sample_{i+1}" for i in range(len(sample_data))],
        'Predicted_Class': [target_names[pred] for pred in predictions]
    })
    pred_df.to_csv(PREDICTIONS_PATH, index=False)
    print(f"Predictions saved to {PREDICTIONS_PATH}")

# Define the DAG
with DAG(
    dag_id='iris_model_pipeline',
    start_date=datetime(2025, 5, 2),
    schedule=None,
    catchup=False
) as dag:
    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )
    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )
    evaluate_model_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model
    )
    make_predictions_task = PythonOperator(
        task_id='make_predictions',
        python_callable=make_predictions
    )

    # Set task dependencies
    load_data_task >> train_model_task >> evaluate_model_task >> make_predictions_task