# PDF to Quiz

Upload a multiple page PDF and generate a quiz with multiple options. For each page 2 questions will be generated.

This leverage Langchain library to abstract the LLM (Large Language Model) calls.

The UI is based on Streamlit

Here is an exemple PDF (sorry in french but you can get the idea...)

![PDF sample](img/PDF-sample.png)

Will generate the following interractive quiz questions:

![PDF sample](img/quiz-reponse.png)


## Pre-requisite

You need a GPU to run the 13B model locally or you need to deploy it on HuggingFace by exemple (it's not free!)

You can find [the model on HuggingFace](https://huggingface.co/fbellame/pdf_to_quizz_llama_13B)

The [training  dataset is also available on HuggingFace](https://huggingface.co/datasets/fbellame/pdf_to_quizz_llama_13B)

A video explaining the process is also [available](https://youtu.be/gXXkLVfiBVQ) (in french sorry)

## Instructions


To install:
``` sh
pip install -r requirements.txt
```

## Run


To run:
```sh
streamlit run ui.py
```

