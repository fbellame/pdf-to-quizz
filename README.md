# PDF to Quiz in Google Form

Upload a multiple page PDF and generate a quiz with multiple options. For each page 1 question will be generated.

You can also generate a google form with the generated quizz.

Here is an exemple PDF (sorry in french but you can get the idea...)

![PDF sample](img/PDF-sample.png)

Will generate the following interractive quiz questions:

![PDF sample](img/quiz-reponse.png)

## Pre-requisite Google Form

In order to allow this app to create a google form quizz, you must register an app on Google cloud and generate a client_secrets.json file.
<br>

Please read [Google form developer](https://developers.google.com/forms/api/quickstart/python)

## Pre-requisite no GPU

In order to generate the Quiz, a fine tuned Mistral 7B must be deployed

You need an RunPod API key if you decide to deploy Mistral LLM on Runpod.

Once you have your API key you can deploy the runPod with: 

``` sh
# deploy the LLM model (fine tuned Mistral 7B) on RunPod
# edit this script to add your runPod key before
./deploy_pod.sh
```

## Instructions

To install:
``` sh
pip install -r requirements.txt
```

## Run

To run:
```sh
streamlit run ui.py --server.port 80
```

To run on docker
```sh
docker build -t pdf-to-quizz .
docker run -e RUNPOD_KEY=[RUNPOD_KEY] -p 80:8501 pdf-to-quizz
```
