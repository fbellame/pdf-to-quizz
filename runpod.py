import requests
import os
import time
import threading
import yaml

class PodStartError(Exception):
    """Custom exception for errors starting the pod."""
    pass

class DeploymentParams:
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as file:
            params = yaml.safe_load(file)

        self.cloud_type = params.get('cloud_type', 'ALL')
        self.gpu_count = params.get('gpu_count', 1)
        self.volume_in_gb = params.get('volume_in_gb', 50)
        self.container_disk_in_gb = params.get('container_disk_in_gb', 40)
        self.gpu_type_id = params.get('gpu_type_id', 'NVIDIA GeForce RTX 3070')
        self.name = params.get('name', 'peft-gpu-inference')
        self.image_name = params.get('image_name', 'docker.io/fbellame/peft-gpu-inference:12')
        self.docker_args = params.get('docker_args', '')
        self.ports = params.get('ports', '8000/http')
        self.volume_mount_path = params.get('volume_mount_path', '/data')

class RunPodScheduler:
    def __init__(self):
        self.runpod_key = os.getenv('RUNPOD_KEY')
        self.url = f"https://api.runpod.io/graphql?api_key={self.runpod_key}"
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.pod_id = self.find_pod_id()
        self.response_data = None
        self.monitor_thread = None

        self.monitoring_interval = 60 # one minute
        self.idle_threshold = 300 # 5 minutes

        if self.pod_id is not None and not self.is_pod_ready(self.pod_id):
            self.start_pod()

        if self.pod_id is not None:
            self.start_monitor()   
            self.start_gpu_usage() 

    def get_pod_state(self):
        if self.monitor_thread is not None and self.monitor_thread.is_alive():
            return "STARTED"
        else:
            return "STOPPED"

    def start_gpu_usage(self):
        self.update_thread = threading.Thread(target=self.update_gpu_usage, daemon=True)
        self.update_thread.start()

    def start_monitor(self):
        self.last_gpu_usage_time = time.time()
        self.monitor_thread = threading.Thread(target=self.monitor_pod_usage, daemon=True)
        self.monitor_thread.start()

    def update_gpu_usage(self):
        while True:
            self.analyze_pod_runtime()  # This will update the last_gpu_usage_time if GPU is active
            time.sleep(self.monitoring_interval)  # Wait for the specified interval before checking again

    def analyze_pod_runtime(self):
        # ... existing analyze_pod_runtime code ...
        runtime_data = self.get_pod_runtime()
        gpu_usage = self.extract_gpu_usage(runtime_data)
        if gpu_usage > 0:
            self.last_gpu_usage_time = time.time()
        return runtime_data

    def extract_gpu_usage(self, runtime_data):
        # Extract the gpuUtilPercent from the runtime_data
        if (runtime_data is not None):
            gpus = runtime_data.get('gpus', [])
            if gpus:
                return gpus[0].get('gpuUtilPercent', 0)
        return 0        

    def monitor_pod_usage(self):
        while True:
            current_time = time.time()
            if current_time - self.last_gpu_usage_time > self.idle_threshold:  # 300 seconds = 5 minutes
                print("Pod has been idle for 5 minutes, stopping pod.")
                self.stop_pod()
                break  # Stop the thread if the pod has been stopped due to inactivity
            time.sleep(self.monitoring_interval)  # Check every minute     

    def is_pod_ready(self, pod_id):
        query = {
            "query": f"""
            query Pod {{
                pod(input: {{ podId: "{pod_id}" }}) {{
                    id
                    name
                    runtime {{
                        uptimeInSeconds
                        ports {{
                            ip
                            isIpPublic
                            privatePort
                            publicPort
                            type
                        }}
                        gpus {{
                            id
                            gpuUtilPercent
                            memoryUtilPercent
                        }}
                        container {{
                            cpuPercent
                            memoryPercent
                        }}
                    }}
                }}
            }}
            """
        }
        response = requests.post(self.url, headers=self.headers, json=query)

        if response.status_code == 200:
            pod_info = response.json()['data']['pod']
            # Here we assume if the 'runtime' block exists, the pod is ready
            return pod_info['runtime'] is not None
        else:
            print(f"Error checking pod status: {response.status_code} {response.text}")
            return False                 

    def deploy_pod(self, params: DeploymentParams):
        data = {
            "query": f"""
            mutation {{
                podFindAndDeployOnDemand(input: {{
                    cloudType: {params.cloud_type},
                    gpuCount: {params.gpu_count},
                    volumeInGb: {params.volume_in_gb},
                    containerDiskInGb: {params.container_disk_in_gb},
                    gpuTypeId: "{params.gpu_type_id}",
                    name: "{params.name}",
                    imageName: "{params.image_name}",
                    dockerArgs: "{params.docker_args}",
                    ports: "{params.ports}",
                    volumeMountPath: "{params.volume_mount_path}"
                }}) {{
                    id
                    imageName
                    env
                    machineId
                    machine {{
                        podHostId
                    }}
                }}
            }}
            """
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        # Immediately after sending the deployment request, check the response.
        if response.status_code == 200:
            self.response_data = response.json()
            self.pod_id = self.response_data['data']['podFindAndDeployOnDemand']['id']
            print("Deployment in progress, please wait...")

            # Wait for the pod to become ready
            while not self.is_pod_ready(self.pod_id):
                print("Waiting for pod to be ready...")
                time.sleep(30)  # Check every 30 seconds

            print("Pod is ready.")
            self.start_monitor()   
            self.start_gpu_usage()
        else:
            print("Error:", response.status_code, response.text)

    def get_pod_id(self):
        return self.pod_id
    
    def stop_pod(self):
        data = {
            "query": """
            mutation {
                podStop(input: {
                    podId: "%s"
                }) {
                    id
                    desiredStatus
                }
            }
            """ % self.pod_id
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Pod stopped successfully:", response.json())
            return response.json()
        else:
            print("Error stopping pod:", response.status_code, response.text)
            return None    
                
    def start_pod(self):
        data = {
            "query": """
            mutation {
                podResume(input: {
                    podId: "%s",
                    gpuCount: 1
                }) { id desiredStatus imageName env machineId machine { podHostId } }
            }
            """ % self.pod_id
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code == 200:
            response_data = response.json()

            # Vérifier si la réponse contient une erreur spécifique liée aux ressources GPU
            if response_data.get("errors"):
                for error in response_data["errors"]:
                    if "not enough free GPUs" in error["message"]:
                        print("Erreur : Pas assez de GPU libres pour démarrer le pod.")
                        raise PodStartError("Error: Not enough free GPUs to start the pod.")

            # Si pas d'erreur, continuer à attendre que le pod soit prêt
            while not self.is_pod_ready(self.pod_id):
                print("Waiting for pod to be ready...")
                time.sleep(2)

            # Redémarrer le moniteur si nécessaire
            if self.monitor_thread is not None and not self.monitor_thread.is_alive():
                self.start_monitor()

            print("Pod started successfully:", response_data)
            return response_data

        else:
            print("Error starting pod:", response.status_code, response.text)
            return None
  
        
    def get_pods_info(self):
        query = {
            "query": """query Pods { myself { pods { id name runtime { uptimeInSeconds ports { ip isIpPublic privatePort publicPort type } gpus { id gpuUtilPercent memoryUtilPercent } container { cpuPercent memoryPercent } } } } }"""
        }
        response = requests.post(self.url, json=query)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def find_pod_id(self, pod_name='peft-gpu-inference'):
        pods_info = self.get_pods_info()
        for pod in pods_info.get('data', {}).get('myself', {}).get('pods', []):
            if pod.get('name') == pod_name:
                return pod.get('id')
        return None  # If no pod with the specified name is found     

    def get_pod_runtime(self):
        # Assuming get_pods_info() fetches the data as shown in your example
        pods_info = self.get_pods_info()
        runtime_data = None
        
        # Loop through the pods to find runtime data
        for pod in pods_info.get('data', {}).get('myself', {}).get('pods', []):
            if pod.get('runtime') is not None:
                runtime_data = pod.get('runtime')
                break  # Assuming you only want the first occurrence

        return runtime_data        