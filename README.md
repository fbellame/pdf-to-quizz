# PDF to Quiz in Google Form

Upload a multiple page PDF and generate a quiz with multiple options. For each page 1 question will be generated.

You can also generate a google form with the generated quizz.

Here is an exemple PDF (sorry in french but you can get the idea...)

![PDF sample](img/PDF-sample.png)

Will generate the following interractive quiz questions:

![PDF sample](img/quiz-reponse.png)


## Pre-requisite no GPU

In order to generate the Quiz, a fine tuned Mistral 7B must be deployed

You need an RunPod API key if you decide to deploy Mistral LLM on Runpod.

Once you have your API key you can deploy the runPod with: 

``` sh
# deploy the LLM model (fine tuned Mistral 7B) on RunPod
# edit this script to add your runPod key before
./deploy_pod.sh

# once the pod is deployed and running, get the POD_ID
# it's required when launching the app later.
```

## Instructions

To install:
``` sh
pip install -r requirements.txt
```

## Run

To run:
```sh
export RUNPOD_ID=[POD_ID]
streamlit run ui.py
```

To run on docker
```sh
docker build -t pdf-to-quizz .
docker run -e RUNPOD_ID=[POD_ID] -p 80:8501 pdf-to-quizz
```
