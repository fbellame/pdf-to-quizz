#/bin/bash

# deploy fbellame/pdf_to_quizz_llama_13B_lora model on a NVIDIA GeForce RTX 3080 10 Go VRAM runpod, cost about 0.24$/hour

export RUNPOD_KEY=""


curl --request POST \
  --header 'content-type: application/json' \
  --url "https://api.runpod.io/graphql?api_key=${RUNPOD_KEY}" \
  --data '{"query": "mutation { podFindAndDeployOnDemand( input: { cloudType: ALL, gpuCount: 1, volumeInGb: 50, containerDiskInGb: 40, gpuTypeId: \"NVIDIA GeForce RTX 3070\", name: \"peft-gpu-inference\", imageName: \"docker.io/fbellame/peft-gpu-inference:11.7.3\", dockerArgs: \"\", ports: \"8000/http\", volumeMountPath: \"/data\" } ) { id imageName env machineId machine { podHostId } } }"}'