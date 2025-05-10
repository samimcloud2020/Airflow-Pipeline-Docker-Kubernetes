# Deployment of ML Model with Apache Airflow DAG Pipeline, Docker, Kubernetes & Streamlit UI

YouTube Link: 

## Requirements
1. Apache Airflow 
2. Python
3. Streamlit
4. Docker
5. DockerHub
6. Kubernetes
7. Kubectl


## Set up Environment

```sh
sudo apt update && sudo apt upgrade -y
```
```sh
sudo apt install python3-pip -y

```
```sh
sudo apt install python3.12-venv
```

### Create Python Virtual Environment & Activate it
```sh
python -m venv venv
```
```sh
source venv/bin/activate
```

```sh
pip3 install apache-airflow flask_appbuilder apache-airflow-providers-fab streamlit scikit-learn pandas joblib 
```

## Set up Airflow
### Initialize the Airflow 
```sh
airflow version
```

### Set & Verify Airflow Home
```sh
export AIRFLOW_HOME=~/airflow
```
```sh
echo $AIRFLOW_HOME
```
```sh
sudo airflow db migrate
```
### Confirm Existence of Airflow DB and Configuration File
```sh
ls -l ~/airflow
```

### Create an Admin User for Airflow Web UI
1. Replace "auth_manager = airflow.api_fastapi.auth.managers.simple.simple_auth_manager.SimpleAuthManager" in airflow.cfg file with "auth_manager=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager". 
2. Or you can comment the earlier variable.

```sh
vim ~/airflow/airflow.cfg
```

Create Airflow DAGS Directory
```sh
mkdir -p ~/airflow/dags
```

Make sure the DAG is in the Airflow DAGS Directory
```sh
cp iris_model_pipeline_dag.py ~/airflow/dags/
```
```sh
ls ~/airflow/dags/
```

### Start the Airflow Scheduler, Api-Server, DB, Create Admin User - Starts all Components or Services of Airflow (For Dev Environment)
```sh
airflow standalone
```

On your browser: 
```sh
localhost:8080
```

Get Admin User Password: 
```sh
cat ~/airflow/simple_auth_manager_passwords.json.generated
```

### Build the DAG Pipeline
```sh
python ~/airflow/dags/iris_model_pipeline_dag.py
```

### On Airflow UI

1. Look for the DAG Pipeline named: iris_model_pipeline
2. Toggle the switch to "ON".
3. Click the "Trigger DAG" button (the play icon) to start run.
4. Monitor the run (in the "Graph" or "Grid" view). 

Once DAG Pipeline run is successful, the model artifact (.pkl file) is saved to location: /tmp 
```sh
ls -ld /tmp/
```
```sh
ls /tmp/iris_logistic_model.pkl
```

### Prediction based on Sample Inputs in Script
```sh
sample_data = [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]  # Sample inputs
```

```sh
cat /tmp/iris_predictions.csv
```

## Load Model & Make Prediction on on Streamlit UI
```sh
streamlit run app.py
```

## Build Docker Image of the Trained Model & Its Dependencies In One Artifact 

### Copy ML Model Artifact (.pkl file) to PWD
```sh
cp /tmp/iris_logistic_model.pkl .
```

```sh
docker build -t ml-airflow-streamlit-app .
```

### Create PAT and Log in to Your DockerHub Account
If it fails, go to your DockerHub account and create a Personal Access Token (PAT) - This will be your login password
```sh
docker login -u iquantc
```


### Try Docker Build Again
```sh
docker build -t ml-airflow-streamlit-app .
```

```sh
docker run -p 8501:8501 ml-airflow-streamlit-app
```

### On your browser - Use Network URL or LocalHost
```sh
http://172.17.0.2:8501
```

```sh
http://localhost:8501
```


## Tag Your Local Docker Image
```sh
docker tag ml-airflow-streamlit-app:latest iquantc/ml-airflow-streamlit-app:latest
```

## Push the Image to DockerHub
```sh
docker push iquantc/ml-airflow-streamlit-app:latest
```


## Deploy ML Model Docker Image to Kubernetes
Review manifest files

### Create Minikube cluster
```sh
minikube start --driver=docker
```

### Deploy the Kubernetes Manifest Files
Review the deployment manifest
```sh
kubectl apply -f deployment.yaml
```

### Check the Resources Created
```sh
kubectl get pods
```
```sh
kubectl get svc
```
```sh
minikube ip
```

### Open in Browser

```sh
http://<minikube-ip>:<NodePort>
```

## Clean up

```sh
minikube stop
```
```sh
minikube delete --all
```
