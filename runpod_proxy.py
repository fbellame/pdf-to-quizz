import time
from runpod import RunPodScheduler, PodStartError
from mistral_inference import MistralTextGenInference

class RunProxyClass:
    def __init__(self, inference_params):
        self.scheduler = RunPodScheduler()

        runpod_id = self.scheduler.get_pod_id()
        url = f"https://{runpod_id}-8000.proxy.runpod.net/"
        self.mistral = MistralTextGenInference(inference_server_url=url, **inference_params)


    def start_pod(self):
        backoff_durations = [60, 300, 1800, 3600]  # Backoff times in seconds
        for duration in backoff_durations:
            try:
                # Attempt to start the pod
                self.scheduler.start_pod()
                break  # Exit loop if successful
            except PodStartError as e:  # Replace with the specific exception you expect
                if "not enough free GPUs" in str(e):
                    print(f"Not enough GPUs, retrying in {duration} seconds...")
                    time.sleep(duration)
                else:
                    raise  # Re-raise the exception if it's not the specific GPU error
        else:
            # If the loop completes without breaking, all retries have failed
            print("All retries failed, deleting the pod.")
            self.scheduler.delete_pod()  # Assuming delete_pod is the method to delete the pod        
        
    def generate_text(self, *args, **kwargs):
        result =  self.mistral(*args, **kwargs)

        # if pod is not running, try to start the pod...
        if result is None:
            self.start_pod()

            result =  self.mistral(*args, **kwargs)

        return result
