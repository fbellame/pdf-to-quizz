import time
from runpod import RunPodScheduler
from mistral_inference import MistralTextGenInference

class RunProxyClass:
    def __init__(self, inference_params):
        self.scheduler = RunPodScheduler()

        self.ensure_pod_is_running_and_instantiate_mistral()

        runpod_id = self.scheduler.get_pod_id()
        url = f"https://{runpod_id}-8000.proxy.runpod.net/"
        self.mistral = MistralTextGenInference(inference_server_url=url, **inference_params)

    def ensure_pod_is_running_and_instantiate_mistral(self):
        self.scheduler.ensure_pod_is_running()
        
    def generate_text(self, *args, **kwargs):
        # Ensure that the pod is running and mistral instance is ready
        self.ensure_pod_is_running_and_instantiate_mistral()

        result =  self.mistral(*args, **kwargs)

        # if pod is not running, try again to start the pod...
        if result is None:
            self.scheduler.start_pod()

            result =  self.mistral(*args, **kwargs)

        return result
