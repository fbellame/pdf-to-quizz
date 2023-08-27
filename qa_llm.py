from langchain.llms import HuggingFaceTextGenInference

class QaLlm():

    def __init__(self) -> None:
        self.llm = HuggingFaceTextGenInference(
            inference_server_url="http://192.168.1.138:8080/",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.2,
            repetition_penalty=1.03,
        )

    def get_llm(self):
        return self.llm