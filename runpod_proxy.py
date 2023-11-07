import time
from runpod import RunPodScheduler
from mistral_inference import MistralTextGenInference

class RunProxyClass:
    def __init__(self, inference_params):
        self.scheduler = RunPodScheduler()

        runpod_id = self.scheduler.get_pod_id()
        url = f"https://{runpod_id}-8000.proxy.runpod.net/"

        self.mistral = MistralTextGenInference(inference_server_url=url, **inference_params)
        self.ensure_pod_is_running_and_instantiate_mistral()

    def ensure_pod_is_running_and_instantiate_mistral(self):
        self.scheduler.ensure_pod_is_running()
        
    def generate_text(self, *args, **kwargs):
        # Ensure that the pod is running and mistral instance is ready
        self.ensure_pod_is_running_and_instantiate_mistral()

        return self.mistral(*args, **kwargs)
